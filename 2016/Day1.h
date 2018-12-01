#pragma once

#include "CommonFunctions.h"

#include <vector>
#include <string>
#include <assert.h>
#include <iostream>
#include <algorithm>

//--- Day 1: No Time for a Taxicab ---
namespace Day1
{
	enum Direction
	{
		EAST, SOUTH, WEST, NORTH,

		_LAST
	};

	struct DistanceInfo
	{
		int displacement = -1;
		int displacementOfFirstBlockTouchedTwice = -1;
	};

	DistanceInfo GetDistanceToDestination(const std::string& directions)
	{
		DistanceInfo info = {};

		std::vector<v2i> visitedLocations;

		int dirFacing = Direction::NORTH;
		v2i ourPos = {};
		visitedLocations.push_back(ourPos);

		std::vector<std::string> inputVec = Split(directions, ',');
		for (size_t i = 0; i < inputVec.size(); i++)
		{
			RemoveSpaces(inputVec[i]);
			const char turnDir = inputVec[i].at(0);
			const int dist = stoi(inputVec[i].substr(1));
			if (turnDir == 'R')
			{
				++dirFacing;
				if (dirFacing == Direction::_LAST) dirFacing = Direction::EAST;
			}
			else if (turnDir == 'L')
			{
				--dirFacing;
				if (dirFacing < 0) dirFacing = Direction::_LAST - 1;
			}

			for (int i = 0; i < dist; i++)
			{
				switch (dirFacing)
				{
				case Direction::EAST:
					ourPos.x += 1;
					break;
				case Direction::SOUTH:
					ourPos.y -= 1;
					break;
				case Direction::WEST:
					ourPos.x -= 1;
					break;
				case Direction::NORTH:
					ourPos.y += 1;
					break;
				}

				if (info.displacementOfFirstBlockTouchedTwice == -1) // We haven't touched a block twice yet
				{
					bool visited = false;
					for (size_t i = 0; i < visitedLocations.size(); i++)
					{
						if (visitedLocations[i] == ourPos)
						{
							info.displacementOfFirstBlockTouchedTwice = abs(ourPos.x) + abs(ourPos.y);
							visited = true;
						}
					}
					if (!visited)
					{
						visitedLocations.push_back(ourPos);
					}
				}
			}
		}

		info.displacement = abs(ourPos.x) + abs(ourPos.y);

		return info;
	}

	void Day1()
	{
		std::cout << "Day 1:" << std::endl;

		std::string input;
		if (ReadFile(input, "input/Day1Input.txt"))
		{
			DistanceInfo displacement = GetDistanceToDestination(input);
			std::cout << "Displacement: " << displacement.displacement << std::endl;
			std::cout << "First block touched twice displacement: "	<< displacement.displacementOfFirstBlockTouchedTwice << std::endl;
		}

		std::cout << std::endl;
	}
}