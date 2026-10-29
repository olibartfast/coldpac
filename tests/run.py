#!/usr/bin/env python3
"""coldpac stdlib test runner. Run: python3 tests/run.py"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.join(ROOT, "coldpac")


def run_coldpac(*argv):
    r = subprocess.run([sys.executable, EXE] + list(argv),
                       capture_output=True, text=True)
    return r


class ValidateTest(unittest.TestCase):
    def test_all_fixtures_validate(self):
        for ex in ("minimal-apt", "backend-mixed", "sibling"):
            d = os.path.join(ROOT, "examples", ex)
            r = run_coldpac("--manifest", os.path.join(d, "deps.yaml"),
                            "--lock", os.path.join(d, "deps.lock"),
                            "validate")
            self.assertEqual(r.returncode, 0, msg=r.stderr)

    def test_unknown_provider_fails(self):
        with tempfile.TemporaryDirectory() as td:
            m = os.path.join(td, "deps.yaml")
            with open(m, "w", encoding="ascii") as h:
                h.write("schema_version: 1\npackages:\n"
                        "  - name: foo\n    kind: tool\n"
                        "    wanted: ==1.0\n    providers: [brew]\n")
            r = run_coldpac("--manifest", m, "--lock", os.path.join(td, "deps.lock"),
                            "validate")
            self.assertEqual(r.returncode, 1)
            self.assertIn("unknown provider", r.stderr)

    def test_mixed_lock_provider_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            m = os.path.join(td, "deps.yaml")
            with open(m, "w", encoding="ascii") as h:
                h.write("schema_version: 1\npackages:\n"
                        "  - name: opencv\n    kind: system-library\n"
                        "    wanted: ==4.6.0\n    providers: [apt]\n")
            lock = os.path.join(td, "deps.lock")
            with open(lock, "w", encoding="ascii") as h:
                h.write("schema_version: 1\nresolved:\n"
                        "  - name: opencv\n    version: 4.6.0\n"
                        "    provider: snap\n")
            r = run_coldpac("--manifest", m, "--lock", lock, "validate")
            self.assertEqual(r.returncode, 1)
            self.assertIn("silently mix", r.stderr)


class ExportTest(unittest.TestCase):
    def test_export_matches_expected(self):
        for ex in ("minimal-apt", "backend-mixed", "sibling"):
            d = os.path.join(ROOT, "examples", ex)
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, "versions.env")
                r = run_coldpac("--manifest", os.path.join(d, "deps.yaml"),
                                "--lock", os.path.join(d, "deps.lock"),
                                "export", "--out", out)
                self.assertEqual(r.returncode, 0, msg=r.stderr)
                with open(out, encoding="ascii") as h:
                    got = h.read()
                with open(os.path.join(d, "versions.env.expected"),
                          encoding="ascii") as h:
                    want = h.read()
                self.assertEqual(got, want, msg=ex)


class ResolveTest(unittest.TestCase):
    def test_resolve_picks_preferred(self):
        with tempfile.TemporaryDirectory() as td:
            m = os.path.join(ROOT, "examples", "backend-mixed", "deps.yaml")
            lock = os.path.join(td, "deps.lock")
            r = run_coldpac("--manifest", m, "--lock", lock, "resolve")
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            r2 = run_coldpac("--manifest", m, "--lock", lock, "validate")
            self.assertEqual(r2.returncode, 0, msg=r2.stderr)

    def test_resolve_keeps_debian_epoch(self):
        with tempfile.TemporaryDirectory() as td:
            m = os.path.join(td, "deps.yaml")
            with open(m, "w", encoding="ascii") as h:
                h.write("schema_version: 1\npackages:\n"
                        "  - name: ffmpeg\n    kind: system-library\n"
                        '    wanted: "==7:6.1.1-3ubuntu5"\n'
                        "    providers: [apt]\n")
            lock = os.path.join(td, "deps.lock")
            r = run_coldpac("--manifest", m, "--lock", lock, "resolve")
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            with open(lock, encoding="ascii") as h:
                text = h.read()
            self.assertIn("7:6.1.1-3ubuntu5", text)


class ImportTest(unittest.TestCase):
    def test_import_minimal_env(self):
        with tempfile.TemporaryDirectory() as td:
            env = os.path.join(td, "versions.env")
            with open(env, "w", encoding="ascii") as h:
                h.write("OPENCV_VERSION=4.6.0\nNEURIPLO_VERSION=v0.10.0\n")
            out = os.path.join(td, "deps.yaml")
            r = run_coldpac("import", "--env", env, "--out", out)
            self.assertEqual(r.returncode, 0, msg=r.stderr)
            with open(out, encoding="ascii") as h:
                text = h.read()
            self.assertIn("opencv", text)
            self.assertIn("neuriplo", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
