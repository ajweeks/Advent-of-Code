
def get_input_str():
    return open("day06.in").readlines()


def get_inputs(input_str):
    return [y.rstrip().split(')') for y in input_str]


class Planet:
    def __init__(self, name, indirect_orbits, parent):
        self.name = name
        self.indirect_orbits = indirect_orbits
        self.parent = parent
        self.children = []

    def has_child(self, child_name):
        if self.name == child_name:
            return True
        for child in self.children:
            if child.has_child(child_name):
                return True
        return False

    def has_direct_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return True
        return False

    def add_child(self, child_name):
        if self.has_direct_child(child_name):
            return
        self.children.append(Planet(child_name, self.indirect_orbits + 1, self))
        return True

    def find_direct_children(self, inputs):
        for line in inputs:
            if line[0] == self.name:
                if self.add_child(line[1]):
                    self.children[-1].find_direct_children(inputs)

    def print_self(self):
        print(self.name, self.indirect_orbits)
        for child in self.children:
            print(' ' * child.indirect_orbits, end='')
            child.print_self()

    def count_orbits(self):
        orbits = self.indirect_orbits
        for child in self.children:
            orbits += child.count_orbits()
        return orbits

    def find_planet(self, planet_name):
        if self.name == planet_name:
            return self
        for child in self.children:
            planet = child.find_planet(planet_name)
            if planet:
                return planet
        return None

    def common_ancestor(self, other):
        ancestor = None
        p1 = self.parent
        p2 = other.parent
        while p1 != p2:
            if p1.has_child(other.name):
                ancestor = p1
                break
            if p2.has_child(self.name):
                ancestor = p2
                break

            if p1.parent:
                p1 = p1.parent
            else:
                p2 = p2.parent
        if ancestor is None and p1 == p1:
            ancestor = p1
        return ancestor


def part1():
    inputs = get_inputs(get_input_str())
    # inputs = get_inputs("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".splitlines())
    root = None
    for line in inputs:  # Find root node
        if line[0] == 'COM':
            root = Planet('COM', 0, None)
            break
    assert root

    root.find_direct_children(inputs)
    # root.print_self()
    print(root.count_orbits())


def part2():
    inputs = get_inputs(get_input_str())
    # inputs = get_inputs("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN".splitlines())
    root = None
    for line in inputs:  # Find root node
        if line[0] == 'COM':
            root = Planet('COM', 0, None)
            break
    assert root

    root.find_direct_children(inputs)

    you = root.find_planet('YOU')
    santa = root.find_planet('SAN')

    common_ancestor = you.common_ancestor(santa)

    print(you.indirect_orbits - common_ancestor.indirect_orbits +
          santa.indirect_orbits - common_ancestor.indirect_orbits
          - 2)
