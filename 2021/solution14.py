#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

insertion_map = {}
for line in file_input[2:]:
    if line == "":
        continue
    template, insertion = line.split()[0], line.split()[-1]
    insertion_map[template] = insertion

start = file_input[0]
templates = {}
for j in range(len(start)-1):
    template = start[j:j+2]
    templates[template] = templates.get(template, 0) + 1

freq_count = {char:start.count(char) for char in set(start)}
for i in range(40):
    for template, freq in dict(templates).items():
        templates[template] -= freq
        insertion = insertion_map[template]
        first, second = template[0] + insertion, insertion + template[1]
        templates[first] = templates.get(first, 0) + freq
        templates[second] = templates.get(second, 0) + freq
        freq_count[insertion] = freq_count.get(insertion, 0) + freq

least = min(freq_count.values())
most = max(freq_count.values())
print("Most - Least common = {}".format(most - least))

