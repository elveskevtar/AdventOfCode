#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

i = 0
line = file_input[i]
dots = set()
while line != "":
    x, y = [int(x) for x in line.split(",")]
    dots.add((x,y))
    i += 1
    line = file_input[i]

for i in range(i+1, len(file_input)):
    if file_input[i] == "":
        continue
    plane, num = file_input[i].split()[-1].split("=")
    num = int(num)
    for x, y in set(dots):
        if plane == "y":
            if y > num:
                dots.add((x,2*num-y))
                dots.remove((x,y))
        else:
            if x > num:
                dots.add((2*num-x,y))
                dots.remove((x,y))

print("Number Dots: {}".format(len(dots)))

for y in range(10):
    result = ""
    for x in range(50):
        if (x, y) in dots:
            result += "#"
        else:
            result += "."
    print(result)

