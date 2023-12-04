import re


class ScratchCard:
    def __init__(self, scratchcard_line):
        tag, values = scratchcard_line.split(':')
        self.card_id = int(re.search(r"(\d+)", tag).group())
        self.winning_numbers, self.card_numbers = values.split('|')

        self.winning_numbers = set(re.findall(r"(\d+)", self.winning_numbers))
        self.card_numbers = set(re.findall(r"(\d+)", self.card_numbers))

    def calculate_copies(self, scratch_cards):
        start = self.card_id + 1
        end = min(start + self.calculate_matching_count(), len(scratch_cards) + 1)
        return range(start, end)

    def calculate_points(self):
        matching_numbers = self.calculate_matching_count()
        return 2 ** (matching_numbers - 1) if matching_numbers >= 1 else 0

    def calculate_matching_count(self):
        return len([n for n in self.card_numbers if n in self.winning_numbers])


with open('input/day_04.txt') as file:
    cards = {}
    copies = {}

    for line in file.readlines():
        card = ScratchCard(line)
        cards[card.card_id] = card
        copies[card.card_id] = 1

    for card_id in cards:
        for copy_id in cards[card_id].calculate_copies(cards):
            copies[copy_id] += copies[card_id]

    print(sum(copies.values()))
