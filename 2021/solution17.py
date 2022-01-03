#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
temp = file_input[0].split("target area: ")[1].split(", ")
min_x, max_x = list(map(lambda x: int(x), temp[0].split("=")[1].split("..")))
min_y, max_y = list(map(lambda x: int(x), temp[1].split("=")[1].split("..")))

range_x = max_x - min_x
range_y = max_y - min_y

result = 0
uniq_velocities = set()
for dx_init in range(1, max_x+1):
    for dy_init in range(min_y, range_y*10):
        dx, x = dx_init, 0
        dy, y, ymax = dy_init, 0, 0
        while x <= max_x and y >= min_y:
            if x >= min_x and y <= max_y:
                uniq_velocities.add((dx_init, dy_init))
                result = max(result, ymax)
                break
            y += dy
            dy -= 1
            ymax = max(ymax, y)
            x += dx
            dx = max(0, dx - 1)

print("Max y: {}".format(result))
print("Unique velocities: {}".format(len(uniq_velocities)))

