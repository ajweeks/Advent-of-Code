#pragma once

#include "CommonFunctions.h"

// --- Day 16: Dragon Checksum ---

namespace Day16
{
	std::string CalculateChecksum(const std::vector<int>& data, int diskSize)
	{
		std::vector<int> newData(data.begin(), data.end());

		while (newData.size() < diskSize)
		{
			std::vector<int> copy(newData.begin(), newData.end());
			std::reverse(copy.begin(), copy.end());
			std::for_each(copy.begin(), copy.end(), [](int& val) { val = 1 - val; });

			newData.reserve(newData.size() * 2 + 1);
			newData.push_back(0);
			newData.insert(newData.end(), copy.begin(), copy.end());
		}

		std::vector<int> checksum(newData.begin(), newData.begin() + diskSize);
		bool evenLength = true;

		while (evenLength)
		{
			std::vector<int> oldChecksum(checksum.begin(), checksum.end());
			checksum.clear();

			for (size_t i = 0; i < oldChecksum.size() - 1; i += 2)
			{
				int match = (oldChecksum[i] == oldChecksum[i + 1] ? 1 : 0);
				checksum.push_back(match);
			}

			evenLength = checksum.size() % 2 == 0;
		}

		std::string checksumString;
		checksumString.reserve(checksum.size());
		for (size_t i = 0; i < checksum.size(); i++)
		{
			checksumString.push_back(checksum[i] == 0 ? '0' : '1');
		}
		return checksumString;
	}

	void Day16()
	{
		std::cout << "Day 16: " << std::endl;

		bool part2 = false;

		std::string fileString;
		if (ReadFile(fileString, "input/Day16Input.txt"))
		{
			int diskSize = 272;

			if (part2)
			{
				diskSize = 35651584;
			}

			std::vector<int> data;
			data.reserve(fileString.size());
			for (size_t i = 0; i < fileString.size(); i++)
			{
				if (fileString[i] != '1' && fileString[i] != '0') continue;
				data.push_back(fileString[i] == '0' ? 0 : 1);
			}
			std::string checksum = CalculateChecksum(data, diskSize);

			std::cout << "Checksum with disk size " << diskSize << ": " << checksum << std::endl;
		}
	
		std::cout << std::endl;
	}
}