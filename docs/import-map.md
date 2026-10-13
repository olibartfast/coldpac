# Import map: existing versions.env files to coldpac manifest

`coldpac import --env <file> --out deps.yaml` translates the four current
`versions.env` files losslessly. Rules:

## Known keys

| versions.env key | manifest name | kind | providers | notes |
| --- | --- | --- | --- | --- |
| OPENCV_VERSION | opencv | system-library | apt, conan, vcpkg, custom-url | package `libopencv-dev` |
| OPENCV_MIN_VERSION | opencv | system-library | apt, conan, vcpkg | wanted `>=value` |
| OPENCV_REVIEWED_VERSION | opencv | system-library | apt | wanted `==value` incl. debian revision |
| GSTREAMER_VERSION / GSTREAMER_REVIEWED_VERSION | gstreamer | system-library | apt | |
| FFMPEG_VERSION / FFMPEG_REVIEWED_VERSION | ffmpeg | system-library | apt | |
| GLOG_MIN_VERSION | glog | system-library | apt, conan, vcpkg | wanted `>=value` |
| CMAKE_VERSION / CMAKE_MIN_VERSION / CMAKE_REVIEWED_VERSION | cmake | tool | apt | |
| ONNX_RUNTIME_VERSION | onnxruntime-gpu | backend-binary | custom-url | url+sha256 must be pinned |
| TENSORRT_VERSION | tensorrt | backend-binary | custom-url | url+sha256 must be pinned |
| PYTORCH_VERSION | libtorch | backend-binary | custom-url | url+sha256 must be pinned |
| OPENVINO_VERSION | openvino | backend-binary | custom-url | url+sha256 must be pinned |
| TENSORFLOW_VERSION | tensorflow | backend-binary | custom-url | url+sha256 must be pinned |
| LITERT_VERSION | litert | backend-binary | custom-url | url+sha256 must be pinned |
| EXECUTORCH_VERSION | executorch | backend-binary | custom-url | url+sha256 must be pinned |
| TVM_VERSION / GGML_VERSION / MIGRAPHX_VERSION / CACTUS_VERSION / LLAMACPP_VERSION / DALI_VERSION | same lowercased name | backend-binary | custom-url | url+sha256 must be pinned |
| CUDA_VERSION | cuda | tool | apt, custom-url | |
| NEURIPLO_VERSION | neuriplo | sibling | fetchcontent | repo `olibartfast/neuriplo` |
| VIDEOCAPTURE_VERSION | videocapture | sibling | fetchcontent | repo `olibartfast/videocapture` |
| NEURIPLO_TASKS_VERSION | neuriplo-tasks | sibling | fetchcontent | repo `olibartfast/neuriplo-tasks` |
| NEURIPLO_KSERVE_CLIENT_VERSION | neuriplo-kserve-client | sibling | fetchcontent | repo `olibartfast/neuriplo-kserve-client` |

## Skipped keys (metadata, not packages)

`UBUNTU_RELEASE`, `DOCKER_BASE_IMAGE`, `DOCKER_USER`, `DOCKER_WORKDIR`,
`OPENVINO_FULL_ID`. Reported as notes, never emitted as packages.

## Generic fallback

Unmapped `*_VERSION` keys become apt entries named from the key
(`FOO_BAR_VERSION` -> `foo-bar`, `==value`); `*_MIN_VERSION` keys become
`>=value`. Each is reported as `note:` on stderr for human review.

## env_var round-trip

Every imported entry keeps its original key in `env_var`, so
`coldpac export` regenerates the identical `KEY=value` line. Verified by
the export round-trip in `scripts/check_repo.py`.
