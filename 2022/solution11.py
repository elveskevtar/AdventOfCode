#!/usr/bin/env python3
from collections import deque
from math import prod
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

class Monkey:
    def __init__(
        self, monkeys,
        starting_items, operation, operand, divisor, if_true, if_false,
    ):
        self.monkeys = monkeys
        self.starting_items = deque(starting_items)
        self.operation = operation
        self.operand = operand
        self.divisor = divisor
        self.if_true = if_true
        self.if_false = if_false
        self.num_inspected = 0

    def inspect_and_throw(self, common_mod):
        while len(self.starting_items) > 0:
            item = self.starting_items.popleft()
            if self.operation == "*":
                operation = lambda old, x: (old * x) % common_mod
            elif self.operation == "+":
                operation = lambda old, x: (old + x) % common_mod
            if self.operand == "old":
                item = operation(item, item)
            else:
                item = operation(item, int(self.operand))
            self.num_inspected += 1
            # item //= 3

            send_to = self.if_true if (item % self.divisor) == 0 else self.if_false
            self.monkeys[send_to].starting_items.append(item)

def mitm(notes):
    monkeys = []
    for line in range(0, len(notes), 7):
        starting_items = notes[line + 1].split(": ")[1].split(", ")
        starting_items = [int(item) for item in starting_items]
        operation = notes[line + 2].split(" = ")[1].split()[1]
        operand = notes[line + 2].split(" = ")[1].split()[2]
        divisor = int(notes[line + 3].split(" by ")[1])
        if_true = int(notes[line + 4].split(" monkey ")[1])
        if_false = int(notes[line + 5].split(" monkey ")[1])
        monkey = Monkey(
            monkeys, starting_items, operation, operand,
            divisor, if_true, if_false,
        )
        monkeys.append(monkey)
    
    common_mod = prod([monkey.divisor for monkey in monkeys])
    print(f"Found common mod {common_mod}")

    # play 20 rounds
    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            monkey.inspect_and_throw(common_mod)
    monkey_inspections = [monkey.num_inspected for monkey in monkeys]
    monkey_business = prod(sorted(monkey_inspections)[-2:])
    print(f"Monkey business: {monkey_business}")

data = open(sys.argv[1], "r").read().strip().split("\n")
mitm(data)
