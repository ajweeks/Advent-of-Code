#pragma once

#include "CommonFunctions.h"

#include <string>
#include <iostream>
#include <vector>
#include <sstream>

//--- Day 2: Bathroom Security ---

namespace Day2
{
	enum Direction
	{
		UP, LEFT, DOWN, RIGHT
	};

	static int digitsSimple[3][3] = {
		{ 1, 2, 3 },
		{ 4, 5, 6 },
		{ 7, 8, 9 },
	};

	int GetKeyCodeSimple(const std::string& path)
	{
		std::vector<std::string> values = Split(path);
		int result = 0;
		int currentDigit = 0;

		v2i currentLocation = { 1, 1 };
		for (size_t i = 0; i < values.size(); i++)
		{
			for (size_t j = 0; j < values[i].length(); j++)
			{
				const char currentMove = values[i].at(j);
				switch (currentMove)
				{
				case 'R':
					if (currentLocation.x < 2) currentLocation.x++;
					break;
				case 'D':
					if (currentLocation.y < 2) currentLocation.y++;
					break;
				case 'L':
					if (currentLocation.x > 0) currentLocation.x--;
					break;
				case 'U':
					if (currentLocation.y > 0) currentLocation.y--;
					break;
				}
			}

			result = (result * 10) + (digitsSimple[currentLocation.y][currentLocation.x]);
			++currentDigit;
		}

		return result;
	}

	static char digitsComplex[5][5] = { // '0's are just placeholders, there are no buttons labled 0
		{ '0', '0', '1', '0', '0' },
		{ '0', '2', '3', '4', '0' },
		{ '5', '6', '7', '8', '9' },
		{ '0', 'A', 'B', 'C', '0' },
		{ '0', '0', 'D', '0', '0' },
	};

	bool ComplexSpotAvailable(v2i spot)
	{
		switch (spot.y)
		{
		case -1:
			return false;
		case 0:
			return spot.x == 2;
			break;
		case 1:
			return spot.x >= 1 && spot.x <= 3;
			break;
		case 2:
			return spot.x >= 0 && spot.x <= 4;
			break;
		case 3:
			return spot.x >= 1 && spot.x <= 3;
			break;
		case 4:
			return spot.x == 2;
			break;
		case 5:
		default:
			return false;
		}

		return true;
	}

	std::string GetKeyCodeComplex(const std::string& path)
	{
		std::vector<std::string> values = Split(path);
		std::string result;
		int currentDigit = 0;

		v2i currentLocation = { 0, 2 };
		for (size_t i = 0; i < values.size(); i++)
		{
			for (size_t j = 0; j < values[i].length(); j++)
			{
				const char currentMove = values[i].at(j);
				switch (currentMove)
				{
				case 'R':
					if (ComplexSpotAvailable(currentLocation + v2i(1, 0))) currentLocation.x++;
					break;
				case 'D':
					if (ComplexSpotAvailable(currentLocation + v2i(0, 1))) currentLocation.y++;
					break;
				case 'L':
					if (ComplexSpotAvailable(currentLocation + v2i(-1, 0))) currentLocation.x--;
					break;
				case 'U':
					if (ComplexSpotAvailable(currentLocation + v2i(0, -1))) currentLocation.y--;
					break;
				}
			}

			result += (digitsComplex[currentLocation.y][currentLocation.x]);
			++currentDigit;
		}

		return result;
	}

	void Day2()
	{
		std::cout << "Day 2:" << std::endl;

		std::string input;
		if (ReadFile(input, "input/Day2Input.txt"))
		{
			int keycode = GetKeyCodeSimple(input);
			std::cout << "Simple keycode: " << keycode << std::endl;

			std::string complexKeyCode = GetKeyCodeComplex(input);
			std::cout << "Complex keycode: " << complexKeyCode << std::endl;
		}

		std::cout << std::endl;
	}
}
