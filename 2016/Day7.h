#pragma once

#include "CommonFunctions.h"

//--- Day 7: Internet Protocol Version 7 ---

namespace Day7
{
	bool IsABBA(const std::string& str)
	{
		if (str.length() < 4) return false;

		for (size_t i = 0; i < str.length() - 3; i++)
		{
			if (str[i] == str[i + 3] && 
				str[i + 1] == str[i + 2] &&
				str[i] != str[i + 1]) return true;
		}

		return false;
	}

	bool IPSupportsTLS(const std::string& ipStr)
	{
		bool containsABBAOutsideBrackets = false;
		bool inBrackets = false;
		for (size_t j = 0; j < ipStr.length(); j++)
		{
			char currentChar = ipStr.at(j);
			if (currentChar == '[')
			{
				assert(inBrackets == false);
				inBrackets = true;
			}
			else if (currentChar == ']')
			{
				assert(inBrackets == true);
				inBrackets = false;
			}
			else
			{
				int count = 4;
				if (j > ipStr.length() - 3)
				{
					count = int(ipStr.length()) - 4;
				}

				if (IsABBA(ipStr.substr(j, count)))
				{
					if (inBrackets)
					{
						return false;
					}
					else
					{
						containsABBAOutsideBrackets = true;
					}
				}
			}
		}

		return containsABBAOutsideBrackets;
	}

	bool IsABA(const std::string& str)
	{
		if (str.length() < 3) return false;
		return (str[0] == str[2] && str[0] != str[1]);
	}

	bool IsABA_BABPair(const std::string& aba, const std::string& bab)
	{
		if (aba.length() != 3 || bab.length() != 3) return false;
		if (!IsABA(aba) || !IsABA(bab)) return false;

		return (aba[0] == bab[1] && 
				bab[0] == aba[1]);
	}

	bool IPSupporsSSL(const std::string& ipStr)
	{
		std::vector<std::string> ABAs; // Outside square brackets
		std::vector<std::string> BABs; // Inside square brackets
		bool inBrackets = false;
		for (size_t j = 0; j < ipStr.length(); j++)
		{
			char currentChar = ipStr.at(j);
			if (currentChar == '[')
			{
				assert(inBrackets == false);
				inBrackets = true;
			}
			else if (currentChar == ']')
			{
				assert(inBrackets == true);
				inBrackets = false;
			}
			else
			{
				int count = 3;
				if (j > ipStr.length() - 2)
				{
					count = int(ipStr.length()) - 3;
				}

				std::string possibleABA = ipStr.substr(j, count);
				if (IsABA(possibleABA))
				{
					if (inBrackets)
					{
						BABs.push_back(possibleABA);
					}
					else
					{
						ABAs.push_back(possibleABA);
					}
				}
			}
		}

		for (size_t i = 0; i < ABAs.size(); i++)
		{
			for (size_t j = 0; j < BABs.size(); j++)
			{
				if (IsABA_BABPair(ABAs[i], BABs[j]))
				{
					return true;
				}
			}
		}
		
		return false;
	}

	void Day7()
	{
		std::cout << "Day 7: " << std::endl;

		std::string input;
		if (ReadFile(input, "input/Day7Input.txt"))
		{
			int tlsIPCount = 0;
			int sslIPCount = 0;
			std::vector<std::string> inputLines = Split(input);
			for (size_t i = 0; i < inputLines.size(); i++)
			{
				if (IPSupportsTLS(inputLines[i]))
				{
					++tlsIPCount;
				}

				if (IPSupporsSSL(inputLines[i]))
				{
					++sslIPCount;
				}
			}

			std::cout << "Number of IPs that support TLS: " << tlsIPCount << std::endl;
			std::cout << "Number of IPs that support SSL: " << sslIPCount << std::endl;
		}

		std::cout << std::endl;
	}
}