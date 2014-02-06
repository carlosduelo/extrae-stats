
# Compile ExtraeStats
include_directories(${EXTRAE_INCLUDE_DIRS})
add_library(ExtraeStats SHARED trace.cpp )

# install
install(FILES trace.h DESTINATION include/ExtraeStats )
install (TARGETS ExtraeStats LIBRARY DESTINATION lib)
install (FILES	application_data.py
				function_data.py
				parseFUNC.py
				parsePCF.py
				parsePRV.py
				parser.py
				stats.py
				thread_data.py
				viso.py
				DESTINATION bin/ExtraeStats/viso)
