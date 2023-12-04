import re

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14
}


class Game:
    def __init__(self, game_id, moves):
        self.id = game_id
        self.moves = moves

    def is_valid(self):
        return all(map(lambda m: m.is_valid(), self.moves))

    def calculate_power(self):
        min_cube_set = {}
        power = 1
        for move in self.moves:
            move.apply_to(min_cube_set)

        for value in min_cube_set.values():
            power *= value

        return power


class GameDraw:
    def __init__(self, cubes):
        self.cubes = cubes

    def is_valid(self):
        for color in self.cubes:
            if color in LIMITS:
                if self.cubes[color] > LIMITS[color]:
                    return False
        return True

    def apply_to(self, min_cube_set):
        for color in self.cubes:
            if color not in min_cube_set:
                min_cube_set[color] = self.cubes[color]
            elif self.cubes[color] > min_cube_set[color]:
                min_cube_set[color] = self.cubes[color]


def parse_game_line(line):
    game_tag, moves = line.split(':')

    game_id = int(re.search(r'(\d+)', game_tag).group)
    game_moves = parse_game_draws(moves)

    return Game(game_id, game_moves)


def parse_game_draws(moves_desc):
    moves = []

    for move_desc in moves_desc.split(';'):
        moves.append(parse_single_draw(move_desc))

    return moves


def parse_single_draw(move_desc):
    cubes = {}

    for colors in move_desc.split(','):
        count, color = colors.strip().split(' ')
        cubes[color.lower()] = int(count)

    return GameDraw(cubes)


with open("input/day_02.txt") as file:
    games = map(lambda line: parse_game_line(line), file.readlines())
    games = map(lambda g: g.calculate_power(), games)

print(sum(games))
