PROJECT(conanmysqlclient)
cmake_minimum_required(VERSION 2.8)
include(${CMAKE_BINARY_DIR}/../../conanbuildinfo.cmake)
#instead the full conan_basic_setup, just these, so avoid messing with the output paths
conan_check_compiler()
conan_flags_setup()
include("CMakeListsOriginal.cmake")
