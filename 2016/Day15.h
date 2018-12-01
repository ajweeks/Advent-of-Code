#pragma once

#include "CommonFunctions.h"

//--- Day 15: Timing is Everything ---

namespace Day15
{
	
	struct Disc
	{
		int numPos;
		int posAtTime0;
	};

	int FirstTimeToGetCapsule(const std::vector<Disc>& discs)
	{
		int startingTime = 0;

		while (true)
		{
			int currentTime = startingTime;
			bool validTime = true; // True if capsule falls through all discs
			for (size_t i = 0; i < discs.size(); i++)
			{
				++currentTime;
				if (((discs[i].posAtTime0 + currentTime) % discs[i].numPos) != 0)
				{
					validTime = false;
					break;
				}
			}
			if (validTime) return startingTime;
			++startingTime;
		}
	}

	void Day15()
	{
		std::cout << "Day 15: " << std::endl;
		
		bool part2 = true;

		std::string fileString;
		if (ReadFile(fileString, "input/Day15Input.txt"))
		{
			// Useless characters
			RemoveCharFromString(fileString, '.');
			RemoveCharFromString(fileString, ',');
			RemoveCharFromString(fileString, '#');
			RemoveCharFromString(fileString, ';');

			std::vector<std::string> fileLines = Split(fileString);
			std::vector<Disc> discs;

			for (size_t i = 0; i < fileLines.size(); i++)
			{
				Disc disc = {};
				std::vector<std::string> discStrLineParts = Split(fileLines[i], ' ');

				disc.numPos = stoi(discStrLineParts[3]);
				disc.posAtTime0 = stoi(discStrLineParts[11]);

				discs.push_back(disc);
			}

			if (part2) discs.push_back({ 11, 0 });

			int firstButtonPress = FirstTimeToGetCapsule(discs);
			std::cout << "First second you can press the button at to retrieve capsule: " << firstButtonPress << std::endl;

		}
	
		std::cout << std::endl;
	}
}