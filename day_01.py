from datetime import datetime
import timeit

digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def first_digit(line, digit_dict):
    for start in range(0, len(line)):
        if line[start].isdigit():
            return line[start]
        for end in range(start + 2, len(line)):
            if line[start: end] in digit_dict:
                return digit_dict[line[start: end]]


def last_digit(line, digit_dict):
    for end in range(len(line) - 1, -1, -1):
        if line[end].isdigit():
            return line[end]
        for start in range(end - 2, -1, -1):
            if line[start:end] in digit_dict:
                return digit_dict[line[start:end]]


def do_part_1(lines):
    lines = map(lambda line: first_digit(line, {}) + last_digit(line, {}), lines)
    lines = map(lambda line: int(line), lines)
    return sum(lines)


def do_part_2(lines):
    lines = map(lambda line: first_digit(line, digits) + last_digit(line, digits), lines)
    lines = map(lambda line: int(line), lines)
    return sum(lines)


with open('input/day_01.txt') as file:
    lines = file.readlines()

result = do_part_1(lines)
avg_time = timeit.timeit(lambda: do_part_1(lines), number=100) / 100

print('part 1:')
print(f"result: {result}")
print(f"avg execution time: {avg_time}s")

result = do_part_2(lines)
avg_time = timeit.timeit(lambda: do_part_2(lines), number=100) / 100

print('part 2:')
print(f"result: {result}")
print(f"avg execution time: {avg_time}s")
