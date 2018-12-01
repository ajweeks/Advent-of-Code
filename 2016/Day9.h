#pragma once

#include "CommonFunctions.h"

//--- Day 9: Explosives in Cyberspace ---

namespace Day9
{
	// Part 1
	std::string DecompressStringSimple(const std::string& compressedString)
	{
		std::string decompressedString;

		size_t currentIndex = 0;

		size_t openBracket = compressedString.find('(', currentIndex);
		size_t closeBracket = compressedString.find(')', openBracket + 1);
		if (openBracket == std::string::npos || closeBracket == std::string::npos)
		{
			decompressedString = compressedString;
		}
		else
		{
			while (openBracket != std::string::npos && closeBracket != std::string::npos)
			{
				decompressedString += compressedString.substr(currentIndex, openBracket - currentIndex);
				currentIndex = closeBracket + 1;
				std::vector<std::string> marker = Split(compressedString.substr(openBracket + 1, closeBracket - openBracket), 'x');
				int numChars = stoi(marker[0]);
				int numRepeated = stoi(marker[1]);

				std::string repeatedString = compressedString.substr(closeBracket + 1, numChars);
				for (int i = 0; i < numRepeated; i++)
				{
					decompressedString += repeatedString;
				}

				currentIndex += numChars;

				openBracket = compressedString.find('(', currentIndex);
				closeBracket = compressedString.find(')', openBracket + 1);
			}

			if (closeBracket != std::string::npos)
			{
				decompressedString += compressedString.substr(currentIndex);
			}

		}

		return decompressedString;
	}
	
	// Part 2
	long long DecompressedStringLengthComplex(const std::string& compressedString)
	{
		long long decompressedStringLength = 0;

		size_t currentIndex = 0;

		size_t openBracket = compressedString.find('(', currentIndex);
		size_t closeBracket = compressedString.find(')', openBracket + 1);
		if (openBracket == std::string::npos || closeBracket == std::string::npos)
		{
			decompressedStringLength = compressedString.length();
		}
		else
		{
			while (openBracket != std::string::npos && closeBracket != std::string::npos)
			{
				decompressedStringLength += (openBracket - currentIndex); // Add all the plain characters before the first bracket
				currentIndex = closeBracket + 1;
				std::vector<std::string> marker = Split(compressedString.substr(openBracket + 1, closeBracket - openBracket), 'x');
				int numChars = stoi(marker[0]);
				int numRepeated = stoi(marker[1]);

				std::string repeatedString = compressedString.substr(closeBracket + 1, numChars);

				decompressedStringLength += DecompressedStringLengthComplex(repeatedString) * numRepeated;

				currentIndex += numChars;

				openBracket = compressedString.find('(', currentIndex);
				closeBracket = compressedString.find(')', openBracket + 1);
			}

			if (closeBracket != std::string::npos)
			{
				decompressedStringLength += compressedString.length() - currentIndex;
			}
		}

		return decompressedStringLength;
	}

	void Day9()
	{
		std::cout << "Day 9: " << std::endl;

		std::string fileString;
		if (ReadFile(fileString, "input/Day9Input.txt"))
		{
			RemoveSpaces(fileString);

			std::string decompressedv1 = DecompressStringSimple(fileString);
			std::cout << "Final length of decompressed string using v1: " << decompressedv1.length() << std::endl;

			long long decompressedv2Len = DecompressedStringLengthComplex(fileString);
			std::cout << "Final length of decompressed string using v2: " << decompressedv2Len << std::endl;
		}
		std::cout << std::endl;
	}
}