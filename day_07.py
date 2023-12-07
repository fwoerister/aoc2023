import re
from datetime import datetime

VALID_CARDS_PART1 = "23456789TJQKA"
VALID_CARDS_PART2 = "J23456789TQKA"


def calculate_card_statistic(draw):
    stat = {}
    for c in draw:
        stat[c] = stat.get(c, 0) + 1
    return stat


def assign_jokers(current_freqs, target_freqs, jokers):
    for idx in range(0, len(current_freqs)):
        while current_freqs[idx] < target_freqs[idx] and jokers > 0:
            current_freqs[idx] += 1
            jokers -= 1

    return current_freqs


def matches_freq_pattern(draw, target_pattern, play_with_jokers=False):
    card_stat = calculate_card_statistic(draw)
    card_freqs = list(card_stat.values())
    card_freqs.sort()

    joker_count = 0
    if play_with_jokers and "J" in draw:
        joker_count = draw.count("J")
        card_freqs.remove(joker_count)

    while len(card_freqs) < len(target_pattern):
        card_freqs = [0] + card_freqs

    if len(card_freqs) == len(target_pattern):
        return assign_jokers(card_freqs, target_pattern, joker_count) == target_pattern

    return False


class Draw:
    def __init__(self, cards, bit, card_order):
        self.cards = cards
        self.bit = bit
        self.card_order = card_order

    def get_card_values(self):
        return [self.card_order.index(card) for card in self.cards]

    def __lt__(self, other):
        if type(self).draw_type_order < other.draw_type_order:
            return True
        elif self.draw_type_order > other.draw_type_order:
            return False

        idx = 0
        my_card_vals = self.get_card_values()
        other_card_vals = other.get_card_values()

        while idx < len(self.cards):
            if my_card_vals[idx] != other_card_vals[idx]:
                return my_card_vals[idx] < other_card_vals[idx]
            idx += 1


class FiveOfAKind(Draw):
    draw_type_order = 6

    def __str__(self):
        return f"FiveOfAKind {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [5], play_with_jokers)


class FourOfAKind(Draw):
    draw_type_order = 5

    def __str__(self):
        return f"FourOfAKind {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [1, 4], play_with_jokers)


class FullHouse(Draw):
    draw_type_order = 4

    def __str__(self):
        return f"FullHouse {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [2, 3], play_with_jokers)


class ThreeOfAKind(Draw):
    draw_type_order = 3

    def __str__(self):
        return f"ThreeOfAKind {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [1, 1, 3], play_with_jokers)


class TwoPair(Draw):
    draw_type_order = 2

    def __str__(self):
        return f"TwoPair {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [1, 2, 2], play_with_jokers)


class OnePair(Draw):
    draw_type_order = 1

    def __str__(self):
        return f"OnePair {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return matches_freq_pattern(draw, [1, 1, 1, 2], play_with_jokers)


class HighCard(Draw):
    draw_type_order = 0

    def __str__(self):
        return f"HighCard {self.cards} {self.bit}"

    @staticmethod
    def is_type_of(draw, play_with_jokers):
        return True


class DrawFactory:
    def __init__(self, play_with_jokers=False):
        self.play_with_jokers = play_with_jokers
        self.draw_types = [
            FiveOfAKind,
            FourOfAKind,
            FullHouse,
            ThreeOfAKind,
            TwoPair,
            OnePair,
            HighCard
        ]

    def create_from_line(self, line, bit, card_order):
        for _type in self.draw_types:
            if _type.is_type_of(line, self.play_with_jokers):
                return _type(line, bit, card_order)


print('part 1:')
start_ts = datetime.now().timestamp()
with open('input/day_07.txt') as file:
    content = "".join(file.readlines())

draws = []
factory = DrawFactory(play_with_jokers=False)

for draw in re.findall(r"([23456789TJQKA]{5}) (\d+)", content):
    draws.append(factory.create_from_line(draw[0], int(draw[1]), VALID_CARDS_PART1))

draws.sort()
result = 0
for idx in range(0, len(draws)):
    result += (idx + 1) * draws[idx].bit

print(result)
end_ts = datetime.now().timestamp()

print(f"{end_ts - start_ts}s")

print('part 2:')
start_ts = datetime.now().timestamp()
with open('input/day_07.txt') as file:
    content = "".join(file.readlines())

draws = []
factory = DrawFactory(play_with_jokers=True)

for draw in re.findall(r"([23456789TJQKA]{5}) (\d+)", content):
    draws.append(factory.create_from_line(draw[0], int(draw[1]), VALID_CARDS_PART2))

draws.sort()
result = 0
for idx in range(0, len(draws)):
    result += (idx + 1) * draws[idx].bit

print(result)
end_ts = datetime.now().timestamp()

print(f"{end_ts - start_ts}s")
