#pragma once

#include "CommonFunctions.h"
#include "MD5.h"
#include <climits>

//--- Day 5: How About a Nice Game of Chess? ---

// TODO: Remove _CRT_SECURE_NO_WARNINGS from preprocessor warnings and use sprintf_s instead
namespace Day5
{
	std::string Part1(const std::string& doorID)
	{
		std::string password;
		long long index = 0;
		bool running = true;
		while (running)
		{
			std::string stringToHash = doorID + std::to_string(index);
			std::string hash = md5(stringToHash);
			if (hash[0] == '0' &&
				hash[1] == '0' &&
				hash[2] == '0' &&
				hash[3] == '0' &&
				hash[4] == '0')
			{
				password.push_back(hash.at(5));

				if (password.length() == 8) running = false;
			}

			assert(index < LLONG_MAX - 1);
			++index;
		}

		return password;
	}

	std::string Part2(const std::string& doorID)
	{
		std::string password(8, '_');
		long long index = 0;
		bool running = true;
		while (running)
		{
			std::string stringToHash = doorID + std::to_string(index);
			std::string hash = md5(stringToHash);
			if (hash[0] == '0' &&
				hash[1] == '0' &&
				hash[2] == '0' &&
				hash[3] == '0' &&
				hash[4] == '0')
			{
				int location = (hash.at(5) - '0');
				if (location >= 0 && location <= 7 &&
					password[location] == '_')
				{
					password[location] = hash.at(6);

					if (password[0] != '_' &&
						password[1] != '_' &&
						password[2] != '_' &&
						password[3] != '_' &&
						password[4] != '_' &&
						password[5] != '_' &&
						password[6] != '_' &&
						password[7] != '_') running = false;
				}
			}

			assert(index < LLONG_MAX - 1);
			++index;
		}

		return password;
	}

	void Day5()
	{
		std::cout << "Day 5: " << std::endl;

		bool calculatePart1 = false;
		bool calculatePart2 = false;

		std::string doorID;
		if (ReadFile(doorID, "input/Day5Input.txt"))
		{
			doorID = Split(doorID)[0];
			
			if (calculatePart1)
			{
				std::string password = Part1(doorID);
				std::cout << "Password of " << doorID << ": " << password << std::endl;
			}
			else
			{
				std::cout << "Not calculating part 1" << std::endl;
			}			
			
			if (calculatePart2)
			{
				std::string password = Part2(doorID);
				std::cout << "Password of " << doorID << ": " << password << std::endl;
			}
			else
			{
				std::cout << "Not calculating part 2" << std::endl;
			}
		}

		std::cout << std::endl;
	}
}