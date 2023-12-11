class MazeElement:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze

    @staticmethod
    def from_char(field_type, x, y, maze):
        if field_type in MAZE_TYPES:
            return MAZE_TYPES[field_type](x, y, maze)
        return None

    def __str__(self):
        return f"({self.x}, {self.y})"


class VerticalPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x, self.y - 1),
                      self.maze.get_element(self.x, self.y + 1)]

        return [elem for elem in neighbours if elem is not None]


class HorizontalPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x - 1, self.y),
                      self.maze.get_element(self.x + 1, self.y)]

        return [elem for elem in neighbours if elem is not None]


class NorthEastPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x, self.y - 1),
                      self.maze.get_element(self.x + 1, self.y)]

        return [elem for elem in neighbours if elem is not None]


class NorthWestPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x, self.y - 1),
                      self.maze.get_element(self.x - 1, self.y)]

        return [elem for elem in neighbours if elem is not None]


class SouthEastPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x, self.y + 1),
                      self.maze.get_element(self.x + 1, self.y)]

        return [elem for elem in neighbours if elem is not None]


class SouthWestPipe(MazeElement):
    def get_neighbours(self):
        neighbours = [self.maze.get_element(self.x, self.y + 1),
                      self.maze.get_element(self.x - 1, self.y)]

        return [elem for elem in neighbours if elem is not None]


class GroundElement(MazeElement):
    def get_neighbours(self):
        return []


class StartElement(MazeElement):
    def get_neighbours(self):
        neighours = [
            self.maze.fields[self.x + 1][self.y],
            self.maze.fields[self.x - 1][self.y],
            self.maze.fields[self.x][self.y + 1],
            self.maze.fields[self.x][self.y - 1],
        ]

        return [elem for elem in neighours if elem and self in elem.get_neighbours()]

    def to_maze_element(self):
        neighbours = self.get_neighbours()

        if set(neighbours) == {self.maze.get_element(self.x - 1, self.y), self.maze.get_element(self.x + 1, self.y)}:
            return HorizontalPipe(self.x, self.y, self.maze)
        if set(neighbours) == {self.maze.get_element(self.x, self.y - 1), self.maze.get_element(self.x, self.y + 1)}:
            return VerticalPipe(self.x, self.y, self.maze)
        if set(neighbours) == {self.maze.get_element(self.x + 1, self.y), self.maze.get_element(self.x, self.y + 1)}:
            return SouthEastPipe(self.x, self.y, self.maze)
        if set(neighbours) == {self.maze.get_element(self.x + 1, self.y), self.maze.get_element(self.x, self.y - 1)}:
            return NorthEastPipe(self.x, self.y, self.maze)
        if set(neighbours) == {self.maze.get_element(self.x - 1, self.y), self.maze.get_element(self.x, self.y + 1)}:
            return SouthWestPipe(self.x, self.y, self.maze)
        if set(neighbours) == {self.maze.get_element(self.x - 1, self.y), self.maze.get_element(self.x, self.y - 1)}:
            return SouthEastPipe(self.x, self.y, self.maze)


class Maze:
    def __init__(self, maze_lines):
        self.fields = []

        for x in range(0, len(maze_lines[0])):
            self.fields.append([])
            for y in range(0, len(maze_lines)):
                new_element = MazeElement.from_char(maze_lines[y][x], x, y, self)
                self.fields[x].append(new_element)

    def get_element(self, x, y):
        if 0 <= x < len(self.fields) and 0 <= y < len(self.fields):
            return self.fields[x][y]

    def get_start(self):
        for x in range(0, len(self.fields)):
            for y in range(0, len(self.fields[0])):
                if isinstance(self.fields[x][y], StartElement):
                    return self.fields[x][y]


MAZE_TYPES = {
    '|': VerticalPipe,
    '-': HorizontalPipe,
    'L': NorthEastPipe,
    'J': NorthWestPipe,
    '7': SouthWestPipe,
    'F': SouthEastPipe,
    '.': GroundElement,
    'S': StartElement
}


def find_tour(start: MazeElement):
    tour = []
    steps = 0
    current = start
    next_neighbour = [elem for elem in current.get_neighbours() if elem and elem not in tour]
    while len(next_neighbour) != 0:
        tour.append(current)
        current = next_neighbour[0]
        next_neighbour = [elem for elem in current.get_neighbours() if elem and elem not in tour]
        steps += 1
    tour.append(current)
    return tour


def calculate_area(tour):
    crossings = {}
    for elem in tour:
        if type(elem) not in [VerticalPipe]:
            crossings[elem.x] = crossings.get(elem.x, []) + [elem]

    area = 0
    for x in crossings:
        print(f"{x} {calculate_area_of_line(crossings[x])}")
        area += calculate_area_of_line(crossings[x])

    return area


def calculate_area_of_line(crossings):
    crossings.sort(key=lambda element: element.y)
    area = 0
    inside = False
    last_crossing = None

    for crossing in crossings:
        if isinstance(crossing, HorizontalPipe):
            if inside:
                area += crossing.y - last_crossing.y - 1
                inside = False
            else:
                inside = True

        if isinstance(crossing, SouthEastPipe):
            if inside:
                area += crossing.y - last_crossing.y - 1

        if isinstance(crossing, SouthWestPipe):
            if inside:
                area += crossing.y - last_crossing.y - 1

        if isinstance(crossing, NorthEastPipe):
            if isinstance(last_crossing, SouthWestPipe):
                inside = not inside

        if isinstance(crossing, NorthWestPipe):
            if isinstance(last_crossing, SouthEastPipe):
                inside = not inside

        last_crossing = crossing
    return area


with open('input/day_10.txt') as file:
    maze_lines = [line.strip() for line in file.readlines()]

maze = Maze(maze_lines)
start = maze.get_start().to_maze_element()
maze.fields[start.x][start.y] = start

tour = find_tour(start)

print(calculate_area(tour))
