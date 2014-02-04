#!/bin/bash

if [ -z "${EXTRAE_HOME}" ]
then
	echo  "Please set EXTRAE_HOME"
else
	export LD_LIBRARY_PATH=${EXTRAE_HOME}/lib
	export EXTRAE_CONFIG_FILE=trace.xml

	g++ -c ../trace.cpp -o trace.o -I${EXTRAE_HOME}/include -DUSE_UTIL_EXTRAE  
	g++ test.cpp trace.o -I${EXTRAE_HOME}/include -I../ -o test -DUSE_UTIL_EXTRAE -L${EXTRAE_HOME}/lib -lpttrace -lboost_thread 
	./test
fi
