def aoc_hash(data):
    hash = 0
    for symbol in data:
        ascii_code = ord(symbol)
        hash += ascii_code
        hash *= 17
        hash %= 256
    return hash


class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, other):
        if type(other) == Lens:
            return other.label == self.label
        if type(other) == str:
            return other == self.label
        return False

    def __str__(self):
        return f"Lens {self.label} = {self.focal_length}"


with open("input/day_15.txt") as file:
    boxes = {}
    for idx in range(0, 256):
        boxes[idx] = []

    instructions = [inst.strip() for inst in file.read().split(',')]

    for instruction in instructions:

        if '-' in instruction:
            label = instruction.split('-')[0]
            if label in boxes[aoc_hash(label)]:
                boxes[aoc_hash(label)].remove(label)
        else:
            label, focal_length = instruction.split('=')
            new_lens = Lens(label, int(focal_length))
            if label in boxes[aoc_hash(label)]:
                idx = boxes[aoc_hash(label)].index(label)
                boxes[aoc_hash(label)][idx].focal_length = int(focal_length)
            else:
                boxes[aoc_hash(label)].append(new_lens)

    result = 0

    for key in boxes:
        for lens_pos in range(0, len(boxes[key])):
            lens = boxes[key][lens_pos]
            result += (key+1) * (lens_pos+1) * lens.focal_length

    print(result)
