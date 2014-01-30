
#include "trace.h"
#include <iostream>

#include <boost/thread.hpp>

void two()
{
	TRACE_START_FUNCTION()
}

void one()
{
	TRACE_START_FUNCTION()

	boost::thread t(two);
	t.join();
}

void testFunction()
{
	TRACE_START_FUNCTION()

	boost::thread t(one);
	t.join();

	TRACE_ADD_MARK_FUNCTION()

}

class clase
{
	int m;

public:
	int function()
	{
		TRACE_START_FUNCTION()
	}
	int method()
	{
		TRACE_START_METHOD()									
	}
};

int main()
{
	TRACE_START_FUNCTION()
	TRACE_ADD_MARK_FUNCTION()
	testFunction();
	TRACE_ADD_MARK_FUNCTION()
	TRACE_ADD_MARK_FUNCTION()
	testFunction();
	boost::thread t(testFunction);

	std::cout<<__FILE__<<" "<<__FUNCTION__<< " "<<__LINE__<<std::endl;

	t.join();

	clase c;
	c.function();
	c.method();

	return 0;
}
