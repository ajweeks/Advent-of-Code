#pragma once

#include "CommonFunctions.h"
#include "AStar.h"

#include <Windows.h>
#include <bitset>

//--- Day 13: A Maze of Twisty Little Cubicles ---

namespace Day13
{
	struct Board
	{
		int favoriteNumber;
		std::vector<v2i> stepsTaken;
		v2i maxCoord;
	};

	// Returns how many high bits there are in the binary representation
	// of the specified number
	int NumHighBits(int number)
	{
		int numHighBits = 0;
		for (int i = 0; i < 32; i++)
		{
			if (number & (1 << i)) ++numHighBits;
		}
		return numHighBits;
	}

	bool IsCoordWall(v2i coord, int favoriteNumber)
	{
		if (coord.x < 0 || coord.y < 0) return true; // Invalid positions

		int n = coord.x * coord.x + 3 * coord.x + 2 * coord.x * coord.y + coord.y + coord.y * coord.y + favoriteNumber;
		return NumHighBits(n) % 2 == 1;
	}

	void PrintBoard(const Board& board)
	{
		static const char wall = '#';
		static const char hall = '.';
		static const char step = 'O';

		HANDLE hCon = GetStdHandle(STD_OUTPUT_HANDLE);

		int width = board.maxCoord.x + 2;
		int height = board.maxCoord.y + 2;

		std::cout << "  ";
		SetConsoleTextAttribute(hCon, 0x0F);
		for (int x = 0; x < width; x++) std::cout << (x % 10);
		std::cout << std::endl;

		for (int y = 0; y < height; y++)
		{
			SetConsoleTextAttribute(hCon, 0x0F);
			std::cout << y << " ";

			for (int x = 0; x < width; x++)
			{
				bool stepTaken = false;
				for (size_t i = 0; i < board.stepsTaken.size(); i++)
				{
					if (board.stepsTaken[i] == v2i(x, y))
					{
						stepTaken = true;
						break;
					}
				}

				if (stepTaken) 
				{
					SetConsoleTextAttribute(hCon, 0x0E);
					std::cout << step;
				}
				else
				{
					bool isWall = IsCoordWall(v2i(x, y), board.favoriteNumber);
					if (isWall) 
					{
						SetConsoleTextAttribute(hCon, 0x03);
						std::cout << wall;
					}
					else 
					{
						SetConsoleTextAttribute(hCon, 0x09);
						std::cout << hall;
					}
				}
			}

			std::cout << std::endl;
		}
		SetConsoleTextAttribute(hCon, 0x0F);
		std::cout << std::endl;
	}

	v2i FindMaxCoord(const std::vector<v2i> vec)
	{
		v2i maxCoord = { 0, 0 };

		for (size_t i = 0; i < vec.size(); i++)
		{
			maxCoord.x = max(vec[i].x, maxCoord.x);
			maxCoord.y = max(vec[i].y, maxCoord.y);
		}

		return maxCoord;
	}

	// Tries moving all four cardinal directions
	void ShortestPathRecursive(Board board, v2i currentLocation, v2i destination, int& shortestPathSoFar, 
		int maxPathDist, bool printOutput)
	{
		if (IsCoordWall(currentLocation, board.favoriteNumber)) return;

		board.stepsTaken.push_back(currentLocation);
		if (ContainsDuplicates(board.stepsTaken)) return; // We've already been to this location before

		// Number of steps - 1 because we don't count the starting location
		int stepsTaken = int(board.stepsTaken.size()) - 1;
		if (stepsTaken > shortestPathSoFar || stepsTaken > maxPathDist) return;

		board.maxCoord = FindMaxCoord(board.stepsTaken);
		if (currentLocation == destination) // We made it!
		{
			if (stepsTaken < shortestPathSoFar)
			{
				shortestPathSoFar = stepsTaken;
				if (printOutput)
				{
					//system("cls");
					std::cout << "Found shorter solution: " << std::endl;
					PrintBoard(board);
					std::cout << "Number of steps taken: " << stepsTaken << std::endl;
				}
			}
			return;
		}

		if (destination.x > 0 && destination.y > 0 &&
			(currentLocation.x > destination.x * 2 || 
			currentLocation.y > destination.y * 2)) return; // Don't try ridiculous solutions

		ShortestPathRecursive(board, currentLocation + v2i(1, 0), destination, shortestPathSoFar, maxPathDist, printOutput);
		ShortestPathRecursive(board, currentLocation + v2i(-1, 0), destination, shortestPathSoFar, maxPathDist, printOutput);
		ShortestPathRecursive(board, currentLocation + v2i(0, 1), destination, shortestPathSoFar, maxPathDist, printOutput);
		ShortestPathRecursive(board, currentLocation + v2i(0, -1), destination, shortestPathSoFar, maxPathDist, printOutput);
	}

