#include "trace.h"

#ifdef USE_UTIL_EXTRAE 

#include <iostream>
#include <fstream>


class Tracer
{
	public:
		unsigned int								_typeId;
		std::map<std::string, unsigned int>			_values;
		boost::mutex								_mutex;

		Tracer() : _typeId(60000) {}

		~Tracer()
		{
			std::ofstream outFile;
			outFile.open("functions.func", std::ios::out | std::ios::trunc);
			outFile<< "#Functions"<<std::endl;
			for (std::map<std::string, unsigned int>::iterator it= _values.begin(); it != _values.end(); ++it)
			    outFile << it->second<<'\n';
			outFile.close();
		}

		unsigned int getType(std::string desc)
		{
			boost::mutex::scoped_lock lock(_mutex);
			std::map<std::string, unsigned int>::iterator it = Tracer::_values.find(desc);

			if (it != Tracer::_values.end())
			{
				return it->second;
			}
			else
			{
				Tracer::_typeId++;
				Tracer::_values.insert( std::pair<std::string, unsigned int>(desc, Tracer::_typeId));
				return Tracer::_typeId;
			}

		}			
};

Tracer TraceHandler::_tracer;

TraceHandler::TraceHandler(const char * file_name, const char * function_name) : _id(-1)
{
	std::string desc(file_name);
	desc += ":";
	desc += function_name;
	unsigned int nvalues = 0;
	_id = TraceHandler::_tracer.getType(desc);
	Extrae_define_event_type (&_id, (char*)desc.c_str(), &nvalues, NULL, NULL);
}

TraceHandler::~TraceHandler()
{
}

void TraceHandler::startFunction()
{
	boost::mutex::scoped_lock lock(_mutex);
	Extrae_event(_id, 1);
}

void TraceHandler::newMark(const int line)
{
	boost::mutex::scoped_lock lock(_mutex);
	std::map<int, int>::iterator it = _values.find(line);
	if (it != _values.end())
	{
		Extrae_event(_id, it->second);
	}
	else
	{
		int value = 2 + _values.size();
		_values.insert(std::pair<int, int>(line, value));
		Extrae_event(_id, value);
	}
}

void TraceHandler::endFunction()
{
	Extrae_event(_id, 0);
}

#endif
