import re
import math


def calculate_distance_to_destination(dessert_map, start):
    current = start
    steps = 0
    idx = 0
    while not current.endswith('Z'):
        current = desert_map[current][directions[idx]]
        idx = (idx + 1) % len(directions)
        steps += 1
    return steps


def parse_desert_map(elements):
    desert_map = {}
    for element in network_elements:
        desert_map[element[0]] = {'L': element[1], 'R': element[2]}
    return desert_map


with (open('input/day_08.txt')) as file:
    directions = re.findall(r"([RL]+)", file.readline())[0]
    content = "".join(file.readlines())
    network_elements = re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", content)

desert_map = parse_desert_map(network_elements)

start_positions = list(filter(lambda elem: elem.endswith('A'), desert_map.keys()))

distances_to_destination = [calculate_distance_to_destination(desert_map, pos) for pos in start_positions]

print(math.lcm(*distances_to_destination))
