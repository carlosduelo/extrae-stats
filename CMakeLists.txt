cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(ExtraeStats)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/CMake)

#include(Buildyard)
#if(BUILDYARD_STOP)
#  return()
#endif()

# Find Extrae
find_package(Extrae REQUIRED)

if (EXTRAE_FOUND)

	# Compile library
	add_subdirectory(ExtraeStats)

	# Compile example
	add_subdirectory(test-app)

else()
	message(FATAL_ERROR "Extrae missing")
endif()
