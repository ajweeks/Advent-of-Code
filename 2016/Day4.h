#pragma once

#include "CommonFunctions.h"

//--- Day 4: Security Through Obscurity ---

namespace Day4
{
	struct Room
	{
		int sectorID;
		std::string name; // With dashes
		std::string decryptedName;
		std::string checksum;
	};

	char Shift(char input, int offset)
	{
		if (input == '-') return ' ';

		offset = offset % 26;
		int result = (input + offset);
		if (result > 'z') 
			result -= ('z' - 'a' + 1);

		return result;
	}

	std::string Shift(const std::string& str, int offset)
	{
		std::string result;
		result.reserve(str.size());
		for (size_t i = 0; i < str.length(); i++)
		{
			result.push_back(Shift(str.at(i), offset));
		}

		return result;
	}

	void Day4()
	{
		std::cout << "Day 4: " << std::endl;

		std::string fileString;
		ReadFile(fileString, "input/Day4Input.txt");
		std::vector<std::string> inputLines = Split(fileString);
		//std::vector<std::string> inputLines = { "aaaaa-bbb-z-y-x-123[abxyz]" };

		int realRoomSectorIDSum = 0;

		std::vector<Room> realRooms;

		for (size_t i = 0; i < inputLines.size(); i++)
		{
			size_t firstNum = inputLines[i].find_first_of("0123456789");
			size_t firstSquareBracket = inputLines[i].find('[', firstNum + 1);
			size_t lastSquareBracket = inputLines[i].find(']', firstSquareBracket + 1);
			assert(firstNum != std::string::npos);
			assert(firstSquareBracket != std::string::npos);
			assert(lastSquareBracket != std::string::npos);

			Room room = {};
			room.name = inputLines[i].substr(0, firstNum);
			std::string nameWithoutDashes = room.name;
			RemoveCharFromString(nameWithoutDashes, '-');
			std::sort(nameWithoutDashes.begin(), nameWithoutDashes.end());
			room.sectorID = stoi(inputLines[i].substr(firstNum, firstSquareBracket - firstNum));
			room.checksum = inputLines[i].substr(firstSquareBracket + 1, lastSquareBracket - firstSquareBracket - 1);

			std::vector<std::pair<int, int>> letterCount; // first int is the count, second int is the letter index (a = 0)
			for (size_t j = 0; j < 26; j++)
			{
				letterCount.push_back({ 0, j });
			}
			for (size_t j = 0; j < nameWithoutDashes.length(); j++)
			{
				++letterCount[nameWithoutDashes.at(j) - 'a'].first;
			}

			std::sort(letterCount.begin(), letterCount.end(), 
				[](const std::pair<int, int>& a, const std::pair<int, int>& b) 
			{
				if (a.first == b.first) return a.second > b.second; // Sort alphabetically if the letters have the same count
				else return a.first < b.first;
			});

			std::string calculatedChecksum; // five most common letters
			calculatedChecksum.push_back(letterCount.at(letterCount.size() - 1).second + 'a');
			calculatedChecksum.push_back(letterCount.at(letterCount.size() - 2).second + 'a');
			calculatedChecksum.push_back(letterCount.at(letterCount.size() - 3).second + 'a');
			calculatedChecksum.push_back(letterCount.at(letterCount.size() - 4).second + 'a');
			calculatedChecksum.push_back(letterCount.at(letterCount.size() - 5).second + 'a');

			if (calculatedChecksum.compare(room.checksum) == 0)
			{
				realRoomSectorIDSum += room.sectorID;
				realRooms.push_back(room);
			}
		}

		Room northPoleRoom = {};

		bool outputRoomNames = false;
		for (size_t i = 0; i < realRooms.size(); i++)
		{
			realRooms[i].decryptedName = Shift(realRooms[i].name, realRooms[i].sectorID);

			if (outputRoomNames)
			{
				std::cout << "Room with sector ID " << realRooms[i].sectorID << std::endl;
				std::cout << "Has an decrypted name \"" << realRooms[i].decryptedName << "\"" << std::endl << std::endl;
			}

			if (realRooms[i].decryptedName.find("northpole") != std::string::npos)
			{
				northPoleRoom = realRooms[i];
			}
		}

		std::cout << "Found real room with decrypted name \"" << northPoleRoom.decryptedName << "\""
			"and a sector id " << northPoleRoom.sectorID << std::endl;
		std::cout << "Number of real rooms: " << realRooms.size() << std::endl;
		std::cout << "Sum of sector ids of real rooms: " << realRoomSectorIDSum << std::endl;

		std::cout << std::endl;
	}
}
