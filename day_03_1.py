class EngineSchema:
    def __init__(self, schema):
        self.fields = []
        for row in schema:
            self.fields.append(list(map(lambda f: EngineField(f), row)))
        self._generate_neighbourhood()

    def _generate_neighbourhood(self):
        for y in range(0, len(self.fields)):
            for x in range(0, len(self.fields[0])):
                if y != 0:
                    self.fields[y][x].neighbours.append(self.fields[y - 1][x])
                    self.fields[y - 1][x].neighbours.append(self.fields[y][x])

                    if x != 0:
                        self.fields[y][x].neighbours.append(self.fields[y - 1][x - 1])
                        self.fields[y - 1][x - 1].neighbours.append(self.fields[y][x])
                    if x < len(self.fields[0]) - 1:
                        self.fields[y][x].neighbours.append(self.fields[y - 1][x + 1])
                        self.fields[y - 1][x + 1].neighbours.append(self.fields[y][x])

                if x != 0:
                    self.fields[y][x].neighbours.append(self.fields[y][x - 1])
                    self.fields[y][x - 1].neighbours.append(self.fields[y][x])

    def parse_valid_numbers(self):
        valid_numbers = []
        current_number = []
        current_is_valid = False

        for y in range(0, len(self.fields)):
            for x in range(0, len(self.fields[0])):
                if self.fields[y][x].is_digit():
                    current_number.append(self.fields[y][x])
                    if self.fields[y][x].has_symbol_in_neighbourhood():
                        current_is_valid = True
                else:
                    if current_is_valid:
                        part_num = "".join(map(lambda f: f.val, current_number))
                        part = EnginePart(int(part_num))
                        valid_numbers.append(part)
                        for f in current_number:
                            f.part = part

                    current_number = []
                    current_is_valid = False

            if current_is_valid:
                part_num = "".join(map(lambda f: f.val, current_number))
                part = EnginePart(int(part_num))
                valid_numbers.append(part)
                for f in current_number:
                    f.part = part
            current_number = []
            current_is_valid = False

        return list(map(lambda p: p.number, valid_numbers))

    def calculate_gear_power(self):
        power_sum = 0
        for y in range(0, len(self.fields)):
            for x in range(0, len(self.fields[0])):
                if self.fields[y][x].val == '*':
                    neighbour_parts = set(map(lambda f: f.part, self.fields[y][x].neighbours))
                    neighbour_parts = set(filter(lambda p: p is not None, neighbour_parts))
                    if len(neighbour_parts) == 2:
                        number_1 = neighbour_parts.pop().number
                        number_2 = neighbour_parts.pop().number
                        power_sum += number_1 * number_2

        return power_sum


class EngineField:
    def __init__(self, val):
        self.val = val
        self.neighbours = []
        self.part = None

    def is_symbol(self):
        return not self.val.isdigit() and self.val != '.'

    def is_digit(self):
        return self.val.isdigit()

    def has_symbol_in_neighbourhood(self):
        return any(map(lambda f: f.is_symbol(), self.neighbours))

    def __str__(self):
        return self.val


class EnginePart:
    def __init__(self, number):
        self.number = number


with open("input/day_03.txt") as file:
    lines = file.readlines()
    lines = map(lambda line: line.strip(), lines)
    lines = map(lambda line: list(line), lines)
    schema = EngineSchema(lines)

    schema.parse_valid_numbers()
    schema.parse_valid_numbers()
    print(schema.calculate_gear_power())
