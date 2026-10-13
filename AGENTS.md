# Agent Instructions

- This repo owns the manifest schema, provider probes, lockfile rules,
  `versions.env` projection, and `status`/`check-updates` commands.
- Keep the `coldpac` executable stdlib-only and Python 3.12 compatible.
- Keep all files ASCII-only. Scripts must be executable with clear errors
  and nonzero exits on failure.
- Consumer repos fetch this repo pinned to a tag; never add consumer-side
  build logic here.
- Validate with `python3 tests/run.py` and `python3 scripts/check_repo.py`
  before every commit.
