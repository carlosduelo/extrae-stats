set -x
export LD_LIBRARY_PATH=/home/cduelo/Extrae/lib
export EXTRAE_HOME=/home/cduelo/Extrae
export EXTRAE_CONFIG_FILE=trace.xml

g++ -c trace.cpp -o trace.o -I/home/cduelo/Extrae/include -DUSE_UTIL_EXTRAE && g++ test.cpp trace.o -I${EXTRAE_HOME}/include -o test -DUSE_UTIL_EXTRAE -L${EXTRAE_HOME}/lib -lpttrace -lboost_thread

./test

#mv set-0/TRACE* .
#/home/cduelo/Extrae/bin/mpi2prv -e ./test TRACE*
#rm TRACE*
