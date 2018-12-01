#pragma once

#include "CommonFunctions.h"

//--- Day 14: One-Time Pad ---

namespace Day14
{

	std::string GetHashV2(size_t index, const std::string& salt, std::vector<std::string>& hashes)
	{
		if (int(index) > int(hashes.size()) - 1)
		{
			for (size_t i = hashes.size(); i <= index; i++)
			{
				std::string key = salt + std::to_string(i);
				std::string hash = md5(key);
				for (size_t j = 0; j < 2016; j++)
				{
					hash = md5(hash);
				}

				hashes.push_back(hash);
			}
		}

		return hashes[index];
	}


	std::string GetHash(size_t index, const std::string& salt, std::vector<std::string>& hashes)
	{
		if (int(index) > int(hashes.size()) - 1)
		{
			for (size_t i = hashes.size(); i <= index; i++)
			{
				hashes.push_back(md5(salt + std::to_string(i)));
			}
		}

		return hashes[index];
	}

	// Returns ! on failure
	char FirstRepeatedChar(const std::string str, int numRepeated, char c = '!')
	{
		if (numRepeated > int(str.length())) return '!';

		bool repeating = false;
		for (int i = 0; i < int(str.length() - numRepeated + 1); i++)
		{
			if (c != '!' && str[i] != c) continue; // The user specified a specific char, and this isn't it

			bool validSequence = true;
			for (int j = 0; j < numRepeated - 1; j++)
			{
				if (str[i + j] != str[i + j + 1]) 
				{
					validSequence = false;
					break;
				}
			}

			if (validSequence)
			{
				return str[i];
			}
		}

		return '!';
	}

	void Day14()
	{
		std::cout << "Day 14: " << std::endl;

		std::string fileString;
		if (ReadFile(fileString, "input/Day14Input.txt"))
		{
			std::string salt = fileString;
			RemoveCharFromString(salt, '\n');

			bool part2 = true;
			auto getHashFunc = (part2 ? GetHashV2 : GetHash);

			// Index/hash pairs
			std::vector<std::pair<int, std::string>> keys;
			std::vector<std::string> hashes;
			int index = 0;

			std::cout << "Using salt " << salt << std::endl;

			while (keys.size() < 64)
			{
				std::string hash = getHashFunc(index, salt, hashes);
				char tripletChar = FirstRepeatedChar(hash, 3);

				bool containsTriplet = (tripletChar != '!');
				if (containsTriplet)
				{
					bool nextHashesContainFive = false;
				
					for (int i = index + 1; i < index + 1000; i++)
					{
						std::string cmpHash = getHashFunc(i, salt, hashes);
						char firstRepeatedChar = FirstRepeatedChar(cmpHash, 5, tripletChar);
						if (firstRepeatedChar != '!')
						{
							nextHashesContainFive = true;
							break;
						}
					}

					if (nextHashesContainFive)
					{
						keys.push_back(std::pair<int, std::string>(index, hash));
						std::cout << "Keys size " << keys.size() << std::endl;
					}
				}

				++index;
			}

			std::cout << "Hash which produced 64th key: " << keys[keys.size() - 1].first << " "
				<< keys[keys.size() - 1].second << std::endl;

		}
	
		std::cout << std::endl;
	}
}