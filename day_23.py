class Route:
    def __init__(self, current, visited_fields):
        self.current = current
        self.visited_fields = visited_fields

    def do_step(self, next_field):

        # get possible directions

        new_visited_fields = list(self.visited_fields)
        new_visited_fields.append(self.current)
        return Route(next_field, new_visited_fields)

    def generate_next_steps(self):
        return [self.do_step(neighbour) for neighbour in self.current.get_neighbours()]

    def __repr__(self):
        return f'{self.current} ({self.visited_fields})'


class MapField:
    def __init__(self, x=0, y=0, value='.', hiking_map=None):
        self.x = x
        self.y = y
        self.value = value
        self.map = hiking_map

    def get_neighbours(self):
        neighbours = [
            self.map.get(self.x + 1, self.y),
            self.map.get(self.x, self.y + 1),
            self.map.get(self.x - 1, self.y),
            self.map.get(self.x, self.y - 1),
        ]

        neighbours = list(filter(lambda n: n and n.value != '#', neighbours))

        for idx, neighbour in enumerate(neighbours):
            if not self.is_left_neighbour(neighbour) and neighbour.value == '<':
                neighbours[idx] = neighbour.get_left_neighbour()
            elif not self.is_right_neighbour(neighbour) and neighbour.value == '>':
                neighbours[idx] = neighbour.get_right_neighbour()
            elif not self.is_top_neighbour(neighbour) and neighbour.value == '^':
                neighbours[idx] = neighbour.get_top_neighbour()
            elif not self.is_bottom_neighbour(neighbour) and neighbour.value == 'v':
                neighbours[idx] = neighbour.get_bottom_neighbour()

        return list(filter(lambda n: n, neighbours))

    def get_left_neighbour(self):
        return self.map.get(self.x - 1, self.y)

    def is_left_neighbour(self, neighbour):
        return neighbour == self.map.get(self.x - 1, self.y)

    def get_right_neighbour(self):
        return self.map.get(self.x + 1, self.y)

    def is_right_neighbour(self, neighbour):
        return neighbour == self.map.get(self.x + 1, self.y)

    def get_top_neighbour(self):
        return self.map.get(self.x, self.y - 1)

    def is_top_neighbour(self, neighbour):
        return neighbour == self.map.get(self.x, self.y - 1)

    def get_bottom_neighbour(self):
        return self.map.get(self.x, self.y + 1)

    def is_bottom_neighbour(self, neighbour):
        return neighbour == self.map.get(self.x, self.y + 1)

    def __repr__(self):
        return f'({self.value} {self.x},{self.y})'


class HikingMap:
    def __init__(self, fields):
        self.fields = []

        for row_idx, line in enumerate(fields):
            self.fields.append([])
            for column_idx, field_val in enumerate(line.strip()):
                self.fields[-1].append(MapField(column_idx, row_idx, field_val, self))

        self.height = len(self.fields)
        self.width = len(self.fields[0])

    def get_start(self):
        for field in self.fields[0]:
            if field.value == '.':
                return field

    def get_end(self):
        for field in self.fields[-1]:
            if field.value == '.':
                return field

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.fields[y][x]

    def find_longest_route(self):
        route_candidates = [Route(self.get_start(), [])]
        max_length = 0
        while route_candidates:
            next_candidates = []
            for route in route_candidates:
                valid = False
                for candidate in route.generate_next_steps():
                    if candidate.current is self.get_end():
                        if len(candidate.visited_fields) > max_length:
                            max_length = len(candidate.visited_fields)
                            valid = True
                    elif candidate.current not in candidate.visited_fields:
                        next_candidates.append(candidate)
                        valid = True


            route_candidates = next_candidates

        return max_length


with open('input/day_23.txt') as file:
    hiking_map = HikingMap(file.readlines())

print(hiking_map.get_start())
print(hiking_map.get_end())

print(hiking_map.find_longest_route())
