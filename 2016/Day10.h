#pragma once

#include "CommonFunctions.h"

#include <assert.h>

//--- Day 10: Balance Bots ---

namespace Day10
{

	struct Bot
	{
		Bot() {};
		Bot(int index, int low, int high) : index(index), low(low), high(high) {}
		
		void AddValue(int value)
		{
			assert(high == -1); // If high != -1 then we already have two values

			if (low == -1)
			{
				low = value;
			}
			else if (value >= low)
			{
				high = value;
			}
			else
			{
				high = low;
				low = value;
			}

			if (low == 17 && high == 61) std::cout << "Bot which compares chip 61 with chip 17: " << index << std::endl;
		}
		
		int index = -1;
		int low = -1;
		int high = -1;
	};

	void Day10()
	{
		std::cout << "Day 10: " << std::endl;

		std::string fileString;
		if (ReadFile(fileString, "input/Day10Input.txt"))
		{
			std::vector<std::string> commands = Split(fileString);
			std::vector<Bot> bots;
			std::vector<int> outputs;

			typedef std::vector<std::string>::iterator commandIterator;
			// Apply then remove all initialize commands (value x goes to bot y) from command vector
			for (commandIterator iter = commands.begin(); iter != commands.end();)
			{
				// Find all initializer commands
				std::string command = *iter;
				if (command.find("value") != std::string::npos)
				{
					std::vector<std::string> commandParts = Split(command, ' ');
					int value = stoi(commandParts[1]);
					int botIndex = stoi(commandParts[5]);

					if (botIndex + 1 > bots.size()) bots.resize(botIndex + 1);
					if (bots[botIndex].low == -1) // This bot hasn't been set yet
					{
						bots[botIndex] = Bot(botIndex, value, -1);
					}
					else // This bot has already been set (hopefully only once)
					{
						bots[botIndex].AddValue(value);
					}

					iter = commands.erase(iter);
				}
				else
				{
					++iter;
				}
			}

			for (int i = 0; i < bots.size(); i++)
			{
				bots[i].index = i;
			}

			bool changed = true;
			while (changed)
			{
				changed = false;
				// Apply all other commands (bot x gives low to x y and high to bot z)
				for (commandIterator iter = commands.begin(); iter != commands.end();)
				{
					std::vector<std::string> commandParts = Split(*iter, ' ');
					int botID = stoi(commandParts[1]);

					if (bots[botID].high != -1)
					{
						changed = true;
						if (commandParts[5].compare("output") == 0) // Give low value to output
						{
							size_t outputID = stoi(commandParts[6]);
							if (outputID + 1 > outputs.size()) outputs.resize(outputID + 1);
							assert(outputs[outputID] == 0);
							outputs[outputID] = bots[botID].low;
						}
						else // Give low value to bot
						{
							size_t lowBotID = stoi(commandParts[6]);
							bots[lowBotID].AddValue(bots[botID].low);
						}

						if (commandParts[10].compare("output") == 0) // Give high value to output
						{
							size_t outputID = stoi(commandParts[11]);
							if (outputID + 1 > outputs.size()) outputs.resize(outputID + 1);
							assert(outputs[outputID] == 0);
							outputs[outputID] = bots[botID].high;
						}
						else // Give high value to bot
						{
							int highBotID = stoi(commandParts[11]);
							bots[highBotID].AddValue(bots[botID].high);
						}

						iter = commands.erase(iter);
					}
					else
					{
						++iter;
					}
				}
			}

			std::cout << "Outputs 0, 1, 2: " << std::endl;
			for (size_t i = 0; i < 3; i++)
			{
				if (i > 0) std::cout << ", ";
				std::cout << outputs[i];
			}
			std::cout << std::endl;
		}

		std::cout << std::endl;
	}
}