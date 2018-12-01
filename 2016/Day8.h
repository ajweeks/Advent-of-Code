#pragma once

#include "CommonFunctions.h"

//--- Day 8: Two-Factor Authentication ---

namespace Day8
{

	void FillRect(std::vector<bool>& pixels, v2i screenDimensions, int width, int height)
	{
		assert(width <= screenDimensions.x);
		assert(height <= screenDimensions.y);

		for (int x = 0; x < width; x++)
		{
			for (int y = 0; y < height; y++)
			{
				const size_t index = y * screenDimensions.x + x;
				pixels[index] = true;
			}
		}
	}

	void RotateRow(std::vector<bool>& pixels, v2i screenDimensions, int rowIndex, int shiftAmount)
	{
		assert(rowIndex >= 0 && rowIndex < screenDimensions.y);

		size_t firstPixelIndex = rowIndex * screenDimensions.x;
		size_t lastPixelIndex = rowIndex * screenDimensions.x + screenDimensions.x - 1;

		std::vector<bool> oldValues(pixels);

		for (int x = 0; x < screenDimensions.x; x++)
		{
			int oldIndex = rowIndex * screenDimensions.x + x;
			int newIndex = oldIndex - shiftAmount;
			if (newIndex < (rowIndex * screenDimensions.x)) newIndex += screenDimensions.x;
			pixels[oldIndex] = oldValues[newIndex];
		}
	}

	void RotateCol(std::vector<bool>& pixels, v2i screenDimensions, int colIndex, int shiftAmount)
	{
		assert(colIndex >= 0 && colIndex < screenDimensions.x);

		size_t firstPixelIndex = colIndex;
		size_t lastPixelIndex = screenDimensions.x * screenDimensions.y + colIndex - (screenDimensions.x - colIndex);

		std::vector<bool> oldValues(pixels);

		for (int y = 0; y < screenDimensions.y; y++)
		{
			int oldIndex = y * screenDimensions.x + colIndex;
			int newIndex = oldIndex - shiftAmount * screenDimensions.x;
			if (newIndex < 0) newIndex += screenDimensions.x * screenDimensions.y;
			pixels[oldIndex] = oldValues[newIndex];
		}
	}

	void Day8()
	{
		std::cout << "Day 8: " << std::endl;

		std::string fileString;
		if (ReadFile(fileString, "input/Day8Input.txt"))
		{
			const v2i screenDimensions = { 50, 6 };
			std::vector<bool> screenPixels(screenDimensions.x * screenDimensions.y, false);

			std::vector<std::string> commands = Split(fileString);
			for (size_t i = 0; i < commands.size(); i++)
			{
				std::vector<std::string> commandParts = Split(commands[i], ' ');
				std::string command = commandParts[0];
				if (command.compare("rect") == 0)
				{
					std::string size = commandParts[1];
					std::vector<std::string> sizeParts = Split(size, 'x');
					int width = stoi(sizeParts[0]);
					int height = stoi(sizeParts[1]);

					FillRect(screenPixels, screenDimensions, width, height);
				}
				else if (command.compare("rotate") == 0)
				{
					std::string colOrRow = commandParts[1];
					if (colOrRow.compare("column") == 0)
					{
						int colIndex = stoi(commandParts[2].substr(2));
						int shiftAmount = stoi(commandParts[4]);

						RotateCol(screenPixels, screenDimensions, colIndex, shiftAmount);
					}
					else if (colOrRow.compare("row") == 0)
					{
						int rowIndex = stoi(commandParts[2].substr(2));
						int shiftAmount = stoi(commandParts[4]);

						RotateRow(screenPixels, screenDimensions, rowIndex, shiftAmount);
					}
					else
					{
						std::cout << "Inavlid command: " << commands[i] << std::endl;
					}
				}
				else 
				{
					std::cout << "Invalid command: " << command << std::endl;
				}

				std::cout << commands[i] << std::endl;
				for (int y = 0; y < screenDimensions.y; y++)
				{
					for (int x = 0; x < screenDimensions.x; x++)
					{
						size_t index = y * screenDimensions.x + x;
						std::cout << (screenPixels[index] ? '#' : '.') << ' ';
					}
					std::cout << std::endl;
				}
				std::cout << std::endl;
				//std::getchar();
			}

			int numPixelsLit = 0;
			for (size_t i = 0; i < screenPixels.size(); i++)
			{
				if (screenPixels[i]) ++numPixelsLit;
			}

			std::cout << "Number of lit pixels: " << numPixelsLit << std::endl;

		}

		std::cout << std::endl;
	}
}