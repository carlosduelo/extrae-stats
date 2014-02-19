
find_package(Boost REQUIRED COMPONENTS thread)

if (Boost_FOUND)

	include_directories(${CMAKE_SOURCE_DIR}/ExtraeStats)
	include_directories(${EXTRAE_INCLUDE_DIRS})
	include_directories(${Boost_INCLUDE_DIRS})
	add_executable(testExtraeStats test.cpp)
	target_link_libraries(testExtraeStats ExtraeStats ${Boost_LIBRARIES})

	install(FILES extrae-config-file-example.xml DESTINATION bin/ExtraeStats)
	configure_file(extrae-trace ${CMAKE_INSTALL_PREFIX}/bin/ExtraeStats/extrae-trace @ONLY)

else()
	message(FATAL_ERROR "Not found Boost")
endif()
