import re


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Block:

    def __init__(self, start: Cube, end: Cube):
        self.start = start
        self.end = end
        self.supported_by = []
        self.supports = []
        self.z_slice = self._calc_z_slice()

    def _calc_z_slice(self) -> set:
        if self.start.x == self.end.x:
            return set([(self.start.x, y) for y in range(self.start.y, self.end.y + 1)])
        else:
            return set([(x, self.start.y) for x in range(self.start.x, self.end.x + 1)])

    def intersects_with(self, other):
        if len(self.z_slice.intersection(other.z_slice)) != 0:
            return True
        return False

    def __repr__(self):
        return f'Block {id(self)} ({self.start} -> {self.end})'

    def __lt__(self, other):
        return self.start.z < other.start.z


def path_exists(start_blocks, target_block, excluded_blocks):
    for block in start_blocks:
        if block == target_block:
            return True
        elif block in excluded_blocks:
            return False
        else:
            return path_exists(block.suports, target_block, excluded_blocks)


def parse_blocks(file_content):
    pattern = r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)'
    blocks = []
    for x_start, y_start, z_start, x_end, y_end, z_end in re.findall(pattern, file_content):
        start = Cube(int(x_start), int(y_start), int(z_start))
        end = Cube(int(x_end), int(y_end), int(z_end))
        blocks.append(Block(start, end))
    return blocks


with open('input/day_22.txt') as file:
    conent = file.read()

blocks = parse_blocks(conent)
blocks.sort()

for idx, block in enumerate(blocks):
    max_z = 0
    for fallen_block in blocks[:idx]:
        if fallen_block.intersects_with(block) and fallen_block.end.z > max_z:
            max_z = fallen_block.end.z
            supporting_blocks = [fallen_block]
        if fallen_block.intersects_with(block) and fallen_block.end.z == max_z:
            supporting_blocks.append(fallen_block)

    z_diff = block.start.z - (max_z + 1)
    block.start.z -= z_diff
    block.end.z -= z_diff

for idx, block in enumerate(blocks):
    for lower_block in blocks[:idx]:
        if lower_block.intersects_with(block) and lower_block.end.z == block.start.z - 1:
            lower_block.supports.append(block)
            block.supported_by.append(lower_block)

removable_blocks = 0

for block in blocks:
    if not block.supports:
        removable_blocks += 1
    elif all([len(b.supported_by) > 1 for b in block.supports]):
        removable_blocks += 1
print(removable_blocks)


def find_reachable_blocks(starting_blocks, excluded_block):
    result = list(starting_blocks)
    for block in starting_blocks:
        if block is not excluded_block:
            result.append(block)
            result = result + find_reachable_blocks(block.supports, excluded_block)
    return result


starting_blocks = [block for block in blocks if block.start.z == 1]

count = 0
for block in blocks:
    count += len(blocks) - len(set(find_reachable_blocks(list(starting_blocks), block)))

print(count)
