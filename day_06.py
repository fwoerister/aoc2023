import datetime
import math
import re


def calc_possible_ways_to_win(t, d):
    min_button_time = math.ceil((-t + math.sqrt(t ** 2 - 4 * d)) / -2)
    max_button_time = math.floor((-t - math.sqrt(t ** 2 - 4 * d)) / -2)

    min_button_time = max(min_button_time, 0)
    max_button_time = min(max_button_time, t)

    ways = (max_button_time - min_button_time) + 1

    if (t - min_button_time) * min_button_time == d:
        ways -= 2

    return ways


print("part 1:")
start = datetime.datetime.now().timestamp()
with open('input/day_06.txt') as file:
    times = [int(t) for t in re.findall(r"(\d+)", file.readline())]
    distances = [int(d) for d in re.findall(r"(\d+)", file.readline())]

possibilities = 1
for idx in range(0, len(times)):
    possibilities *= calc_possible_ways_to_win(times[idx], distances[idx])

print(possibilities)
end = datetime.datetime.now().timestamp()
print(f"time: {end - start}s\n")

print("part 2:")
start = datetime.datetime.now().timestamp()
with open('input/day_06.txt') as file:
    time = int("".join(re.findall(r"(\d)", file.readline())))
    distance = int("".join(re.findall(r"(\d)", file.readline())))

print(calc_possible_ways_to_win(time, distance))

end = datetime.datetime.now().timestamp()
print(f"time: {end - start}s")
