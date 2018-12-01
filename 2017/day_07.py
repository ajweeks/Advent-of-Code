import pprint

from collections import defaultdict


def tree(): return defaultdict(tree)


def dicts(t): return {k: dicts(t[k]) for k in t}


f = open("day_07_input.txt")
fileStr = f.read()

# fileStr = "\
# pbga (66)\n\
# xhth (57)\n\
# ebii (61)\n\
# havc (66)\n\
# ktlj (57)\n\
# fwft (72) -> ktlj, cntj, xhth\n\
# qoyq (66)\n\
# padx (45) -> pbga, havc, qoyq\n\
# tknk (41) -> ugml, padx, fwft\n\
# jptl (61)\n\
# ugml (68) -> gyxo, ebii, jptl\n\
# gyxo (61)\n\
# cntj (57)"

lines = fileStr.splitlines()


def all_programs():
    p = set()
    for line in lines:
        line_parts = line.split()
        children = ""
        if '->' in line_parts:
            for child in line_parts[3:]:
                c = child.strip(',')
                children += c + " " if c not in p else ""
        p.add((str(line_parts[0]), int(line_parts[1].strip('()')), children))
    return p


def get_child(name):
    for program in all_programs:
        if name == program[0]:
            return program
    return None


all_programs = all_programs()


def bottom_program():
    possible_bottom_programs = all_programs

    for line in lines:
        line_parts = line.split()
        if '->' in line_parts:
            for child in line_parts[3:]:
                possible_bottom_programs = [e for e in possible_bottom_programs if child.strip(',') != e[0]]

    if len(possible_bottom_programs) != 1:
        print("ERROR: Failed to find bottom program!")

    return possible_bottom_programs.pop()


def find_unique(lst):
    if len(lst) <= 1:
        return 0

    if lst[0] != lst[1]:
        if lst[0] == lst[2]:
            return 1
        else:
            return 0

    for i in range(1, len(lst)):
        if lst[i] != lst[0]:
            return i


def get_program_weight(program):
    weight = program[1]

    if len(program[2]) > 0:
        child_weights = []
        for child in program[2].split():
            child_weights.append(get_program_weight(get_child(child)))
            weight += child_weights[-1]

        for w in range(1, len(child_weights)):
            if child_weights[w] != child_weights[0]:
                unique_index = find_unique(child_weights)
                other_index = (unique_index + 1) % len(child_weights)
                diff = child_weights[other_index] - child_weights[unique_index]
                unbalanced_child = get_child(program[2].split()[unique_index])
                print(unbalanced_child[1] + diff)
                exit()

    return weight


def get_children(program):
    return [c.strip(',') for c in lines[[l.split()[0] for l in lines].index(program[0])].split()[3:]]


def parse_tree():
    bottom = bottom_program()
    get_program_weight(bottom)


part_2 = True
if part_2:
    parse_tree()
else:
    print(bottom_program()[0])
