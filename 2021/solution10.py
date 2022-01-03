#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

file_input = open(sys.argv[1], "r").read().strip().split("\n")

syntax_total, autocomplete_list = 0, []
for line in file_input:
    stack = deque()
    corrupted = False
    for i, char in enumerate(line):
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
            continue
        if len(stack) == 0 or stack[-1] != pairs[char]:
            syntax_total += points[char]
            corrupted = True
            break
        stack.pop()
    if len(stack) == 0 or corrupted:
        continue
    autocomplete_total = 0
    for x in list(reversed(stack)):
        autocomplete_total *= 5
        autocomplete_total += points[x]
    autocomplete_list.append(autocomplete_total)
autocomplete_list.sort()

print("Syntax Error Score: " + str(syntax_total))
print("Autocomplete Score: " + str(autocomplete_list[len(autocomplete_list)//2]))

