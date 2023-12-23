from collections import deque


class Grid:
    def __init__(self, lines):
        self.tiles = self._parse_lines(lines)
        self.width = len(self.tiles)
        self.height = len(self.tiles[0])
        self.start = self._find_start()

    def _find_start(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.tiles[x][y] == 'S':
                    return x, y

    @staticmethod
    def _parse_lines(lines):
        tile_map = []

        for column_idx in range(len(lines[0])):
            tile_map.append([])
            for row_idx in range(len(lines)):
                tile_map[-1].append(lines[row_idx][column_idx])
        return tile_map

    def is_garden_tile(self, x, y):
        x = x % self.width
        y = y % self.height

        if 0 <= x < self.width and 0 <= y < self.height:
            if self.tiles[x][y] != '#':
                return True

    def reachable_tiles(self, steps):

        routes = [self.start]

        steps_history = dict()

        for steps in range(steps):
            new_positions = set()
            for route in routes:
                for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    x = (route[0] + direction[0]) % self.width
                    y = (route[1] + direction[1]) % self.height

                    if self.is_garden_tile(x, y):
                        new_positions.add((x, y))
                        steps_history[(x, y)] = steps_history.get((x, y), set())
                        steps_history[(x, y)].add(steps)

            # self.draw_map(visited)

            routes = new_positions

        return len(routes)

    def draw_map(self, visited):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in visited:
                    print('O', end='')
                else:
                    print(self.tiles[x][y], end='')
            print()
        print()


with open('input/day_21.txt') as file:
    grid = Grid([line.strip() for line in file.readlines()])

last_result = 0
grid.reachable_tiles(300)
