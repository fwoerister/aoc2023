from heapq import heappush, heappop


class MapBlock:
    def __init__(self, x, y, heat_loss=0):
        self.x = x
        self.y = y
        self.heat_loss = heat_loss

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class State:
    def __init__(self, trace):
        self.current_block = trace[-1]
        self.trace = trace
        self.heat_loss = self.calculate_heat_loss()

    def __eq__(self, other):
        return (self.current_block == other.current_block
                and self.calculate_direction() == other.calculate_direction()
                and self.distance_since_last_turn() == other.distance_since_last_turn())

    def __hash__(self):
        return hash(f"{self.current_block} - {self.calculate_direction()} - {self.distance_since_last_turn()}")

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss

    def __str__(self):
        return str([str(block) for block in self.trace]) + " - " + str(self.calculate_heat_loss())

    def calculate_direction(self):
        if len(self.trace) <= 1:
            return 0, 0
        return self.trace[-1].x - self.trace[-2].x, self.trace[-1].y - self.trace[-2].y

    def calculate_heat_loss(self):
        if len(self.trace) <= 1:
            return 0

        return sum([block.heat_loss for block in self.trace[1:]])

    def tail(self):
        return self.trace[-1]

    def is_moving_north(self):
        return self.calculate_direction() == (0, -1)

    def is_moving_south(self):
        return self.calculate_direction() == (0, 1)

    def is_moving_west(self):
        return self.calculate_direction() == (-1, 0)

    def is_moving_east(self):
        return self.calculate_direction() == (1, 0)

    def distance_since_last_turn(self):
        last_x = self.trace[-1].x
        last_y = self.trace[-1].y
        idx = len(self.trace) - 2
        distance = 0

        if self.is_moving_north() or self.is_moving_south():
            while idx >= 0 and self.trace[idx].x == last_x:
                distance += 1
                idx -= 1

        if self.is_moving_west() or self.is_moving_east():
            while idx >= 0 and self.trace[idx].y == last_y:
                distance += 1
                idx -= 1

        return distance


class HeatLossGrid:
    def __init__(self, values):
        self.blocks = self._parse_map_lines(values)
        self.width = len(self.blocks)
        self.height = len(self.blocks[0])

        self.visited_blocks = set()

    def _parse_map_lines(self, lines):
        parsed_map = []
        for column_idx in range(0, len(lines[0].strip())):
            parsed_map.append([])
            for row_idx in range(0, len(lines)):
                new_block = MapBlock(column_idx, row_idx, int(lines[row_idx][column_idx]))
                parsed_map[column_idx].append(new_block)
        return parsed_map

    def get(self, x, y) -> MapBlock:
        if 0 <= x < len(self.blocks):
            if 0 <= y < len(self.blocks[0]):
                return self.blocks[x][y]
        return None

    def calculate_minimum_heat_loss(self, start, target, min_moves=1, max_moves=3):
        self.visited_blocks = set()
        active_states = [State([start])]

        while active_states:
            state = heappop(active_states)
            state_direction = state.calculate_direction()
            state_distance_since_last_turn = state.distance_since_last_turn()

            if state.current_block == target and state_distance_since_last_turn >= min_moves:
                return state

            if state in self.visited_blocks:
                continue

            self.visited_blocks.add(state)

            if state_distance_since_last_turn < max_moves and state_direction != (0, 0):
                new_block = self.get(state.current_block.x + state_direction[0],
                                     state.current_block.y + state_direction[1])
                if new_block:
                    new_state = State(state.trace + [new_block])
                    heappush(active_states, new_state)

            if state_distance_since_last_turn >= min_moves or state_direction == (0, 0):
                for ndx, ndy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if (ndx, ndy) != state_direction and (ndx, ndy) != (-state_direction[0], -state_direction[1]):
                        new_block = self.get(state.current_block.x + ndx, state.current_block.y + ndy)
                        if new_block:
                            new_state = State(state.trace + [new_block])
                            heappush(active_states, new_state)


def draw_state(state, width, height):
    for y_idx in range(0, height):
        for x_idx in range(0, width):
            if MapBlock(x_idx, y_idx) in state.trace:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print(f'heat loss: {state.calculate_heat_loss()}\n')


with open("input/day_17.txt") as file:
    lines = file.readlines()

heat_loss_map = HeatLossGrid(lines)

start_block = heat_loss_map.blocks[0][0]
target_block = heat_loss_map.blocks[len(heat_loss_map.blocks) - 1][len(heat_loss_map.blocks[0]) - 1]

state = heat_loss_map.calculate_minimum_heat_loss(start_block, target_block, min_moves=1, max_moves=3)
draw_state(state, heat_loss_map.width, heat_loss_map.height)

state = heat_loss_map.calculate_minimum_heat_loss(start_block, target_block, min_moves=4, max_moves=10)
draw_state(state, heat_loss_map.width, heat_loss_map.height)
