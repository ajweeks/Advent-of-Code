#pragma once

#include "CommonFunctions.h"

#include <string>
#include <sstream>
#include <vector>
#include <iostream>

//--- Day 3: Squares With Three Sides ---

namespace Day3
{
	bool TrianglePossible(int a, int b, int c)
	{
		return ((a < b + c) &&
				(b < a + c) &&
				(c < a + b));
	}

	int PossibleTrianglesSimple(const std::string& inputString)
	{
		int numTrisPossible = 0;

		std::vector<std::string> triangles = Split(inputString);
		for (size_t i = 0; i < triangles.size(); i++)
		{
			std::vector<std::string> tri1 = Split(triangles[i], ' ');
			if (TrianglePossible(stoi(tri1[0]), stoi(tri1[1]), stoi(tri1[2]))) ++numTrisPossible;
		}

		return numTrisPossible;
	}

	int PossibleTrianglesComplex(const std::string& inputString)
	{
		int numTrisPossible = 0;

		std::vector<std::string> triangles = Split(inputString);
		for (size_t i = 0; i < triangles.size() - 2; i += 3)
		{
			std::vector<std::string> triInd1 = Split(triangles[i], ' ');
			std::vector<std::string> triInd2 = Split(triangles[i + 1], ' ');
			std::vector<std::string> triInd3 = Split(triangles[i + 2], ' ');
			if (TrianglePossible(stoi(triInd1[0]), stoi(triInd2[0]), stoi(triInd3[0]))) ++numTrisPossible;
			if (TrianglePossible(stoi(triInd1[1]), stoi(triInd2[1]), stoi(triInd3[1]))) ++numTrisPossible;
			if (TrianglePossible(stoi(triInd1[2]), stoi(triInd2[2]), stoi(triInd3[2]))) ++numTrisPossible;
		}

		return numTrisPossible;
	}

	void Day3()
	{
		std::cout << "Day 3:" << std::endl;

		std::string input;
		if (ReadFile(input, "input/Day3Input.txt"))
		{
			int numTrisPossibleSimple = PossibleTrianglesSimple(input);
			std::cout << "Number of possible triangles (simple): " << numTrisPossibleSimple << std::endl;

			int numTrisPossibleComplex = PossibleTrianglesComplex(input);
			std::cout << "Number of possible triangles (complex): " << numTrisPossibleComplex << std::endl;
		}

		std::cout << std::endl;
	}
}