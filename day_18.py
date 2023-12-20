import re


class DigDirection:

    def __init__(self, hex_code):
        match hex_code[-1]:
            case '0':
                self.orientation = 'R'
            case '1':
                self.orientation = 'D'
            case '2':
                self.orientation = 'L'
            case '3':
                self.orientation = 'U'

        self.distance = int(hex_code[1:-1], base=16)

    def __str__(self):
        return f"{self.orientation} {self.distance} {self.color}"


class Shape:
    def __init__(self, dig_directions):
        self.nodes = [(0, 0)]
        self._generate_nodes(dig_directions)
        self.nodes = self.nodes[:-1]
        self.expand()

    def _generate_nodes(self, dig_directions):
        idx = 0
        while idx < len(dig_directions):
            current = self.nodes[-1]
            direction = dig_directions[idx]

            match direction.orientation:
                case 'U':
                    new_x = current[0]
                    new_y = current[1] - direction.distance

                    self.nodes.append((new_x, new_y))
                case 'D':
                    new_x = current[0]
                    new_y = current[1] + direction.distance

                    self.nodes.append((new_x, new_y))
                case 'L':
                    new_x = current[0] - direction.distance
                    new_y = current[1]

                    self.nodes.append((new_x, new_y))
                case 'R':
                    new_x = current[0] + direction.distance
                    new_y = current[1]

                    self.nodes.append((new_x, new_y))

            idx += 1

    def expand(self):
        nodes = [(x + 0.5, y + 0.5) for x, y in self.nodes]

        idx = 0
        while idx < len(self.nodes):
            previous = self.nodes[idx - 1]
            current = self.nodes[idx]
            successor = self.nodes[(idx + 1) % len(self.nodes)]

            # bottom -> right
            if previous[1] > current[1] and current[0] < successor[0]:
                nodes[idx] = (nodes[idx][0] - 0.5, nodes[idx][1] - 0.5)

            # top -> left
            if previous[1] < current[1] and current[0] > successor[0]:
                nodes[idx] = (nodes[idx][0] + 0.5, nodes[idx][1] + 0.5)

            # top -> right
            if previous[1] < current[1] and current[0] < successor[0]:
                nodes[idx] = (nodes[idx][0] + 0.5, nodes[idx][1] - 0.5)

            # bottom -> left
            if previous[1] > current[1] and current[0] > successor[0]:
                nodes[idx] = (nodes[idx][0] - 0.5, nodes[idx][1] + 0.5)

            # right -> bottom
            if previous[0] > current[0] and current[1] < successor[1]:
                nodes[idx] = (nodes[idx][0] + 0.5, nodes[idx][1] + 0.5)

            # left -> top
            if previous[0] < current[0] and current[1] > successor[1]:
                nodes[idx] = (nodes[idx][0] - 0.5, nodes[idx][1] - 0.5)

            # left -> bottom
            if previous[0] < current[0] and current[1] < successor[1]:
                nodes[idx] = (nodes[idx][0] + 0.5, nodes[idx][1] - 0.5)

            # right -> top
            if previous[0] > current[0] and current[1] > successor[1]:
                nodes[idx] = (nodes[idx][0] - 0.5, nodes[idx][1] + 0.5)

            idx += 1

        self.nodes = nodes

    def calc_area(self):
        print(self.nodes)
        prev_node = self.nodes[-1]
        area = 0
        for node in self.nodes:
            area += (prev_node[1] + node[1]) * (prev_node[0] - node[0])
            prev_node = node
        return area / 2


with open('input/day_18.txt') as file:
    file_content = file.read()

directions = re.findall(r'(\w) (\d+) \((#[abcdef0123456789]+)\)', file_content)
directions = [DigDirection(direction[2]) for direction in directions]
lagoon = Shape(directions)

# print_edge(lagoon.edge, False)
print(lagoon.calc_area())
