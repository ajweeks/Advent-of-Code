#pragma once

#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>
#include <algorithm>

struct v2i
{
	v2i() {}
	v2i(int x, int y) : x(x), y(y) {}

	v2i(const v2i& rhs) : x(rhs.x), y(rhs.y) {}
	v2i(v2i&& rhs) { std::swap(rhs.x, x); std::swap(rhs.y, y); }

	v2i operator+(const v2i& rhs) const { return v2i(x + rhs.x, y + rhs.y); }
	v2i& operator=(const v2i& rhs) { x = rhs.x; y = rhs.y; return *this; }

	int x = 0, y = 0;
	
	friend std::ostream& operator<<(std::ostream& stream, const v2i& lhs);
};
std::ostream& operator<<(std::ostream& stream, const v2i& lhs) { stream << lhs.x << ", " << lhs.y; return stream; };
static bool operator==(const v2i& lhs, const v2i& rhs) { return rhs.x == lhs.x && rhs.y == lhs.y; }

void RemoveSpaces(std::string& str)
{
	str.erase(std::remove_if(str.begin(), str.end(), isspace), str.end());
}

std::vector<std::string> Split(const std::string& values, char delim = '\n')
{
	std::vector<std::string> result;
	std::stringstream valuesStream(values);

	while (valuesStream.good())
	{
		std::string line;
		getline(valuesStream, line, delim);
		if (line.length() > 0)
		{
			result.push_back(line);
		}
	}

	return result;
}

inline void RemoveCharFromString(std::string& str, char character)
{
	str.erase(std::remove_if(str.begin(), str.end(), [&character](char c) { return c == character; }), str.end());
}

template<class T>
bool ContainsDuplicates(const std::vector<T>& vec)
{
	for (size_t i = 0; i < vec.size(); i++)
	{
		for (size_t j = i + 1; j < vec.size(); j++)
		{
			if (vec[i] == vec[j]) return true;
		}
	}
	return false;
}

template<class T>
bool Contains(const std::vector<T>& vec, const T& t)
{
	for (size_t i = 0; i < vec.size(); i++)
	{
		if (vec[i] == t) return true;
	}
	return false;
}

bool ReadFile(std::string& str, const std::string& filePath, bool outputErrors = true)
{
	std::ifstream fileStream(filePath);
	if (!fileStream.is_open())
	{
		if (outputErrors)
		{
			std::cout << "Couldn't open " << filePath << std::endl;
		}
		return false;
	}

	std::string line;
	std::stringstream stringStream;
	while (!fileStream.eof())
	{
		std::getline(fileStream, line);
		stringStream << line << "\n";
	}
	str = stringStream.str();

	fileStream.close();

	return true;
}