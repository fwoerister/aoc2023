class Galaxy:
    def __init__(self, x, y, galaxy_id):
        self.x = x
        self.y = y
        self.id = galaxy_id

    def __str__(self):
        return f"{self.id} - {self.x} {self.y}"

    def distance_to(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)


class GalaxyMap:
    def __init__(self, galaxies):
        self.galaxies = galaxies

    def __str__(self):
        return str(list(map(lambda elem: str(elem), self.galaxies)))

    def get_width(self):
        return max([galaxy.x for galaxy in self.galaxies])

    def get_height(self):
        return max([galaxy.y for galaxy in self.galaxies])

    def get_occupied_rows(self):
        return set([galaxy.x for galaxy in self.galaxies])

    def get_occupied_colums(self):
        return set([galaxy.y for galaxy in self.galaxies])

    def expand(self, delta=1):
        current_x = 0
        while current_x < self.get_width():
            if current_x not in self.get_occupied_rows():
                for galaxy in [galaxy for galaxy in self.galaxies if galaxy.x > current_x]:
                    galaxy.x += delta-1
                current_x += delta-1
            current_x += 1

        current_y = 0
        while current_y < self.get_height():
            if current_y not in self.get_occupied_colums():
                for galaxy in [galaxy for galaxy in self.galaxies if galaxy.y > current_y]:
                    galaxy.y += delta-1
                current_y += delta-1
            current_y += 1

    def find_shortest_distance(self):
        distances = 0
        for galaxy in self.galaxies:
            for other_galaxy in [other for other in self.galaxies if other.id > galaxy.id]:
                distances += galaxy.distance_to(other_galaxy)
        return distances


def parse_galaxies(lines):
    galaxies = []
    galaxy_id = 1
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] == "#":
                galaxies.append(Galaxy(x, y, galaxy_id))
                galaxy_id += 1
    return GalaxyMap(galaxies)


with open('input/day_11.txt') as file:
    galaxies = parse_galaxies(file.readlines())

galaxy_dict = {}
for g in galaxies.galaxies:
    galaxy_dict[g.id] = g

print(galaxies)
galaxies.expand(1000000)
print(galaxies)
print(galaxies.find_shortest_distance())
