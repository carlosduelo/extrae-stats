
#include "trace.h"
#include <iostream>
#include <unistd.h>

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

int recursive(int n)
{
	TRACE_START_FUNCTION()
	sleep(1);
	if (n)
	{
		TRACE_ADD_MARK_FUNCTION()
		sleep(1);
		TRACE_ADD_MARK_FUNCTION()
		return recursive(n-1);
	}
	else
	{
		TRACE_ADD_MARK_FUNCTION()
		sleep(2);
		return 0;
	}
}

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


	recursive(5);

	return 0;
}
