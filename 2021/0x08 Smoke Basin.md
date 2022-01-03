## --- Day 9: Smoke Basin ---

These caves seem to be [lava tubes](https://en.wikipedia.org/wiki/Lava_tube). Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

Each number corresponds to the height of a particular location, where `9` is the highest and `0` is the lowest a location can be.

Your first goal is to find the _low points_ - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are _four_ low points, all highlighted: two are in the first row (a `1` and a `0`), one is in the third row (a `5`), and one is in the bottom row (also a `5`). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The _risk level_ of a low point is _1 plus its height_. In the above example, the risk levels of the low points are `2`, `1`, `6`, and `6`. The sum of the risk levels of all low points in the heightmap is therefore `_15_`.

Find all of the low points on your heightmap. _What is the sum of the risk levels of all low points on your heightmap?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

heightmap = {}
for y, line in enumerate(file_input):
    for x, val in enumerate(line):
        heightmap[x,y] = int(val)

total = 0
for (x, y), val in heightmap.items():
    low = True
    for dx in [-1,1]:
        if (x + dx, y) in heightmap and heightmap[x+dx,y] <= val:
            low = False
    for dy in [-1,1]:
        if (x, y + dy) in heightmap and heightmap[x,y+dy] <= val:
            low = False
    if low:
        total += 1 + val

print("Risk Level: " + str(total))
```

```bash
❯ python3 solution9.py input9
Risk Level: 560
```

## --- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A _basin_ is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height `9` do not count as being in any basin, and all other locations will always be part of exactly one basin.

The _size_ of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size `3`:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The top-right basin, size `9`:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The middle basin, size `14`:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The bottom-right basin, size `9`:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

Find the three largest basins and multiply their sizes together. In the above example, this is `9 * 14 * 9 = _1134_`.

_What do you get if you multiply together the sizes of the three largest basins?_

```python
#!/usr/bin/env python3
from collections import deque
from functools import reduce
import heapq
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

heightmap = {}
for y, line in enumerate(file_input):
    for x, val in enumerate(line):
        heightmap[x,y] = int(val)

total = 0
for (x, y), val in heightmap.items():
    low = True
    for dx in [-1,1]:
        if (x + dx, y) in heightmap and heightmap[x+dx,y] <= val:
            low = False
    for dy in [-1,1]:
        if (x, y + dy) in heightmap and heightmap[x,y+dy] <= val:
            low = False
    if low:
        total += 1 + val

basin_queue = deque()
visited = set()
largest_basins = []
for (x, y), val in heightmap.items():
    if val == 9 or (x, y) in visited:
        continue
    basin_queue.clear()
    basin_queue.append((x,y))
    basin_length = 0
    while len(basin_queue) != 0:
        x1, y1 = basin_queue.pop()
        if (x1, y1) in visited:
            continue
        basin_length += 1
        visited.add((x1,y1))
        for dx in [-1,1]:
            check = (x1 + dx, y1)
            if check in heightmap and heightmap[check] != 9:
                basin_queue.append(check)
        for dy in [-1,1]:
            check = (x1, y1 + dy)
            if check in heightmap and heightmap[check] != 9:
                basin_queue.append(check)
    heapq.heappush(largest_basins, basin_length)

largest = reduce(lambda x, y: x * y, heapq.nlargest(3, largest_basins))
print("Risk Level: " + str(total))
print("Largest Basins: " + str(largest))
```

```bash
❯ python3 solution9.py input9
Risk Level: 560
Largest Basins: 959136
```