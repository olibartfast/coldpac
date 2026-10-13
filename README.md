# coldpac

Standalone manager of package managers for C++ projects.

One manifest per project (`deps.yaml`), one resolved lockfile
(`deps.lock`), one generated `versions.env`, and one `status` view across
providers: `apt`, `snap`, `conan`, `vcpkg`, `custom-url`, `fetchcontent`.

Consumers fetch this repo pinned to a tag via CMake `FetchContent`:

```cmake
FetchContent_Declare(
  coldpac
  GIT_REPOSITORY https://github.com/olibartfast/coldpac.git
  GIT_TAG v0.1.0
)
```

Then:

```sh
python3 <coldpac>/coldpac --manifest deps.yaml --lock deps.lock validate
python3 <coldpac>/coldpac --manifest deps.yaml --lock deps.lock resolve
python3 <coldpac>/coldpac --manifest deps.yaml --lock deps.lock status
python3 <coldpac>/coldpac --manifest deps.yaml --lock deps.lock export --out versions.env
python3 <coldpac>/coldpac --manifest deps.yaml check-updates
python3 <coldpac>/coldpac --manifest deps.yaml import --env versions.env --out deps.yaml
```

## Layout

- `coldpac`: single-file executable (stdlib only, no third-party deps).
- `cmake/Coldpac.cmake`: `coldpac_export()` helper for CMake consumers.
- `schema/`: field reference for `deps.yaml` / `deps.lock`.
- `examples/`: golden fixtures per provider mix.
- `tests/run.py`: stdlib test runner (no pytest needed).
- `scripts/check_repo.py`: repo gate (ASCII + fixtures + export round-trip).
- `docs/import-map.md`: lossless mapping from the existing
  `versions.env` files.

## Status codes

`status` and `check-updates` exit `0` clean, `2` updates available,
`1` error or drift. `--offline` performs zero network calls.

## Versioning

Tags `vX.Y.Z` on `main`. See `CHANGELOG.md`.
