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


def first_digit(line):
    for start in range(0, len(line)):
        if line[start].isdigit():
            return line[start]
        for end in range(start+2, len(line)):
            if line[start: end] in digits:
                return digits[line[start: end]]


def last_digit(line):
    for end in range(len(line) - 1, -1, -1):
        if line[end].isdigit():
            return line[end]
        for start in range(end - 2, -1, -1):
            if line[start:end] in digits:
                return digits[line[start:end]]


with open('input/simple.txt') as file:
    lines = file.readlines()

    lines = map(lambda line: first_digit(line) + last_digit(line), lines)
    lines = map(lambda line: int(line), lines)

    print(sum(lines))
