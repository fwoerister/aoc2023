import re


class MapLine:
    def __init__(self, line):
        self.line = line

    def find_smudge_split_points(self, split_points):
        smudge_split_points = list(split_points)
        for split_point in split_points:
            smudges = 0
            for idx in range(0, min(split_point, len(self.line) - split_point)):
                if self.line[split_point - idx - 1] != self.line[split_point + idx]:
                    smudges += 1
            if smudges != 1:
                smudge_split_points.remove(split_point)

        return smudge_split_points

    def check_split_points(self, split_points):
        valid_split_points = list(split_points)
        for split_point in split_points:
            smudges = 0
            for idx in range(0, min(split_point, len(self.line) - split_point)):
                if self.line[split_point - idx - 1] != self.line[split_point + idx]:
                    valid_split_points.remove(split_point)
                    break

        return valid_split_points


def rotate(lines):
    new_lines = []
    for idx in range(0, len(lines[0].line)):
        new_lines.append(MapLine(""))

    for symbol_idx in range(0, len(lines[0].line)):
        for line_idx in range(0, len(lines)):
            new_lines[symbol_idx].line += lines[line_idx].line[symbol_idx]

    return new_lines


def parse_map(file):
    content = file.read()
    return content.split('\n\n')


with open('input/day_13.txt') as file:
    maps = parse_map(file)

    result = 0

    for map in maps:
        lines = [MapLine(line) for line in map.strip().split('\n')]

        split_points = range(1, len(lines[0].line))
        smudge_splitpoints = {}

        for idx in range(0, len(lines)):
            smudge_splitpoints[idx] = lines[idx].find_smudge_split_points(split_points)

        for idx in range(0, len(lines)):
            for line_idx in [i for i in range(0, len(lines)) if i != idx]:
                smudge_splitpoints[idx] = lines[line_idx].check_split_points(smudge_splitpoints[idx])

        for split_point in smudge_splitpoints.values():
            result += sum(split_point)

        lines = rotate(lines)

        split_points = range(1, len(lines[0].line))
        smudge_splitpoints = {}

        for idx in range(0, len(lines)):
            smudge_splitpoints[idx] = lines[idx].find_smudge_split_points(split_points)

        for idx in range(0, len(lines)):
            for line_idx in [i for i in range(0, len(lines)) if i != idx]:
                smudge_splitpoints[idx] = lines[line_idx].check_split_points(smudge_splitpoints[idx])

        for split_point in smudge_splitpoints.values():
            result += sum(split_point) * 100

print(result)
