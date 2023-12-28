import re
import sympy

MIN_LIMIT = 200000000000000
MAX_LIMIT = 400000000000000


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class HailStone:
    def __init__(self, start: Vector, velocity: Vector):
        self.start = start
        self.velocity = velocity

        self.gradient = self.velocity.y / self.velocity.x
        self.y0 = self._calculate_y0()

    def __repr__(self):
        return f'{self.start} @ {self.velocity}'

    def intersects_with(self, other):
        if (other.gradient - self.gradient) == 0:
            return False

        x = (other.y0 - self.y0) / (self.gradient - other.gradient)
        y = self.y0 + x * self.gradient

        if (self.velocity.x > 0 and x < self.start.x) or (self.velocity.x < 0 and x > self.start.x):
            return False

        if (other.velocity.x > 0 and x < other.start.x) or (other.velocity.x < 0 and x > other.start.x):
            return False

        return MIN_LIMIT <= x <= MAX_LIMIT and MIN_LIMIT <= y <= MAX_LIMIT

    def _calculate_y0(self):
        return self.start.y - self.start.x * self.gradient


with open('input/day_24.txt') as file:
    hail_stones = []
    for x, y, z, v_x, v_y, v_z in re.findall(
            r"(-?[0-9]+), +(-?[0-9]+), +(-?[0-9]+) @ +(-?[0-9]+), +(-?[0-9]+), +(-?[0-9]+)", file.read()):
        hail_stones.append(HailStone(Vector(int(x), int(y), int(z)), Vector(int(v_x), int(v_y), int(v_z))))

intersections = 0
for idx, hail_stone_a in enumerate(hail_stones):
    for hail_stone_b in hail_stones[idx + 1:]:
        if hail_stone_a.intersects_with(hail_stone_b):
            intersections += 1

rock_x, rock_y, rock_z, rock_velocity_x, rock_velocity_y, rock_velocity_z = sympy.symbols("rx, ry, rz, rvx, rvy, rvz")

equations = [
]

for stone in hail_stones:
    equations.append(
        sympy.Eq((stone.start.x - rock_x) * (rock_velocity_y - stone.velocity.y),
                 (stone.start.y - rock_y) * (rock_velocity_x - stone.velocity.x))
    )
    equations.append(
        sympy.Eq((stone.start.y - rock_y) * (rock_velocity_z - stone.velocity.z),
                 (stone.start.z - rock_z) * (rock_velocity_y - stone.velocity.y))
    )

solution = sympy.solve(equations)[0]
print(solution[rock_x] + solution[rock_y] + solution[rock_z])
