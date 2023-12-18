import re


class Cube:
    def __init__(self, x, y, is_vertical):
        self.x = x
        self.y = y
        self.is_vertical = is_vertical

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class DigDirection:
    def __init__(self, orientation, distance, color):
        self.orientation = orientation
        self.distance = distance
        self.color = color


class Shape:
    def __init__(self, edge):
        self.edge = edge

    def get_covered_cubes(self) -> set:
        pass

    def print_edge(self, vertical_only):
        y_coordinates = [cube.y for cube in self.edge]

        for y in range(min(y_coordinates), max(y_coordinates) + 1):
            if vertical_only:
                x_coordinates = [cube.x for cube in self.edge if cube.y == y and cube.is_vertical]
            else:
                x_coordinates = [cube.x for cube in self.edge if cube.y == y]
            x_coordinates.sort()

            count = 0
            for coordinate in x_coordinates:
                while count < coordinate:
                    print(' ', end='')
                    count += 1
                print('#', end='')
                count += 1

            print('')


class Lagoon:
    def __init__(self, dig_directions):
        self.current = Cube(0, 0, False)
        self.dig_directions = dig_directions
        self.edge = [self.current]
        self.shapes = []

        self._generate_edge_cubes()

    def _generate_edge_cubes(self):
        for direction in self.dig_directions:
            match direction.orientation:
                case 'U':
                    self.current.is_vertical = True
                    for step in range(0, direction.distance):
                        self.current = Cube(self.current.x, self.current.y - 1, True)
                        if self.current in self.edge:
                            current_idx = self.edge.index(self.current)
                            self.edge[current_idx].is_vertical = True
                            self.shapes.append(Shape(self.edge[current_idx:]))
                            self.edge = self.edge[:current_idx]
                            self.current.is_vertical = False
                        self.edge.append(self.current)
                case 'D':
                    self.current.is_vertical = True
                    for step in range(0, direction.distance):
                        self.current = Cube(self.current.x, self.current.y + 1, True)
                        if self.current in self.edge:
                            current_idx = self.edge.index(self.current)
                            self.edge[current_idx].is_vertical = True
                            self.shapes.append(Shape(self.edge[current_idx:]))
                            self.edge = self.edge[:current_idx]
                            self.current.is_vertical = False
                        self.edge.append(self.current)
                case 'L':
                    for step in range(0, direction.distance):
                        self.current = Cube(self.current.x - 1, self.current.y, False)
                        if self.current in self.edge:
                            current_idx = self.edge.index(self.current)
                            self.edge[current_idx].is_vertical = False
                            self.shapes.append(Shape(self.edge[current_idx:]))
                            self.edge = self.edge[:current_idx]
                        self.edge.append(self.current)
                case 'R':
                    for step in range(0, direction.distance):
                        self.current = Cube(self.current.x + 1, self.current.y, False)
                        if self.current in self.edge:
                            current_idx = self.edge.index(self.current)
                            self.edge[current_idx].is_vertical = False
                            self.shapes.append(Shape(self.edge[current_idx:]))
                            self.edge = self.edge[:current_idx]
                        self.edge.append(self.current)

    def calculate_area(self):
        y_coordinates = [cube[1] for cube in self.edge]
        area = 0

        for y in range(min(y_coordinates), max(y_coordinates) + 1):
            x_coordinates = [cube[0] for cube in self.edge if cube[1] == y]
            x_coordinates.sort()

            idx = 1
            while idx < len(x_coordinates):
                start = x_coordinates[idx]

                while idx < len(x_coordinates) and x_coordinates[idx - 1] + 1 == x_coordinates[idx]:
                    idx += 1

                idx += 1

                while idx < len(x_coordinates) and x_coordinates[idx - 1] + 1 == x_coordinates[idx]:
                    idx += 1

                end = x_coordinates[idx]
                area += end - start + 1

        return area


with open('input/day_18.txt') as file:
    file_content = file.read()

directions = re.findall(r'(\w) (\d+) \((#[abcdef0123456789]+)\)', file_content)
directions = [DigDirection(direction[0], int(direction[1]), direction[2]) for direction in directions]
lagoon = Lagoon(directions)
print('hi')
