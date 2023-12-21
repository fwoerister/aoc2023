import re
from collections import deque

MODULES = {}


class Signal:
    HIGH_SIGNALS = 0
    LOW_SIGNALS = 0

    def __init__(self, source, target, value):
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return f"{self.source} - {self.target} - {self.value}"

    def apply(self, verbose=False):
        if self.value:
            Signal.HIGH_SIGNALS += 1
        else:
            Signal.LOW_SIGNALS += 1

        if self.target not in MODULES:
            return []

        MODULES[self.target].apply_signal(self.source, self.value)

        if verbose:
            print(f'{self.source} -{self.value}-> {self.target}')

        return MODULES[self.target].emit_signals()

    @staticmethod
    def reset_counter():
        Signal.LOW_SIGNALS = 0
        Signal.HIGH_SIGNALS = 0


class Module:
    descriptor = "?"

    def __init__(self, name, output_modules):
        self.name = name
        self.output = output_modules
        self.state = False
        self.input = False

    def to_state(self):
        return self.input, self.state

    def __str__(self):
        return f"{self.descriptor}{self.name} -> {self.output}"

    def apply_signal(self, source, value):
        self.input = value

    def emit_signals(self):
        self.state = self.input
        return [Signal(self.name, m, self.state) for m in self.output]


class FlipFlopModule(Module):
    descriptor = "%"

    def __init__(self, name, output_modules):
        super().__init__(name, output_modules)

    def emit_signals(self):
        if not self.input:
            self.state = not self.state
            return [Signal(self.name, m, self.state) for m in self.output]
        return []


class ConjunctionModule(Module):
    descriptor = "&"

    def __init__(self, name, output_modules):
        super().__init__(name, output_modules)
        self.input = {}

    def init_inputs(self, input_modules):
        for sender in input_modules:
            self.input[sender] = False

    def to_state(self):
        return tuple(self.input.values()), self.state

    def apply_signal(self, source, value):
        self.input[source] = value

    def emit_signals(self):
        self.state = False if all(self.input.values()) else True
        return [Signal(self.name, m, self.state) for m in self.output]


class BroadcastModule(Module):
    descriptor = "broadcaster"

    def __init__(self, name, output_modules):
        super().__init__('broadcaster', output_modules)
        self.input = False


class ButtonModule(Module):
    descriptor = "button"

    def __init__(self, name, output_modules):
        super().__init__('button', output_modules)
        self.input = False


MODULE_TYPES = [
    FlipFlopModule,
    ConjunctionModule,
    BroadcastModule,
]


def create_module(name, output_modules):
    for module_type in MODULE_TYPES:
        if name.startswith(module_type.descriptor):
            return module_type(name[len(module_type.descriptor):], output_modules)


def parse_modules(module_lines):
    all_output_modules = []
    for line in module_lines:
        name, output_modules = line.split(' -> ')
        parsed_output_modules = [receiver.strip() for receiver in output_modules.split(',')]
        all_output_modules += parsed_output_modules
        new_module = create_module(name, parsed_output_modules)
        MODULES[new_module.name] = new_module

    MODULES['button'] = ButtonModule('button', [MODULES['broadcaster'].name])

    for name, module in MODULES.items():
        for output in module.output:
            if output in MODULES and isinstance(MODULES[output], ConjunctionModule):
                MODULES[output].input[name] = False


with open('input/day_20.txt') as file:
    lines = file.readlines()

parse_modules(lines)

q = deque([])

module_names = MODULES.keys()

states = set()
signal_history = []
count = 0

while True:
    count += 1

    if count % 1000 == 0:
        print(count)

    for signal in MODULES['button'].emit_signals():
        q.append(signal)

    while q:
        signal = q.popleft()

        for new_signal in signal.apply():

            if new_signal.target == 'rx' and not new_signal.value:
                print('hi')
                break
            q.append(new_signal)

print(Signal.LOW_SIGNALS * Signal.HIGH_SIGNALS)
