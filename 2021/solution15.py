#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

class Cell:
    def __init__(self, x, y, weight=None):
        self.x = x
        self.y = y
        self.weight = weight

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

graph = {}
x_length = len(file_input[0])
y_length = len(file_input)
for y, line in enumerate(file_input):
    for x, weight in enumerate(line):
        for ry in range(5):
            for rx in range(5):
                graph_x = rx * x_length + x
                graph_y = ry * y_length + y
                new_weight = ((int(weight) + (ry + rx) - 1) % 9) + 1
                graph[graph_x,graph_y] = Cell(graph_x, graph_y, new_weight)

dx = [-1,0,1,0]
dy = [0,1,0,-1]

x_length *= 5
y_length *= 5

st = set()
st.add(Cell(0, 0, 0))
dist = {(0,0): 0}
while len(st) != 0:
    cell = st.pop()
    for i in range(4):
        x = cell.x + dx[i]
        y = cell.y + dy[i]

        if x < 0 or y < 0 or y >= y_length or x >= x_length:
            continue

        if (x,y) not in dist or dist[x,y] > dist[cell.x,cell.y] + graph[x,y].weight:
            check = Cell(x,y)
            if check in st:
                st.remove(check)

            dist[x,y] = dist[cell.x,cell.y] + graph[x,y].weight
            st.add(Cell(x, y, dist[x,y]))

print("Shortest Path Length: {}".format(dist[x_length-1,y_length-1]))

