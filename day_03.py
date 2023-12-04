class Symbol:
    def __init__(self, char, position):
        self.char = char
        self.position = position


class EnginePart:
    def __init__(self, number, indices):
        self.number = number
        self.indices = indices
        self.neighbourhood = set()
        self.generate_neighbourhood()

    def generate_neighbourhood(self):
        for pos in self.indices:
            self.neighbourhood = self.neighbourhood.union(self._pos_to_neighbourhood(pos))

    @staticmethod
    def _pos_to_neighbourhood(pos):
        return {(pos[0] - 1, pos[1] - 1), (pos[0], pos[1] - 1),
                (pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1]),
                (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1] + 1),
                (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] + 1)}

    def is_adjacent(self, sym: Symbol):
        return sym.position in self.neighbourhood


def load_parts_and_symbols(lines):
    parts = []
    symbols = []
    for y, line in enumerate(lines):
        part_num = ""
        part_indices = []

        for x, char in enumerate(line.strip()):
            if char.isdigit():
                part_num += char
                part_indices.append((x, y))
            else:
                if char != '.':
                    symbols.append(Symbol(char, (x, y)))
                if part_num:
                    parts.append(EnginePart(int(part_num), part_indices))
                part_num = ""
                part_indices = []

        if part_num:
            parts.append(EnginePart(int(part_num), part_indices))

    return parts, symbols


def calculate_gear_ratio(parts, sym):
    adjacent_parts = [part for part in parts if part.is_adjacent(sym)]
    return adjacent_parts[0].number * adjacent_parts[1].number if len(adjacent_parts) == 2 else 0


def is_valid_part(part, symbols):
    return any([part.is_adjacent(s) for s in symbols])


with open("input/day_03.txt") as file:
    engine_parts, plan_symbols = load_parts_and_symbols(file.readlines())

    print("part 1:")
    valid_parts = [p.number for p in engine_parts if is_valid_part(p, plan_symbols)]

    print(sum(valid_parts))

    print("part 2:")
    gear_symbols = list(filter(lambda sym: sym.char == '*', plan_symbols))
    gear_power_sum = 0
    for symbol in gear_symbols:
        gear_power_sum += calculate_gear_ratio(engine_parts, symbol)
    print(gear_power_sum)
