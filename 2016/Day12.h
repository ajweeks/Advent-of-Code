#pragma once

#include "CommonFunctions.h"

//--- Day 12: Leonardo's Monorail ---

namespace Day12
{
	enum Instruction
	{
		CPY, INC, DEC, JNZ
	};

	struct InstructionSet
	{
		Instruction inst;
		int* regX = nullptr;
		int valueX = 0;
		int* regY = nullptr;
		int valueY = 0;
	};

	std::vector<InstructionSet> ParseIntructions(const std::vector<std::string>& instructions, 
		int* a, int* b, int* c, int* d)
	{
		std::vector<InstructionSet> result;
		result.reserve(instructions.size());

		for (size_t i = 0; i < instructions.size(); i++)
		{
			InstructionSet set = {};
			std::vector<std::string> instructionParts = Split(instructions[i], ' ');
			std::string instruction = instructionParts[0];

			if (instruction.compare("cpy") == 0)
			{
				set.inst = Instruction::CPY;

				std::string x = instructionParts[1];
				char y = instructionParts[2].at(0);

				if (isdigit(x.at(0)))
				{
					set.valueX = atoi(x.c_str());
				}
				else
				{
					char reg = x.at(0);
					if (reg == 'a') set.regX = a;
					else if (reg == 'b') set.regX = b;
					else if (reg == 'c') set.regX = c;
					else if (reg == 'd') set.regX = d;
					else std::cout << "Invalid register! " << reg << std::endl;
				}

				if (y == 'a') set.regY = a;
				else if (y == 'b') set.regY = b;
				else if (y == 'c') set.regY = c;
				else if (y == 'd') set.regY = d;
				else std::cout << "Invalid register! " << y << std::endl;
			}
			else if (instruction.compare("inc") == 0)
			{
				set.inst = Instruction::INC;
				char x = instructionParts[1].at(0);
				if (x == 'a') set.regX = a;
				else if (x == 'b') set.regX = b;
				else if (x == 'c') set.regX = c;
				else if (x == 'd') set.regX = d;
				else std::cout << "Invalid register! " << x << std::endl;
			}
			else if (instruction.compare("dec") == 0)
			{
				set.inst = Instruction::DEC;
				char x = instructionParts[1].at(0);
				if (x == 'a') set.regX = a;
				else if (x == 'b') set.regX = b;
				else if (x == 'c') set.regX = c;
				else if (x == 'd') set.regX = d;
				else std::cout << "Invalid register! " << x << std::endl;
			}
			else if (instruction.compare("jnz") == 0)
			{
				set.inst = Instruction::JNZ;
				std::string x = instructionParts[1];
				set.valueY = stoi(instructionParts[2]);

				if (isdigit(x.at(0)))
				{
					set.valueX = atoi(x.c_str());
				}
				else
				{
					char reg = x.at(0);
					if (reg == 'a') set.regX = a;
					else if (reg == 'b') set.regX = b;
					else if (reg == 'c') set.regX = c;
					else if (reg == 'd') set.regX = d;
					else std::cout << "Invalid register! " << reg << std::endl;
				}
			}

			result.push_back(set);
		}

		return result;
	}

	void Day12()
	{
		std::cout << "Day 12: " << std::endl;

		bool part2 = false;

		std::string fileString;
		if (ReadFile(fileString, "input/Day12Input.txt"))
		{
			std::vector<std::string> instructionStrings = Split(fileString);

			int a = 0;
			int b = 0;
			int c = (part2 ? 1 : 0);
			int d = 0;
			std::vector<InstructionSet> instructions = ParseIntructions(instructionStrings, &a, &b, &c, &d);
			for (size_t i = 0; i < instructions.size(); i++)
			{
				InstructionSet set = instructions[i];
				switch (set.inst)
				{
				case Instruction::CPY:
				{
					if (set.regX != nullptr)
					{
						*set.regY = *set.regX;
					}
					else
					{
						*set.regY = set.valueX;
					}
				} break;
				case Instruction::INC:
				{
					++(*set.regX);
				} break;
				case Instruction::DEC:
				{
					--(*set.regX);
				} break;
				case Instruction::JNZ:
				{
					int x = 0;
					if (set.regX != nullptr) x = *set.regX;
					else x = set.valueX;
					if (x != 0)
					{
						i += set.valueY - 1;
					}
				} break;
				default:
				{
					std::cout << "Invalid instruction! " << instructions[i].inst << std::endl;
				} break;
				}
			}

			std::cout << "Registers after instructions executed: a: " << a << " b: " << b << " c: " << c << " d: " << d << std::endl; 
		}
	
		std::cout << std::endl;
	}
}