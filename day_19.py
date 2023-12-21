import re
import json

WORKFLOW_DICT = dict()
WORKFLOW_LIST = list()

ACCEPTED = []
REJECTED = []


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


class LessThanRule(Rule):
    def __init__(self, category, limit, workflow):
        self.category = category
        self.limit = limit
        self.workflow = workflow

    def check_rating(self, rating):
        return self.workflow if rating[self.category] < self.limit else None


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


class AcceptWorkflow(Workflow):
    def __init__(self, name, rules: list):
        super().__init__(name, rules)

    def process(self, rating):
        ACCEPTED.append(rating)


class RejectWorkflow(Workflow):
    def __init__(self, name, rules: list):
        super().__init__(name, rules)

    def process(self, rating):
        REJECTED.append(rating)


def get_combinations(wf: Workflow, rating):
    combinations = 1

    for rule in wf.rules[:-1]:
        if isinstance(rule, GreaterThanRule):
            new_rating = dict(rating)
            new_rating[rule.category] = (max(rating[rule.category][0], rule.limit), rating[rule.category][1])
            combinations *= get_combinations(rule.workflow, new_rating)
            rating[rule.category] = (
            rating[rule.category][0], min(rating[rule.category][0], new_rating[rule.category][1]))
        elif isinstance(rule, LessThanRule):
            new_rating = ((0, 0), (0, 0), (0, 0), (0, 0))
            combinations *= get_combinations(rule.workflow, new_rating)
    combinations *= get_combinations(WORKFLOW_DICT[wf.rules[-1]])


def parse_rules(rules):
    for name, rule_str in re.findall(r"(\w+)\{([a-zA-Z0-9<>:,]+)\}", rules):
        rules = []
        for rule in rule_str.split(',')[:-1]:
            rules.append(Rule.fromString(rule))
        rules.append(rule_str.split(',')[-1].strip())

        WORKFLOW_DICT[name] = Workflow(name, rules)
        WORKFLOW_LIST.append(WORKFLOW_DICT[name])
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
