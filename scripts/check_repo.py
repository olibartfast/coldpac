#!/usr/bin/env python3
"""coldpac repo gate: ASCII + fixtures validate + export round-trip."""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.join(ROOT, "coldpac")
SKIP_DIRS = {".git", "__pycache__"}


def fail(errors, msg):
    errors.append(msg)


def check_ascii(errors):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                with open(p, "rb") as h:
                    raw = h.read()
                raw.decode("ascii")
            except UnicodeDecodeError:
                fail(errors, "non-ASCII content: %s" % os.path.relpath(p, ROOT))


def run(*argv):
    r = subprocess.run([sys.executable, EXE] + list(argv),
                       capture_output=True, text=True)
    return r


def main():
    errors = []
    check_ascii(errors)
    for ex in ("minimal-apt", "backend-mixed", "sibling"):
        d = os.path.join(ROOT, "examples", ex)
        r = run("--manifest", os.path.join(d, "deps.yaml"),
                "--lock", os.path.join(d, "deps.lock"), "validate")
        if r.returncode != 0:
            fail(errors, "%s validate failed: %s" % (ex, r.stderr.strip()))
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "versions.env")
            r = run("--manifest", os.path.join(d, "deps.yaml"),
                    "--lock", os.path.join(d, "deps.lock"),
                    "export", "--out", out)
            if r.returncode != 0:
                fail(errors, "%s export failed: %s" % (ex, r.stderr.strip()))
                continue
            with open(out, encoding="ascii") as h:
                got = h.read()
            with open(os.path.join(d, "versions.env.expected"),
                      encoding="ascii") as h:
                want = h.read()
            if got != want:
                fail(errors, "%s export drift" % ex)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tests", "run.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fail(errors, "tests/run.py failed:\n%s" % (r.stdout + r.stderr))
    if errors:
        for e in errors:
            print("ERROR: %s" % e, file=sys.stderr)
        return 1
    print("coldpac repo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
