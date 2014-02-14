#ifndef UTIL_EXTRAE_H
#define UTIL_EXTRAE_H

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

		unsigned			_id;
		std::map<int, int>*	_values;

		boost::mutex		_mutex;
	
	public:
		TraceHandler(const char * file_name, const char * function_name, const int line);

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

#define TRACE_START_METHOD()									\
	std::string func = typeid(this).name();						\
	func += ":";												\
	func += __FUNCTION__;										\
	static ExtraeStats::TraceHandler __traceHandler(__FILE__, func.c_str(), __LINE__); \
	ExtraeStats::DeferFunction __deferFunction(&__traceHandler);				

#define TRACE_START_FUNCTION()									\
	static ExtraeStats::TraceHandler __traceHandler(__FILE__, __FUNCTION__, __LINE__); \
	ExtraeStats::DeferFunction __deferFunction(&__traceHandler);				

#define TRACE_ADD_MARK_FUNCTION()		\
	__traceHandler.newMark(__LINE__);
	

#endif
