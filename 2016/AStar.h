#pragma once

#include "CommonFunctions.h"

#include <math.h>
#include <queue>
#include <time.h>
#include <iostream>
#include <vector>

// Taken almost entirely from http://code.activestate.com/recipes/577457-a-star-shortest-path-algorithm/

namespace AStar
{
	const int dir = 4;
	static int dx[dir] = { 1, 0, -1, 0 };
	static int dy[dir] = { 0, 1, 0, -1 };

	struct Node
	{
		Node(v2i position, int level, int priority) :
			pos(position), level(level), priority(priority)
		{}

		void UpdatePriority(v2i dest)
		{
			priority = level + Estimate(dest) * 10;
		}

		void NextLevel(int i)
		{
			level += (dir == 8 ? (i % 2 == 0 ? 10 : 14) : 10);
		}

		int Estimate(v2i dest)
		{
			static int xd = dest.x - pos.x;
			static int yd = dest.y - pos.y;

			// Euclidian distance
			return int(sqrt(xd * xd + yd * yd));
		}

		v2i pos;
		int level; // Distance already travelled to reach this node
		int priority;  // Smaller: higher priority
	};

	bool operator<(const Node& lhs, const Node& rhs)
	{
		return lhs.priority > rhs.priority;
	}

	std::string FindPath(const std::vector<std::vector<int>>& map, v2i startPos, v2i endPos)
	{
		std::vector<std::vector<int>> openNodesMap;
		std::vector<std::vector<int>> closedNodesMap;
		std::vector<std::vector<int>> directionMap;

		const size_t mapHeight = map.size();
		const size_t mapWidth = map[0].size();

		// Initialze all vectors with 0s
		openNodesMap.resize(mapHeight);
		closedNodesMap.resize(mapHeight);
		directionMap.resize(mapHeight);
		for (size_t y = 0; y < mapHeight; y++)
		{
			openNodesMap[y].resize(mapWidth, 0);
			closedNodesMap[y].resize(mapWidth, 0);
			directionMap[y].resize(mapWidth, 0);
		}

		std::priority_queue<Node> priorityQueue[2]; // Open (not-tried) Nodes
		int priorityQueueIndex = 0;
		Node* n0;
		Node* m0;

		// Create the start node and push into list of open nodes
		n0 = new Node(startPos, 0, 0);
		n0->UpdatePriority(endPos);
		priorityQueue[priorityQueueIndex].push(*n0);
		openNodesMap[startPos.y][startPos.x] = n0->priority; // Mark it on the open nodes map

		// A* search
		while (!priorityQueue[priorityQueueIndex].empty())
		{
			// Get the current node w/ the highest priority
			// from the list of open nodes
			n0 = new Node(priorityQueue[priorityQueueIndex].top().pos,
				priorityQueue[priorityQueueIndex].top().level, priorityQueue[priorityQueueIndex].top().priority);

			int x = n0->pos.x;
			int y = n0->pos.y;

			priorityQueue[priorityQueueIndex].pop(); // Remove the node from the open list
			openNodesMap[y][x] = 0;
			// Mark it on the closed nodes map
			closedNodesMap[y][x] = 1;

			// Quit searching when the goal state is reached
			if (x == endPos.x && y == endPos.y)
			{
				// Generate the path from finish to start
				// by following the directions
				std::string path = "";
				while (!(x == startPos.x && y == startPos.y))
				{
					int j = directionMap[y][x];
					char c = '0' + (j + dir / 2) % dir;
					path = c + path;
					x += dx[j];
					y += dy[j];
				}

				delete n0;

				// Empty the leftover nodes
				while (!priorityQueue[priorityQueueIndex].empty())
					priorityQueue[priorityQueueIndex].pop();
				return path;
			}

			// Generate moves (child nodes) in all possible directions
			for (int i = 0; i<dir; i++)
			{
				int xdx = x + dx[i];
				int ydy = y + dy[i];

				if (xdx >= 0 && xdx < int(mapWidth) && ydy >= 0 && ydy < int(mapHeight) && map[ydy][xdx] != 1 && closedNodesMap[ydy][xdx] != 1)
				{
					// Generate a child node
					m0 = new Node(v2i(xdx, ydy), n0->level, n0->priority);
					m0->NextLevel(i);
					m0->UpdatePriority(endPos);

					// If it is not in the open list then add it
					if (openNodesMap[ydy][xdx] == 0)
					{
						openNodesMap[ydy][xdx] = m0->priority;
						priorityQueue[priorityQueueIndex].push(*m0);
						// Point at the node's parent
						directionMap[ydy][xdx] = (i + dir / 2) % dir;
					}
					else if (openNodesMap[ydy][xdx]>m0->priority)
					{
						// Update the priority info
						openNodesMap[ydy][xdx] = m0->priority;
						// Point at the node's parent
						directionMap[ydy][xdx] = (i + dir / 2) % dir;

						// Empty one queue into the other one except for the current node
						while (!(priorityQueue[priorityQueueIndex].top().pos.x == xdx &&
							priorityQueue[priorityQueueIndex].top().pos.y == ydy))
						{
							priorityQueue[1 - priorityQueueIndex].push(priorityQueue[priorityQueueIndex].top());
							priorityQueue[priorityQueueIndex].pop();
						}
						priorityQueue[priorityQueueIndex].pop(); // Remove the wanted node

						// Empty the larger size pq to the smaller one
						if (priorityQueue[priorityQueueIndex].size()>priorityQueue[1 - priorityQueueIndex].size()) priorityQueueIndex = 1 - priorityQueueIndex;
						while (!priorityQueue[priorityQueueIndex].empty())
						{
							priorityQueue[1 - priorityQueueIndex].push(priorityQueue[priorityQueueIndex].top());
							priorityQueue[priorityQueueIndex].pop();
						}
						priorityQueueIndex = 1 - priorityQueueIndex;
						priorityQueue[priorityQueueIndex].push(*m0); // Add the better node instead
					}
					else
					{
						delete m0;
					}
				}
			}
			delete n0;
		}

		return ""; // No route found
	}

} // namespace AStar
