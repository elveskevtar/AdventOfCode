#!/usr/bin/env python3
from math import prod
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

class Cube:
    def __init__(self, dims):
        self.dims = dims

    def intersects(self, other):
        return not (other.dims[0] < self.dims[0] and other.dims[1] < self.dims[0]) \
            and not (other.dims[0] > self.dims[1] and other.dims[1] > self.dims[1]) \
            and not (other.dims[2] < self.dims[2] and other.dims[3] < self.dims[2]) \
            and not (other.dims[2] > self.dims[3] and other.dims[3] > self.dims[3]) \
            and not (other.dims[4] < self.dims[4] and other.dims[5] < self.dims[4]) \
            and not (other.dims[4] > self.dims[5] and other.dims[5] > self.dims[5])

    def volume(self):
        return prod([self.dims[i+1] - self.dims[i] + 1 for i in range(0, 6, 2)])

    def __str__(self):
        return str(self.dims)

def split(cubes, cube1, cube2):
    """
    If cube2 intersects cube1, this functions splits cube1 into new cubes
    and adds them to the cubes set.
    """
    x_start, y_start, z_start = cube1.dims[0], cube1.dims[2], cube1.dims[4]
    x_end, y_end, z_end = cube1.dims[1], cube1.dims[3], cube1.dims[5]
    if x_start < cube2.dims[0]:
        cubes.add(Cube((x_start, cube2.dims[0]-1, y_start, y_end, z_start, z_end)))
        x_start = cube2.dims[0]
    if y_start < cube2.dims[2]:
        cubes.add(Cube((x_start, x_end, y_start, cube2.dims[2]-1, z_start, z_end)))
        y_start = cube2.dims[2]
    if z_start < cube2.dims[4]:
        cubes.add(Cube((x_start, x_end, y_start, y_end, z_start, cube2.dims[4]-1)))
        z_start = cube2.dims[4]
    x_start2, y_start2, z_start2 = cube2.dims[1] + 1, cube2.dims[3] + 1, cube2.dims[5] + 1
    if x_start2 <= x_end:
        cubes.add(Cube((x_start2, x_end, y_start, y_end, z_start, z_end)))
        x_end = cube2.dims[1]
    if y_start2 <= y_end:
        cubes.add(Cube((x_start, x_end, y_start2, y_end, z_start, z_end)))
        y_end = cube2.dims[3]
    if z_start2 <= z_end:
        cubes.add(Cube((x_start, x_end, y_start, y_end, z_start2, z_end)))
        z_end = cube2.dims[5]

cubes = set()
for line in file_input:
    if line == "":
        continue
    instr, ranges = line.split()
    _x, _y, _z = ranges.split(",")
    x1, x2 = [int(x) for x in _x.split("=")[1].split("..")]
    y1, y2 = [int(y) for y in _y.split("=")[1].split("..")]
    z1, z2 = [int(z) for z in _z.split("=")[1].split("..")]
    new_cube = Cube((x1, x2, y1, y2, z1, z2))
    for cube in list(cubes):
        if cube.intersects(new_cube):
            cubes.remove(cube)
            split(cubes, cube, new_cube)
    if instr == "on":
        cubes.add(new_cube)

total = sum([cube.volume() for cube in cubes])
print("Number of cubes lit: {}".format(total))

