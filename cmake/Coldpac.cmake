# Coldpac CMake helper
#
# Usage in a consumer after FetchContent_MakeAvailable(coldpac):
#
#   include(${coldpac_SOURCE_DIR}/cmake/Coldpac.cmake)
#   coldpac_export(
#     MANIFEST ${CMAKE_CURRENT_SOURCE_DIR}/deps.yaml
#     LOCK ${CMAKE_CURRENT_SOURCE_DIR}/deps.lock
#     OUT ${CMAKE_CURRENT_BINARY_DIR}/versions.env)
#
# The generated versions.env keeps `cmake -D > versions.env` precedence:
# pass -D explicitly and it wins over the file.

find_package(Python3 COMPONENTS Interpreter REQUIRED)

function(coldpac_export)
  cmake_parse_arguments(ARG "" "MANIFEST;LOCK;OUT;COLDPAC" "" ${ARGN})
  if(NOT ARG_MANIFEST)
    message(FATAL_ERROR "coldpac_export: MANIFEST is required")
  endif()
  if(NOT ARG_LOCK)
    message(FATAL_ERROR "coldpac_export: LOCK is required")
  endif()
  if(NOT ARG_OUT)
    message(FATAL_ERROR "coldpac_export: OUT is required")
  endif()
  if(NOT ARG_COLDPAC)
    set(ARG_COLDPAC "${CMAKE_CURRENT_LIST_DIR}/../coldpac")
  endif()
  add_custom_command(
    OUTPUT "${ARG_OUT}"
    COMMAND "${Python3_EXECUTABLE}" "${ARG_COLDPAC}"
      --manifest "${ARG_MANIFEST}" --lock "${ARG_LOCK}"
      export --out "${ARG_OUT}"
    DEPENDS "${ARG_LOCK}" "${ARG_COLDPAC}"
    COMMENT "coldpac: generating versions.env"
    VERBATIM)
endfunction()
