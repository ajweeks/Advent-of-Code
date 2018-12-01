#pragma once

#include "CommonFunctions.h"

#include "MD5.h"

#include <queue>

// --- Day 17: Two Steps Forward ---

namespace Day17
{
	std::string s_ShortestPath;
	size_t s_LongestPathSteps = 0;

	bool DoorOpen(char character)
	{
		return (character >= 'b' && character <= 'f');
	}

	struct PathInfo
	{
		v2i room;
		std::string pathTaken;
	};

	void FindLongestPathLength(const std::string& passcode)
	{
		std::queue<PathInfo> roomsToEnter;
		roomsToEnter.push({ { 0, 0 }, "" });

		while (!roomsToEnter.empty())
		{
			PathInfo currentPath = roomsToEnter.front();
			roomsToEnter.pop();

			if (currentPath.room.x == 3 && currentPath.room.y == 3)
			{
				if (currentPath.pathTaken.size() > s_LongestPathSteps)
				{
					s_LongestPathSteps = currentPath.pathTaken.size();
				}

				continue;
			}

			std::string totalString = passcode + currentPath.pathTaken;

			std::string hash = md5(totalString);
			// up, down, left, right
			bool openDoors[4] = { DoorOpen(hash[0]), DoorOpen(hash[1]), DoorOpen(hash[2]), DoorOpen(hash[3]) };
			if (currentPath.room.x == 0) openDoors[2] = false;
			if (currentPath.room.x == 3) openDoors[3] = false;
			if (currentPath.room.y == 0) openDoors[0] = false;
			if (currentPath.room.y == 3) openDoors[1] = false;

			if (openDoors[0]) roomsToEnter.push({ currentPath.room + v2i(0, -1), currentPath.pathTaken + "U" });
			if (openDoors[1]) roomsToEnter.push({ currentPath.room + v2i(0, 1), currentPath.pathTaken + "D" });
			if (openDoors[2]) roomsToEnter.push({ currentPath.room + v2i(-1, 0), currentPath.pathTaken + "L" });
			if (openDoors[3]) roomsToEnter.push({ currentPath.room + v2i(1, 0), currentPath.pathTaken + "R" });
		}
	}

	void EnterDoorRecursive(const v2i& currentLocation, const std::string& currentPath, const std::string& passcode)
	{
		if (!s_ShortestPath.empty() && currentPath.size() >= s_ShortestPath.size()) return;

		if (currentLocation.x == 3 && currentLocation.y == 3)
		{
			s_ShortestPath = currentPath;

			return;
		}

		std::string totalString = passcode + currentPath;

		std::string hash = md5(totalString);
		// up, down, left, right
		bool openDoors[4] = { DoorOpen(hash[0]), DoorOpen(hash[1]), DoorOpen(hash[2]), DoorOpen(hash[3]) };
		if (currentLocation.x == 0) openDoors[2] = false;
		if (currentLocation.x == 3) openDoors[3] = false;
		if (currentLocation.y == 0) openDoors[0] = false;
		if (currentLocation.y == 3) openDoors[1] = false;

		if (openDoors[0]) EnterDoorRecursive(currentLocation + v2i(0, -1), currentPath + "U", passcode);
		if (openDoors[1]) EnterDoorRecursive(currentLocation + v2i(0, 1), currentPath + "D", passcode);
		if (openDoors[2]) EnterDoorRecursive(currentLocation + v2i(-1, 0), currentPath + "L", passcode);
		if (openDoors[3]) EnterDoorRecursive(currentLocation + v2i(1, 0), currentPath + "R", passcode);
	}

	void FindShortestPath(const std::string& passcode)
	{
		std::string shortestPath;
		v2i startingLocation = { 0, 0 };

		EnterDoorRecursive(startingLocation, shortestPath, passcode);
	}

	void Day17()
	{
		std::cout << "Day 17: " << std::endl;

		bool part1 = true;
		bool part2 = true;

		std::string fileString;
		if (ReadFile(fileString, "input/Day17Input.txt"))
		{
			std::string passcode = fileString;
			RemoveCharFromString(passcode, '\n');

			if (part1)
			{
				FindShortestPath(passcode);
				std::cout << "Shortest path: " << s_ShortestPath << std::endl;
			}

			if (part2)
			{
				FindLongestPathLength(passcode);
				std::cout << "Longest path length: " << s_LongestPathSteps << std::endl;
			}
		}
	
		std::cout << std::endl;
	}
}