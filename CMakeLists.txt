project(foobinding)

cmake_minimum_required(VERSION 2.6)

set(LIBFOO_DIR ${CMAKE_SOURCE_DIR}/libfoo)

if(CMAKE_HOST_UNIX)
 option(ENABLE_GCC_OPTIMIZATION "Enable specific GCC flags to optimization library size and performance. Only available on Release Mode" 0)
 set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-strict-aliasing")
 set(CMAKE_CXX_FLAGS_DEBUG "-g")
 if(ENABLE_GCC_OPTIMIZATION)
 set(CMAKE_BUILD_TYPE Release)
 set(CMAKE_CXX_FLAGS_RELEASE "-DNDEBUG -Os -Wl,-O1")
 if(NOT CMAKE_HOST_APPLE)
 set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wl,—hash-style=gnu")
 endif()
 endif()

 if(CMAKE_HOST_APPLE)
 if (NOT QT_INCLUDE_DIR)
 set(QT_INCLUDE_DIR "/Library/Frameworks")
 endif()
 endif()
endif()

# CMake error: include called with wrong number of arguments.  include() only takes one file.
# This is a result of QT_USE_FILE being empty.
# https://stackoverflow.com/questions/28252909/cmake-and-qt5-include-only-takes-one-argument
#include(${QT_USE_FILE})

add_subdirectory(libfoo)
add_subdirectory(foo)

# build libfoo before foo
add_dependencies(foo libfoo)
