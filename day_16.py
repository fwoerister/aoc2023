class CaveTile:
    def __init__(self, x, y, cave=None):
        self.x = x
        self.y = y
        self.cave = cave
        self.source_cache = set()

    def __str__(self):
        return f"{type(self).__name__} ({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x}-{self.y}")


class FinalTile(CaveTile):
    @staticmethod
    def process_ray_beam(trace):
        return trace


class VerticalSplitter(CaveTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def process_ray_beam(self, trace):
        source_tile = trace[-2]

        if source_tile in self.source_cache:
            return [trace + [FinalTile(self.x, self.y)]]
        self.source_cache.add(source_tile)

        column = self.cave.columns[self.x]
        column_idx = column.index(self)

        if column_idx >= len(column) - 1:
            bottom_beam = FinalTile(self.x, self.cave.height - 1)
        else:
            bottom_beam = column[column_idx + 1]

        if column_idx <= 0:
            top_beam = FinalTile(self.x, 0)
        else:
            top_beam = column[column_idx - 1]

        if self.x == source_tile.x:
            if self.y > source_tile.y:
                return [trace + [bottom_beam]]
            elif self.y < source_tile.y:
                return [trace + [top_beam]]

        return [trace + [top_beam], trace + [bottom_beam]]


class HorizontalSplitter(CaveTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def process_ray_beam(self, trace):
        source_tile = trace[-2]

        if source_tile in self.source_cache:
            return [trace + [FinalTile(self.x, self.y)]]
        self.source_cache.add(source_tile)

        row = self.cave.rows[self.y]
        row_idx = row.index(self)

        if row_idx >= len(row) - 1:
            right_beam = FinalTile(self.cave.width - 1, self.y)
        else:
            right_beam = row[row_idx + 1]

        if row_idx <= 0:
            left_beam = FinalTile(0, self.y)
        else:
            left_beam = row[row_idx - 1]

        if self.y == source_tile.y:
            if self.x > source_tile.x:
                return [trace + [right_beam]]
            elif self.x < source_tile.x:
                return [trace + [left_beam]]

        return [trace + [right_beam], trace + [left_beam]]


class Mirror(CaveTile):
    def get_neighbours(self):
        column = self.cave.columns[self.x]
        row = self.cave.rows[self.y]

        column_idx = column.index(self)
        row_idx = row.index(self)

        if column_idx <= 0:
            north_neighbour = FinalTile(self.x, 0)
        else:
            north_neighbour = column[column_idx - 1]

        if column_idx >= len(column) - 1:
            south_neighbour = FinalTile(self.x, self.cave.height - 1)
        else:
            south_neighbour = column[column_idx + 1]

        if row_idx <= 0:
            west_neighbour = FinalTile(0, self.y)
        else:
            west_neighbour = row[row_idx - 1]

        if row_idx >= len(row) - 1:
            east_neighbour = FinalTile(self.cave.width - 1, self.y)
        else:
            east_neighbour = row[row_idx + 1]

        return north_neighbour, east_neighbour, south_neighbour, west_neighbour


class SlashMirror(Mirror):
    def __init__(self, x, y):
        super().__init__(x, y)

    def process_ray_beam(self, trace):
        source_tile = trace[-2]

        if source_tile in self.source_cache:
            return [trace + [FinalTile(self.x, self.y)]]
        self.source_cache.add(source_tile)

        north_neighbour, east_neighbour, south_neighbour, west_neighbour = self.get_neighbours()

        if self.x == source_tile.x:
            if self.y > source_tile.y:

                return [trace + [west_neighbour]]
            else:
                return [trace + [east_neighbour]]

        if self.y == source_tile.y:
            if self.x > source_tile.x:
                return [trace + [north_neighbour]]
            else:
                return [trace + [south_neighbour]]


class BackSlashMirror(Mirror):
    def process_ray_beam(self, trace):
        source_tile = trace[-2]
        north_neighbour, east_neighbour, south_neighbour, west_neighbour = self.get_neighbours()

        if source_tile in self.source_cache:
            return [trace + [FinalTile(self.x, self.y)]]
        self.source_cache.add(source_tile)

        if self.x == source_tile.x:
            if self.y > source_tile.y:
                return [trace + [east_neighbour]]
            else:
                return [trace + [west_neighbour]]

        if self.y == source_tile.y:
            if self.x > source_tile.x:
                return [trace + [south_neighbour]]
            else:
                return [trace + [north_neighbour]]


class Cave:
    def __init__(self, width, height, mirrors, splitters):
        self.width = width
        self.height = height

        self.mirrors = mirrors
        self.splitters = splitters

        self._set_reference_to_cave()

        self.rows = {}
        self._generate_rows()

        self.columns = {}
        self._generate_columns()

    def reset_source_cache(self):
        for mirror in self.mirrors:
            mirror.source_cache = set()
        for splitter in self.splitters:
            splitter.source_cache = set()

    def _set_reference_to_cave(self):
        for mirror in self.mirrors:
            mirror.cave = self
        for splitter in self.splitters:
            splitter.cave = self

    def _generate_rows(self):
        for mirror in self.mirrors:
            row_list = self.rows.get(mirror.y, [])
            self.rows[mirror.y] = row_list + [mirror]
        for splitter in self.splitters:
            row_list = self.rows.get(splitter.y, [])
            self.rows[splitter.y] = row_list + [splitter]

        for lst in self.rows.values():
            lst.sort(key=lambda tile: tile.x)

    def _generate_columns(self):
        for mirror in self.mirrors:
            column_list = self.columns.get(mirror.x, [])
            self.columns[mirror.x] = column_list + [mirror]
        for splitter in self.splitters:
            column_list = self.columns.get(splitter.x, [])
            self.columns[splitter.x] = column_list + [splitter]

        for lst in self.columns.values():
            lst.sort(key=lambda tile: tile.y)

    def find_most_energetic_beam(self):
        max_energy = 0
        for idx in range(0, self.width):
            result = len(self.calculate_visited_tiles(CaveTile(idx, 0), 's'))

            max_energy = max(max_energy, result)
            result = len(self.calculate_visited_tiles(CaveTile(idx, self.height - 1), 'n'))

            max_energy = max(max_energy, result)

        for idx in range(0, self.height):
            result = len(self.calculate_visited_tiles(CaveTile(0, idx), 'e'))

            max_energy = max(max_energy, result)
            result = len(self.calculate_visited_tiles(CaveTile(self.width - 1, idx), 'w'))

            max_energy = max(max_energy, result)

        return max_energy

    def follow_beam(self, source, direction='w'):
        match direction:
            case 'e':
                initial_trace = [[source, self.rows[source.y][0]]] if source.y in self.rows else [
                    [source, FinalTile(self.height - 1, source.y)]]
            case 's':
                initial_trace = [[source, self.columns[source.x][0]]] if source.x in self.columns else [
                    [source, FinalTile(source.x, self.height - 1)]]
            case 'w':
                initial_trace = [[source, self.rows[source.y][-1]]] if source.y in self.rows else [
                    [source, FinalTile(0, source.y)]]
            case 'n':
                initial_trace = [[source, self.columns[source.x][-1]]] if source.x in self.columns else [
                    [source, FinalTile(source.x, 0)]]

        terminated_traces = list(filter(lambda t: isinstance(t[-1], FinalTile), initial_trace))
        open_traces = list(filter(lambda t: not isinstance(t[-1], FinalTile), initial_trace))

        while open_traces:
            new_open_traces = []
            for trace in open_traces:
                result = trace[-1].process_ray_beam(trace)
                terminated_traces += list(filter(lambda t: isinstance(t[-1], FinalTile), result))
                new_open_traces += list(filter(lambda t: not isinstance(t[-1], FinalTile), result))
            open_traces = new_open_traces

        return terminated_traces

    def calculate_visited_tiles(self, source, direction):
        visited_tiles = set()
        traces = self.follow_beam(source, direction)

        for trace in traces:
            prev_tile = trace[0]
            visited_tiles.add(prev_tile)

            for tile in trace[1:]:
                visited_tiles.update(self._to_tiles(prev_tile, tile))
                prev_tile = tile

        self.reset_source_cache()
        return visited_tiles

    @staticmethod
    def _to_tiles(source, target):
        generated_tiles = []
        if source.x == target.x:
            for y in range(min(source.y, target.y), max(source.y, target.y) + 1):
                generated_tiles.append(CaveTile(source.x, y))

        elif source.y == target.y:
            for x in range(min(source.x, target.x), max(source.x, target.x) + 1):
                generated_tiles.append(CaveTile(x, source.y))

        return generated_tiles


def parse_cave(cave_lines):
    splitters = []
    mirrors = []

    width = len(cave_lines[0].strip())
    height = len(cave_lines)

    for row in range(0, height):
        for column in range(0, width):
            match cave_lines[row][column]:
                case '/':
                    mirrors.append(SlashMirror(column, row))
                case '\\':
                    mirrors.append(BackSlashMirror(column, row))
                case '-':
                    splitters.append(HorizontalSplitter(column, row))
                case '|':
                    splitters.append((VerticalSplitter(column, row)))
    return Cave(width, height, mirrors, splitters)


def print_visited_tiles(visited_tiles, width, height):
    for y in range(0, height):
        for x in range(0, width):
            if CaveTile(x, y) in visited_tiles:
                print('#', end='')
            else:
                print('.', end='')
        print('')


with open('input/day_16.txt') as file:
    lines = file.readlines()

cave = parse_cave(lines)
print(cave.find_most_energetic_beam())
