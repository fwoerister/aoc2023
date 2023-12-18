import heapq

MAX_TRAVEL_DISTANCE = 10


class Route:
    def __init__(self, blocks, heat_loss_map):
        self.blocks = blocks
        self.heat_loss = sum([block.heat_loss for block in blocks[1:]])
        self.heat_loss_map = heat_loss_map

    def __add__(self, other):
        return Route(self.blocks + other.blocks, self.heat_loss_map)

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss

    def __str__(self):
        return str([str(block) for block in self.blocks]) + " - " + str(self.heat_loss)

    def tail(self):
        return self.blocks[-1]

    def generate_reachable_fields_north(self):
        result = []

        if self.is_moving_south():
            return result

        if self.is_moving_east() and self.distance_since_last_turn() < 4:
            return result

        if self.is_moving_west() and self.distance_since_last_turn() < 4:
            return result

        traveled_distance = self.distance_since_last_turn() if self.is_moving_north() else 0

        offset = max(4 - traveled_distance, 1)

        x = self.tail().x
        y = self.tail().y - offset

        for count in range(0, min(MAX_TRAVEL_DISTANCE - traveled_distance, 6)):
            reachable_block = self.heat_loss_map.get(x, y)
            if reachable_block and reachable_block not in self.heat_loss_map.visited_blocks:
                result.append(reachable_block)
            y -= 1

        return result

    def generate_reachable_fields_south(self):
        result = []

        if self.is_moving_north():
            return result

        if self.is_moving_east() and self.distance_since_last_turn() < 4:
            return result

        if self.is_moving_west() and self.distance_since_last_turn() < 4:
            return result

        traveled_distance = self.distance_since_last_turn() if self.is_moving_south() else 0

        offset = max(4 - traveled_distance, 1)

        x = self.tail().x
        y = self.tail().y + offset

        for count in range(0, min(MAX_TRAVEL_DISTANCE - traveled_distance, 6)):
            reachable_block = self.heat_loss_map.get(x, y)
            if reachable_block and reachable_block not in self.heat_loss_map.visited_blocks:
                result.append(reachable_block)
            y += 1

        return result

    def generate_reachable_fields_west(self):
        result = []

        if self.is_moving_east():
            return result

        if self.is_moving_north() and self.distance_since_last_turn() < 4:
            return result

        if self.is_moving_south() and self.distance_since_last_turn() < 4:
            return result

        traveled_distance = self.distance_since_last_turn() if self.is_moving_west() else 0

        offset = max(4 - traveled_distance, 1)

        x = self.tail().x - offset
        y = self.tail().y

        for count in range(0, min(MAX_TRAVEL_DISTANCE - traveled_distance, 6)):
            reachable_block = self.heat_loss_map.get(x, y)
            if reachable_block and reachable_block not in self.heat_loss_map.visited_blocks:
                result.append(reachable_block)
            x -= 1
        return result

    def generate_reachable_fields_east(self):
        result = []

        if self.is_moving_west():
            return result

        if self.is_moving_north() and self.distance_since_last_turn() < 4:
            return result

        if self.is_moving_south() and self.distance_since_last_turn() < 4:
            return result

        traveled_distance = self.distance_since_last_turn() if self.is_moving_east() else 0

        offset = max(4 - traveled_distance, 1)

        x = self.tail().x + offset
        y = self.tail().y

        for count in range(0, min(MAX_TRAVEL_DISTANCE - traveled_distance, 6)):
            reachable_block = self.heat_loss_map.get(x, y)
            if reachable_block and reachable_block not in self.heat_loss_map.visited_blocks:
                result.append(reachable_block)
            x += 1

        return result

    def is_moving_north(self):
        if len(self.blocks) < 2:
            return False

        if self.blocks[-2].y > self.blocks[-1].y and self.blocks[-2].x == self.blocks[-1].x:
            return True

        return False

    def is_moving_south(self):
        if len(self.blocks) < 2:
            return False

        if self.blocks[-2].y < self.blocks[-1].y and self.blocks[-2].x == self.blocks[-1].x:
            return True

        return False

    def is_moving_west(self):
        if len(self.blocks) < 2:
            return False

        if self.blocks[-2].y == self.blocks[-1].y and self.blocks[-2].x > self.blocks[-1].x:
            return True

        return False

    def is_moving_east(self):
        if len(self.blocks) < 2:
            return False

        if self.blocks[-2].y == self.blocks[-1].y and self.blocks[-2].x < self.blocks[-1].x:
            return True

        return False

    def distance_since_last_turn(self):
        last_x = self.blocks[-1].x
        last_y = self.blocks[-1].y
        idx = len(self.blocks) - 2
        distance = 0

        if self.is_moving_north() or self.is_moving_south():
            while idx >= 0 and self.blocks[idx].x == last_x:
                distance += 1
                idx -= 1

        if self.is_moving_west() or self.is_moving_east():
            while idx >= 0 and self.blocks[idx].y == last_y:
                distance += 1
                idx -= 1

        return distance


