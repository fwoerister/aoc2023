import re
from datetime import datetime

values = []


def differentiate(values):
    result = []
    last_val = values[0]
    for val in values[1:]:
        result.append(val - last_val)
        last_val = val
    return result


def predict_next_val(values):
    difference_levels = calculate_difference_levels(values)
    return values[-1] + sum([val[-1] for val in difference_levels])


def predict_new_first_val(values):
    difference_levels = calculate_difference_levels(values)
    difference_levels.reverse()

    subtract_val = 0
    for diff in difference_levels:
        subtract_val = diff[0] - subtract_val

    return values[0] - subtract_val


def calculate_difference_levels(values):
    difference_levels = []
    current = values
    while not all_equal(current):
        difference_levels.append(differentiate(current))
        current = difference_levels[-1]
    return difference_levels


def all_equal(values: list):
    return len(set(values)) == 1


with open('input/day_09.txt') as file:
    for line in file.readlines():
        values.append([int(val) for val in re.findall(r"([-\d]+)", line)])

start_ts = datetime.now().timestamp()
print("part 1:")
print(sum([predict_next_val(val) for val in values]))
end_ts = datetime.now().timestamp()
print(f"{end_ts - start_ts}s \n")

start_ts = datetime.now().timestamp()
print("part 2:")
print(sum([predict_new_first_val(val) for val in values]))
end_ts = datetime.now().timestamp()
print(f"{end_ts - start_ts}s \n")
