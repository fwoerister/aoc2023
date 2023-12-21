import re
import copy

WORKFLOW_DICT = dict()

ACCEPTED = []
REJECTED = []


class Range:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def __str__(self):
        return f"({self.min}, {self.max})"


class Rule:
    @staticmethod
    def fromString(checker_str):
        equation, workflow = checker_str.split(':')
        if '>' in equation:
            category, value = equation.split('>')
            return GreaterThanRule(category, int(value), workflow)
        else:
            category, value = equation.split('<')
            return LessThanRule(category, int(value), workflow)


class GreaterThanRule(Rule):
    def __init__(self, category, limit, workflow):
        self.category = category
        self.limit = limit
        self.workflow = workflow

    def check_rating(self, rating):
        return self.workflow if rating[self.category] > self.limit else None

    def calculate_remainder(self, rating):
        remainder = copy.deepcopy(rating)
        remainder[self.category].max = min(rating[self.category].max, self.limit+1)
        remainder[self.category].min = min(rating[self.category].min, self.limit+1)
        return remainder

    def apply_to_rating_range(self, rating: dict):
        rating[self.category].min = max(rating[self.category].min, self.limit+1)
        rating[self.category].max = max(rating[self.category].max, self.limit+1)

    def __str__(self):
        return f"{self.category} > {self.limit} -> {self.workflow}"


class LessThanRule(Rule):
    def __init__(self, category, limit, workflow):
        self.category = category
        self.limit = limit
        self.workflow = workflow

    def check_rating(self, rating):
        return self.workflow if rating[self.category] < self.limit else None

    def calculate_remainder(self, rating):
        remainder = copy.deepcopy(rating)
        remainder[self.category].max = max(rating[self.category].max, self.limit)
        remainder[self.category].min = max(rating[self.category].min, self.limit)
        return remainder

    def apply_to_rating_range(self, rating: dict):
        rating[self.category].max = min(rating[self.category].max, self.limit)
        rating[self.category].min = min(rating[self.category].min, self.limit)

    def __str__(self):
        return f"{self.category} < {self.limit} -> {self.workflow}"


class Workflow:
    def __init__(self, name, rules: list):
        self.name = name
        self.rules = rules

    def process(self, rating):
        for step in self.rules[:-1]:
            workflow = step.check_rating(rating)
            if workflow:
                WORKFLOW_DICT[workflow].process(rating)
                return
        WORKFLOW_DICT[self.rules[-1]].process(rating)

    def possible_combinations(self, rating):
        rating = copy.deepcopy(rating)
        combinations = 0
        for step in self.rules[:-1]:
            remainder = step.calculate_remainder(rating)
            step.apply_to_rating_range(rating)
            combinations += WORKFLOW_DICT[step.workflow].possible_combinations(rating)
            rating = remainder
        combinations += WORKFLOW_DICT[self.rules[-1]].possible_combinations(rating)

        return combinations


class AcceptWorkflow(Workflow):
    def __init__(self, name, rules: list):
        super().__init__(name, rules)

    def process(self, rating):
        ACCEPTED.append(rating)

    def possible_combinations(self, rating):
        combinations = rating['x'].max - rating['x'].min
        combinations *= rating['m'].max - rating['m'].min
        combinations *= rating['a'].max - rating['a'].min
        combinations *= rating['s'].max - rating['s'].min
        return max(0, combinations)


class RejectWorkflow(Workflow):
    def __init__(self, name, rules: list):
        super().__init__(name, rules)

    def process(self, rating):
        REJECTED.append(rating)

    def possible_combinations(self, rating):
        return 0


def parse_rules(rules):
    for name, rule_str in re.findall(r"(\w+)\{([a-zA-Z0-9<>:,]+)\}", rules):
        rules = []
        for rule in rule_str.split(',')[:-1]:
            rules.append(Rule.fromString(rule))
        rules.append(rule_str.split(',')[-1].strip())

        WORKFLOW_DICT[name] = Workflow(name, rules)
    WORKFLOW_DICT['R'] = RejectWorkflow('R', [])
    WORKFLOW_DICT['A'] = AcceptWorkflow('A', [])


def parse_ratings(ratings):
    rating_list = []
    for result in re.findall(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", ratings):
        rating_list.append({
            "x": int(result[0]),
            "m": int(result[1]),
            "a": int(result[2]),
            "s": int(result[3])
        })

    return rating_list


with open('input/day_19.txt') as file:
    file_content = file.read()

rules, ratings = file_content.split('\n\n')
parse_rules(rules)
ratings = parse_ratings(ratings)

for rating in ratings:
    WORKFLOW_DICT['in'].process(rating)

result = 0
for rating in ACCEPTED:
    result += rating['x']
    result += rating['m']
    result += rating['a']
    result += rating['s']

print(result)

rating = {
    'x': Range(1, 4001),
    'm': Range(1, 4001),
    'a': Range(1, 4001),
    's': Range(1, 4001)
}

print(WORKFLOW_DICT['in'].possible_combinations(rating))
