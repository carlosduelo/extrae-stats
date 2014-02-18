#include "trace.h"

#include <iostream>
#include <fstream>
#include <extrae_user_events.h> 

namespace ExtraeStats
{

class Tracer
{
	public:
		unsigned int								_typeId;
		std::map<std::string, unsigned int>			_values;
		std::map<unsigned int, std::map<int, int>*>	_FunctionValues;
		boost::mutex								_mutex;

		Tracer() : _typeId(60000) {}

		~Tracer()
		{
			boost::mutex::scoped_lock lock(_mutex);
			std::ofstream outFile;
			outFile.open("functions.func", std::ios::out | std::ios::trunc);
			outFile<< "#Functions"<<std::endl;
			for (std::map<std::string, unsigned int>::iterator it= _values.begin(); it != _values.end(); ++it)
			{
				outFile << it->second;
				std::map<unsigned int, std::map<int,int>*>::iterator mapF = _FunctionValues.find(it->second);
				for (std::map<int,int>::iterator itV = ((mapF->second))->begin(); 
						itV != (mapF->second)->end(); ++itV)
				{
					outFile << " " <<  itV->first << " " << itV->second;
				}
				outFile<<'\n';
			}
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
				std::map<int, int> * m = new std::map<int,int>();
				Tracer::_FunctionValues.insert(std::pair<unsigned int, std::map<int, int>*>(Tracer::_typeId, m));
				return Tracer::_typeId;
			}

		}
		std::map<int, int> * getFunctionValues(unsigned id)
		{
			boost::mutex::scoped_lock lock(_mutex);
			std::map<unsigned int, std::map<int, int>*>::iterator it = Tracer::_FunctionValues.find(id);

			if (it != Tracer::_FunctionValues.end())
			{
				return it->second;
			}
			else
			{
				std::cout<<"Error, trace function"<<std::endl;
				exit(1);	
			}
		}
};

Tracer TraceHandler::_tracer;

TraceHandler::TraceHandler(const char * file_name, const char * function_name, const int line) : _id(-1)
{
	std::string desc(file_name);
	desc += ":";
	desc += function_name;
	unsigned int nvalues = 0;
	_id = TraceHandler::_tracer.getType(desc);
	_values = TraceHandler::_tracer.getFunctionValues(_id);
	_values->insert(std::pair<int, int>(line, 1));
	Extrae_define_event_type (&_id, (char*)desc.c_str(), &nvalues, NULL, NULL);
}

TraceHandler::~TraceHandler()
{
}

void TraceHandler::startFunction()
{
	Extrae_event(_id, 1);
}

void TraceHandler::newMark(const int line)
{
	boost::mutex::scoped_lock lock(_mutex);
	std::map<int, int>::iterator it = _values->find(line);
	if (it != _values->end())
	{
		Extrae_event(_id, it->second);
	}
	else
	{
		int value = 1 + _values->size();
		_values->insert(std::pair<int, int>(line, value));
		Extrae_event(_id, value);
	}
}

void TraceHandler::endFunction()
{
	Extrae_event(_id, 0);
}

}
