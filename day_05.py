import re
import datetime


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"

    def intersects_with(self, other: "Range") -> bool:
        return self.start < other.end and self.end > other.start

    def intersection(self, other: "Range") -> "Range":
        return Range(max(self.start, other.start), min(self.end, other.end))

    def left_remainder(self, other: "Range") -> "Range":
        if self.start <= other.start - 1:
            return Range(self.start, other.start - 1)

    def right_remainder(self, other: "Range") -> "Range":
        if other.end + 1 <= self.end:
            return Range(other.end + 1, self.end)


class MappedRange(Range):
    def __init__(self, start: int, end: int, offset: int):
        super().__init__(start, end)
        self.offset = offset

    def __str__(self) -> str:
        return f"{self.start} - {self.end} ({self.offset})"

    def translate_range(self, other: Range) -> (list, Range, list):
        if self.intersects_with(other):
            intersection = other.intersection(self)
            intersection.start += self.offset
            intersection.end += self.offset

            return other.left_remainder(self), intersection, other.right_remainder(self)

        return None, None, None  # left_remainder, intersection, right_remainder


class MappingStage:
    def __init__(self, mapped_ranges: list):
        self.mapped_ranges = mapped_ranges

    def apply(self, seed_ranges: list) -> list:
        result = []
        for seed_range in seed_ranges:
            mapped_intersection, remainders = self._apply_mapped_ranges(seed_range)
            seed_ranges.extend(remainders)
            result.append(mapped_intersection if mapped_intersection is not None else seed_range)

        return result

    def _apply_mapped_ranges(self, seed_range: Range) -> (Range, list):
        for mapped_range in self.mapped_ranges:

            left_remainder, mapped_intersection, right_remainder = mapped_range.translate_range(seed_range)

            remainders = []
            if left_remainder:
                remainders.append(left_remainder)

            if right_remainder:
                remainders.append(right_remainder)

            if mapped_intersection:
                return mapped_intersection, remainders
                
        return None, []


def parse_seeds_part_1(f):
    line = f.readline()
    tag, seed_numbers = line.split(':')
    
    return [Range(int(start), int(start)) for start in re.findall(r'(\d+)', seed_numbers)]


def parse_seeds_part_2(f):
    line = f.readline()
    tag, seed_numbers = line.split(':')
    
    return [Range(int(start), int(start) + int(end) - 1) for start, end in re.findall(r'(\d+) (\d+)', seed_numbers)]


def parse_mapping_stages(f) -> list:
    content = "".join(f.readlines())
    raw_stages = re.findall(r"map:\n((?:\d+ \d+ \d+\n)+)", content)

    return [parse_stage(stage) for stage in raw_stages]


def parse_stage(raw_stage):
    ranges = []
    for m in re.findall(r"(\d+) (\d+) (\d+)\n", raw_stage):
        destination = int(m[0])
        source = int(m[1])
        length = int(m[2])
        ranges.append(MappedRange(source, source + length - 1, destination - source))
        
    return MappingStage(ranges)


print('part 1:')
start_ts = datetime.datetime.now().timestamp()

with open('input/day_05.txt') as file:
    seeds = parse_seeds_part_1(file)
    mapping_stages = parse_mapping_stages(file)

for stage in mapping_stages:
    seeds = stage.apply(seeds)

print(min(map(lambda r: r.start, seeds)))

end_ts = datetime.datetime.now().timestamp()
print(f"{end_ts - start_ts}s\n")

print("part 2:")
start_ts = datetime.datetime.now().timestamp()

with open('input/day_05.txt') as file:
    seeds = parse_seeds_part_2(file)
    mapping_stages = parse_mapping_stages(file)

for stage in mapping_stages:
    seeds = stage.apply(seeds)

print(min(map(lambda r: r.start, seeds)))

end_ts = datetime.datetime.now().timestamp()
print(f"{end_ts - start_ts}s")
