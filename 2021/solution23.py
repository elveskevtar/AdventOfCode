#!/usr/bin/env python3
from copy import copy, deepcopy
from heapq import heappush, heappop
from math import copysign
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
amphipod_dst = {"A": 2, "B": 4, "C": 6, "D": 8}

class Amphipod:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.moved = False

    def move(self, new_pos, field):
        self.moved = True
        moves = abs(self.pos[0] - new_pos[0]) + abs(self.pos[1] - new_pos[1])
        field.field[new_pos] = self
        field.field[self.pos] = None
        self.pos = new_pos
        field.points += moves * multiplier[self.label]

    def __repr__(self):
        return "Amphipod({})".format(self.label)

    def __eq__(self, other):
        return other and self.label == other.label \
                and self.pos == other.pos and self.moved == other.moved

    def __hash__(self):
        return hash((self.label, self.pos, self.moved))

class Field:
    def __init__(self, field, points):
        self.field = field
        self.points = points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.field == other.field and self.points == other.points

    def __hash__(self):
        states = []
        for pod in self.field.values():
            if pod:
                states.append(hash(pod))
        states.sort()
        return hash(tuple(states))

    def custom_copy(self, pos):
        # shallow copy field dict and points
        field = copy(self.field)
        points = copy(self.points)
        obj = Field(field, points)
        # deepcopy single amphipod object at position
        obj.field[pos] = deepcopy(obj.field[pos])
        return obj

    def solved(self):
        field = self.field
        for y in range(1,5):
            for x in range(4):
                x = x*2 + 2
                if not field[x,y]: return False
                if amphipod_dst[field[x,y].label] != x: return False
        return True

def print_field(field):
    for y in range(5):
        result = ""
        for x in range(11):
            if (x,y) not in field:
                result += "#"
            elif field[x,y] is None:
                result += "."
            else:
                result += field[x,y].label
        print(result)
    print("")

field = {(x,0):None for x in range(11)}
field[2,2] = Amphipod("D", (2,2))
field[2,3] = Amphipod("D", (2,3))
field[4,2] = Amphipod("C", (4,2))
field[4,3] = Amphipod("B", (4,3))
field[6,2] = Amphipod("B", (6,2))
field[6,3] = Amphipod("A", (6,3))
field[8,2] = Amphipod("A", (8,2))
field[8,3] = Amphipod("C", (8,3))
for x in range(4):
    x = x*2 + 3
    field[x-1,1] = Amphipod(file_input[2][x], (x-1,1))
    field[x-1,4] = Amphipod(file_input[3][x], (x-1,4))
field = Field(field, 0)

print_field(field.field)

queue = []
heappush(queue, field)
visited_states = set()
room_rows = [2,4,6,8]
min_energy_cost = sys.maxsize
while len(queue) != 0:
    field_obj = heappop(queue)
    field_hash, field, score = hash(field_obj), field_obj.field, field_obj.points
    if field_hash in visited_states or score > min_energy_cost:
        continue
    visited_states.add(field_hash)
    if field_obj.solved():
        min_energy_cost = min(min_energy_cost, score)
        continue
    for y in range(1,5):
        for x in range(4):
            x = x*2 + 2
            if field[x,y] and not field[x,y].moved:
                blocked = False
                for y2 in range(y-1, 0, -1):
                    if field[x,y2]:
                        blocked = True
                        break
                if blocked: continue
                for x2 in range(x-1, -1, -1):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
                for x2 in range(x+1, 11):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
    for x in range(11):
        if not field[x,0]: continue
        dest = amphipod_dst[field[x,0].label]
        if field[dest,1]: continue
        room_available = True
        for y in range(4, 1, -1):
            if field[dest,y] and field[dest,y].label != field[x,0].label:
                room_available = False
        if not room_available: continue
        direction = int(copysign(1, dest-x))
        for x2 in range(x+direction, dest+direction, direction):
            if field[x2,0]: break
            if x2 != dest: continue
            for y in range(4, 0, -1):
                if not field[x2,y]:
                    new_field = field_obj.custom_copy((x,0))
                    new_field.field[x,0].move((x2,y), new_field)
                    heappush(queue, new_field)
                    break

print("Minimum energy cost: {}".format(min_energy_cost))
