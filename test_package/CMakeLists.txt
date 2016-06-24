PROJECT(MySQLClientTestVersion)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_VERBOSE_MAKEFILE ON)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(version version.cpp)
target_link_libraries (version ${CONAN_LIBS})