class MapBlock:
    def __init__(self, x, y, heat_loss=0):
        self.x = x
        self.y = y
        self.heat_loss = heat_loss

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x}{self.y}{self.heat_loss}")


class HeatLossMap:
    def __init__(self, values):
        self.blocks = self._parse_map_lines(values)
        self.visited_blocks = set()
    def _parse_map_lines(self, lines):
        parsed_map = []
        for column_idx in range(0, len(lines[0].strip())):
            parsed_map.append([])
            for row_idx in range(0, len(lines)):
                new_block = MapBlock(column_idx, row_idx, int(lines[row_idx][column_idx]))
                parsed_map[column_idx].append(new_block)
        return parsed_map

    def get(self, x, y):
        if 0 <= x < len(self.blocks):
            if 0 <= y < len(self.blocks[0]):
                return self.blocks[x][y]
        return None

    def get_optimal_path(self, start, target):
        self.visited_blocks.add(start)


        heapq.heapify([])

        return self._get_optimal_path([Route([start], self)], target)

    def _get_optimal_path(self, current_routes, target):

        while target not in self.visited_blocks:
            optimal_route = heapq.heappop(current_routes)

            north_moves = optimal_route.generate_reachable_fields_north()
            if any(north_moves):
                next_step = self.get(optimal_route.tail().x, optimal_route.tail().y - 1)
                self.visited_blocks.add(next_step)
                heapq.heappush(current_routes, optimal_route + Route([next_step], self))

            east_moves = optimal_route.generate_reachable_fields_east()
            if any(east_moves):
                next_step = self.get(optimal_route.tail().x + 1, optimal_route.tail().y)
                self.visited_blocks.add(next_step)
                heapq.heappush(current_routes, optimal_route + Route([next_step], self))

            south_moves = optimal_route.generate_reachable_fields_south()
            if any(south_moves):
                next_step = self.get(optimal_route.tail().x, optimal_route.tail().y + 1)
                self.visited_blocks.add(next_step)
                heapq.heappush(current_routes, optimal_route + Route([next_step], self))

            west_moves = optimal_route.generate_reachable_fields_west()
            if any(west_moves):
                next_step = self.get(optimal_route.tail().x - 1, optimal_route.tail().y)
                self.visited_blocks.add(next_step)
                heapq.heappush(current_routes, optimal_route + Route([next_step], self))

        for r in current_routes:
            if r.tail() == target:
                return r


def draw_route(route, width, height):
    for y_idx in range(0, height):
        for x_idx in range(0, width):
            if MapBlock(x_idx, y_idx) in route.blocks:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('')


with open("input/day_17.txt") as file:
    lines = file.readlines()

heat_loss_map = HeatLossMap(lines)

start = heat_loss_map.blocks[0][0]
target = heat_loss_map.blocks[len(heat_loss_map.blocks) - 1][len(heat_loss_map.blocks[0]) - 1]

route = heat_loss_map.get_optimal_path(start, target)

draw_route(route, len(heat_loss_map.blocks), len(heat_loss_map.blocks[0]))
print(route.heat_loss)
