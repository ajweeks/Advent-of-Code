
f = open("day_24_input.txt")
portsStr = f.read()

# portsStr = """0/2
# 2/2
# 2/3
# 3/4
# 3/5
# 0/1
# 10/1
# 9/10"""

components = []
for str in [s.split('/') for s in portsStr.split('\n')]:
    components.append([int(str[0]), int(str[1])])
components = sorted(components)

strongestBridge = []
strongestBridgeStrength = 0

longestBridge = []
longestBridgeLength = 0

part2 = True


def contains_component(bridge, component):
    for c in bridge:
        if component == c:
            return True
    return False


def measure_strength(bridge):
    strength = 0
    for c in bridge:
        strength += c[0] + c[1]

    return strength


def do_bridge(cur_bridge, next_port_idx):
    global strongestBridge
    global strongestBridgeStrength
    global longestBridge
    global longestBridgeLength
    global part2

    next_port = cur_bridge[-1][next_port_idx]

    for c in components:
        if not contains_component(cur_bridge, c):
            new_next_port_idx = -1
            if c[0] == next_port:
                new_next_port_idx = 1
            if c[1] == next_port:
                new_next_port_idx = 0

            if new_next_port_idx != -1:
                new_bridge = cur_bridge[:]
                new_bridge.append(c)
                s = measure_strength(new_bridge)
                l = len(new_bridge)
                if part2:
                    if l > longestBridgeLength or (l == longestBridgeLength and s > strongestBridgeStrength):
                        longestBridgeLength = l
                        longestBridge = new_bridge
                        strongestBridgeStrength = s
                        strongestBridge = new_bridge
                        print(f"Longest bridge length: {longestBridgeLength} (strength: {strongestBridgeStrength})")
                        print(f"{longestBridge}")
                else:
                    if s > strongestBridgeStrength:
                        strongestBridgeStrength = s
                        strongestBridge = new_bridge
                        print(f"Strongest bridge strength: {strongestBridgeStrength}")
                        print(f"{strongestBridge}")
                do_bridge(new_bridge, new_next_port_idx)


def main():
    starting_ports = []
    for c in components:
        if c[0] == 0 or c[1] == 0:
            starting_ports.append(c)

    for start in starting_ports:
        cur_bridge = [start]
        do_bridge(cur_bridge, 1)

    print(f"Strongest bridge strength: {strongestBridgeStrength}")
    print(f"{strongestBridge}")


main()
