#pragma once

#include "CommonFunctions.h"

//--- Day 6: Signals and Noise ---

namespace Day6
{
	void Day6()
	{
		std::cout << "Day 6: " << std::endl;

		std::string input;
		if (ReadFile(input, "input/Day6Input.txt"))
		{
			std::vector<std::string> inputRows = Split(input);
			std::vector<std::string> inputColumns;
			inputColumns.resize(inputRows[0].size());
			for (size_t i = 0; i < inputRows.size(); i++)
			{
				for (size_t j = 0; j < inputColumns.size(); j++)
				{
					inputColumns[j].push_back(inputRows[i][j]);
				}
			}

			std::string mostCommonLetters;
			std::string leastCommonLetters;
			for (size_t i = 0; i < inputColumns.size(); i++)
			{
				std::vector<std::pair<int, int>> letterCount; // first int is the count, second int is the letter index (a = 0)
				for (size_t j = 0; j < 26; j++)
				{
					letterCount.push_back({ 0, j });
				}
				for (size_t j = 0; j < inputColumns[i].length(); j++)
				{
					++letterCount[inputColumns[i].at(j) - 'a'].first;
				}

				std::sort(letterCount.begin(), letterCount.end(),
					[](const std::pair<int, int>& a, const std::pair<int, int>& b)
				{
					if (a.first == b.first) return a.second > b.second; // Sort alphabetically if the letters have the same count
					else return a.first < b.first;
				});

				mostCommonLetters.push_back(char(letterCount.at(letterCount.size() - 1).second + 'a'));
				leastCommonLetters.push_back(char(letterCount.at(0).second + 'a'));
			}
			
			std::cout << "Most common letters: " << mostCommonLetters << std::endl;
			std::cout << "Least common letters: " << leastCommonLetters << std::endl;
		}

		std::cout << std::endl;
	}
}