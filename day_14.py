class Platform:
    def __init__(self, platform_map):
        self.columns = self._extract_columns(platform_map)

    def __str__(self):
        return "".join(self.columns)

    @staticmethod
    def _extract_columns(platform_map):
        row_length = len(platform_map.split('\n')[0])
        columns = [""] * row_length

        for column_idx in range(0, row_length):
            for row in platform_map.strip().split('\n'):
                columns[column_idx] += row[column_idx]

        return columns

    def calculate_weight(self):
        weight = 0

        for column in self.columns:
            reversed_column = column[::-1]
            for idx in range(0, len(reversed_column)):
                if reversed_column[idx] == 'O':
                    weight += (idx + 1)

        return weight

    def tilt_north(self):
        tilted_columns = []
        for column in self.columns:
            segments = [self.sort_segment(seg) for seg in column.split('#')]

            tilted_columns.append("#".join(segments))

        self.columns = tilted_columns

    def rotate_90(self):
        column_length = len(self.columns[0])
        rows = [''] * column_length

        for column in self.columns:
            for row_idx in range(0, column_length):
                rows[column_length - row_idx - 1] += column[row_idx]

        self.columns = rows

    def do_cycle(self):
        for idx in range(0, 4):
            self.tilt_north()
            self.rotate_90()

    @staticmethod
    def sort_segment(segment):
        seg_list = list(segment)
        seg_list.sort(reverse=True)
        return "".join(seg_list)


with open("input/day_14.txt") as file:
    platform = Platform(file.read())
    weights = []
    states = []
    cycle = 0

    platform.do_cycle()
    state = str(platform)
    weight = platform.calculate_weight()

    while state not in states:
        weights.append(weight)
        states.append(state)

        platform.do_cycle()

        state = str(platform)
        weight = platform.calculate_weight()

        cycle += 1

    weights.append(weight)
    states.append(state)

    cycle_start = states.index(state) + 1
    print(cycle_start)

    cycle_length = cycle - cycle_start
    print(cycle_length)

    idx = (1000000000 - cycle_start) % (cycle_length + 1)

    print(weights[idx + (cycle_start - 1)])
