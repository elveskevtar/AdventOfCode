#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
enhance = lambda x: 0 if enhancement[x] == "." else 1
enhancement = file_input[0]

default = 0
pixel_map = {}
for y, line in enumerate(file_input[2:]):
    if line == "":
        continue
    for x, char in enumerate(line):
        result = 0 if char == "." else 1
        pixel_map[x,y] = result
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0 or (x+dx,y+dy) in pixel_map:
                    continue
                pixel_map[x+dx,y+dy] = default

for i in range(50):
    new_default = enhance(int(str(default) * 9, 2))
    pixel_map_old = dict(pixel_map)
    for pos, val in pixel_map_old.items():
        x, y = pos
        result = ""
        for dy in range(-1,2):
            for dx in range(-1,2):
                if (x+dx,y+dy) not in pixel_map_old:
                    pixel_map[x+dx,y+dy] = new_default
                    result += str(default)
                    continue
                result += str(pixel_map_old[x+dx,y+dy])
        result = int(result, 2)
        pixel_map[x,y] = enhance(result)
    default = new_default

num_pixels = len(list(filter(lambda x: x == 1, pixel_map.values())))
print("Number Pixel Lit: {}".format(num_pixels))

