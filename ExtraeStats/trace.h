#ifndef UTIL_EXTRAE_H
#define UTIL_EXTRAE_H

#include <extrae_user_events.h> 
#include <boost/thread/mutex.hpp>
#include <map>
#include <string>

namespace ExtraeStats
{

class Tracer;

class TraceHandler
{
	private:
		static Tracer	_tracer;

		extrae_type_t		_id;
		std::map<int, int>	_values;

		boost::mutex								_mutex;
	
	public:
		TraceHandler(const char * file_name, const char * function_name);

		~TraceHandler();

		void startFunction();

		void newMark(const int line);

		void endFunction();
};

class DeferFunction
{
	private:
		TraceHandler * _traceHandler;

	public:
		DeferFunction(TraceHandler * traceHandler)
		{
			_traceHandler = traceHandler;
			_traceHandler->startFunction();
		} 
		~DeferFunction() {  _traceHandler->endFunction(); } 
};

}

#ifdef __cplusplus													
	#define TRACE_START_METHOD()									\
		std::string func = typeid(this).name();						\
		func += ":";												\
		func += __FUNCTION__;										\
		static TraceHandler __traceHandler(__FILE__, func.c_str()); \
		DeferFunction __deferFunction(&__traceHandler);				
#endif																

#define TRACE_START_FUNCTION()									\
	static TraceHandler __traceHandler(__FILE__, __FUNCTION__); \
	DeferFunction __deferFunction(&__traceHandler);				

#define TRACE_ADD_MARK_FUNCTION()		\
	__traceHandler.newMark(__LINE__);
	

#endif