	int ShortestRouteLength(Board board, v2i start, v2i end, int maxPathDist, bool printOutput)
	{
		int shortestPath = INT_MAX;
		ShortestPathRecursive(board, start, end, shortestPath, maxPathDist, printOutput);

		return shortestPath;
	}

	// Checks the area surrounding the starting location to see which spots are reachable in given steps
	// Returns num locations reachable
	int LocationsReachable(Board& board, v2i startingLocation, int maxSteps)
	{
		if (IsCoordWall(startingLocation, board.favoriteNumber) ||
			startingLocation.x < 0 || startingLocation.y < 0) return 0; // Invalid starting location

		int locationsReachable = 1; // Include starting location

		// The minimum possible x, y that is reachable in given steps
		v2i minCoord = v2i(startingLocation.x - maxSteps, startingLocation.y - maxSteps); 
		if (minCoord.x < 0) minCoord.x = 0;
		if (minCoord.y < 0) minCoord.y = 0;
		v2i maxCoord = v2i(startingLocation.x + maxSteps, startingLocation.y + maxSteps);

		std::vector<v2i> stepsTaken;
		stepsTaken.push_back(startingLocation);

		std::vector<std::vector<int>> boardTiles;
		boardTiles.reserve(maxCoord.y - minCoord.y);
		for (int y = minCoord.y; y < maxCoord.y; y++)
		{
			boardTiles.push_back({});
			boardTiles[y].reserve(maxCoord.x - minCoord.x);
			for (int x = minCoord.x; x < maxCoord.x; x++)
			{
				boardTiles[y].push_back(IsCoordWall({ x, y }, board.favoriteNumber) ? 1 : 0);
			}
		}

		// Start in top left corner and iterate through all tiles row by row
		for (int y = minCoord.y; y < maxCoord.y; y++)
		{
			for (int x = minCoord.x; x < maxCoord.x; x++)
			{
				const v2i currentLocation = v2i(x, y);
				if (boardTiles[y][x] == 0)
				{
					// Check if this tile is reachable in given steps from start location
					std::string path = AStar::FindPath(boardTiles, startingLocation, currentLocation);
					int shortestRouteLength = int(path.length());
					if (!path.empty() && shortestRouteLength <= maxSteps)
					{
						stepsTaken.push_back(currentLocation);
						++locationsReachable;
					}
				}
			}
		}
		
		board.stepsTaken = stepsTaken;
		board.maxCoord = FindMaxCoord(stepsTaken);
		PrintBoard(board);

		return locationsReachable;
	}

	void Day13()
	{
		std::cout << "Day 13: " << std::endl;

		std::string fileString;
		if (ReadFile(fileString, "input/Day13Input.txt"))
		{
			Board board = {};
			board.favoriteNumber = stoi(fileString);
			
			bool part1 = false;
			bool part2 = true;

			if (part1)
			{
				v2i start = { 1, 1 };
				v2i end = { 31, 39 };
				int shortestPath = ShortestRouteLength(board, start, end, INT_MAX, true);
				PrintBoard(board);
				std::cout << "Shortest path from " << start << " to " << end << ": " << shortestPath << std::endl;;
			}
			
			if (part2)
			{
				std::vector<v2i> locations;
				v2i start = { 1, 1 };
				int maxSteps = 50;
				int reachable = LocationsReachable(board, start, maxSteps);

				std::cout << "Number of locations reachable in " << maxSteps << " steps: " << reachable << std::endl;
			}
		}
	
		std::cout << std::endl;
	}
}