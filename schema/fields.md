# Schema reference

`deps.yaml` (intent, checked in per consumer):

- `schema_version`: must be `1`.
- `packages`: list of entries. Each entry:
  - `name` (required): logical name, e.g. `opencv`, `onnxruntime-gpu`.
  - `kind` (required): `system-library`, `backend-binary`, `tool`, `sibling`.
  - `wanted` (required): version spec, e.g. `==4.6.0`, `>=4.6.0`,
    `>=1.0,<2.0`, or a sibling tag like `v0.10.0`. Bare versions mean `==`.
  - `providers` (required): non-empty subset of `apt`, `snap`, `conan`,
    `vcpkg`, `custom-url`, `fetchcontent`, in priority order.
  - `preferred` (optional): must be a member of `providers`.
  - `package` (optional): provider-side name, e.g. `libopencv-dev`.
    Defaults to `name` when absent.
  - `components`, `linkage`, `platforms` (optional): metadata for readers.
  - `url`, `sha256` (required when `custom-url` is listed): pinned
    download coordinates; `sha256` is 64 hex chars.
  - `repo`, `ref` (required when `fetchcontent` is listed): `org/repo`
    plus a 40-char SHA or `vX.Y.Z` tag.
  - `env_var` (optional): `versions.env` key override. Default is
    `NAME_UPPER with non-alphanumerics as _` plus `_VERSION`.
  - Sibling entries (`kind: sibling`) must list `fetchcontent`.

`deps.lock` (resolved, checked in; the only thing installers execute):

- `schema_version`: `1`.
- `resolved`: list of `{name, version, provider}` plus optional
  `package`, `env_var`, `sha256`, `repo`, `ref`.
- The lock provider for each entry must be a member of the manifest
  `providers` for that name; otherwise validation fails closed instead
  of silently mixing providers.

Precedence: `cmake -D` > environment > `versions.env` > lockfile default.
