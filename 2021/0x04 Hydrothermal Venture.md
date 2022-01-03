## --- Day 5: Hydrothermal Venture ---

You come across a field of [hydrothermal vents](https://en.wikipedia.org/wiki/Hydrothermal_vent) on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in _lines_; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

```
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
```

Each line of vents is given as a line segment in the format `x1,y1 -> x2,y2` where `x1`,`y1` are the coordinates of one end the line segment and `x2`,`y2` are the coordinates of the other end. These line segments include the points at both ends. In other words:

-   An entry like `1,1 -> 1,3` covers points `1,1`, `1,2`, and `1,3`.
-   An entry like `9,7 -> 7,7` covers points `9,7`, `8,7`, and `7,7`.

For now, _only consider horizontal and vertical lines_: lines where either `x1 = x2` or `y1 = y2`.

So, the horizontal and vertical lines from the above list would produce the following diagram:

```
.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
```

In this diagram, the top left corner is `0,0` and the bottom right corner is `9,9`. Each position is shown as _the number of lines which cover that point_ or `.` if no line covers that point. The top-left pair of `1`s, for example, comes from `2,2 -> 2,1`; the very bottom row is formed by the overlapping lines `0,9 -> 5,9` and `0,9 -> 2,9`.

To avoid the most dangerous areas, you need to determine _the number of points where at least two lines overlap_. In the above example, this is anywhere in the diagram with a `2` or larger - a total of `_5_` points.

Consider only horizontal and vertical lines. _At how many points do at least two lines overlap?_

##### Solution
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

field = {}
file_input = open(sys.argv[1], "r").read().strip().split("\n")

def delta(p1, p2):
    if p1 > p2:
        return -1
    return int(p1 != p2)

for line in file_input:
    start, end = line.split(" -> ")
    x1, y1 = list(map(lambda x: int(x), start.split(",")))
    x2, y2 = list(map(lambda x: int(x), end.split(",")))
    delta_x, delta_y = delta(x1, x2), delta(y1, y2)
    x, y = x1, y1
    if delta_y == 0 and delta_x != 0:
        while x != x2:
            field[x,y] = field.get((x,y),0) + 1
            x += delta_x
        field[x,y] = field.get((x,y),0) + 1
    if delta_x == 0 and delta_y != 0:
        while y != y2:
            field[x,y] = field.get((x,y),0) + 1
            y += delta_y
        field[x,y] = field.get((x,y),0) + 1

num_points = sum(list(map(lambda x: x >= 2, field.values())))
print("Dangerous Points: " + str(num_points))
```

```bash
❯ python3 solution5.py input5
Dangerous Points: 6666
```

## --- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider _diagonal lines_.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

-   An entry like `1,1 -> 3,3` covers points `1,1`, `2,2`, and `3,3`.
-   An entry like `9,7 -> 7,9` covers points `9,7`, `8,8`, and `7,9`.

Considering all lines from the above example would now produce the following diagram:

```
1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
```

You still need to determine _the number of points where at least two lines overlap_. In the above example, this is still anywhere in the diagram with a `2` or larger - now a total of `_12_` points.

Consider all of the lines. _At how many points do at least two lines overlap?_

Part 2 was really easy if we just generalized our main loop:
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

field = {}
file_input = open(sys.argv[1], "r").read().strip().split("\n")

def delta(p1, p2):
    if p1 > p2:
        return -1
    return int(p1 != p2)

for line in file_input:
    start, end = line.split(" -> ")
    x1, y1 = list(map(lambda x: int(x), start.split(",")))
    x2, y2 = list(map(lambda x: int(x), end.split(",")))
    delta_x, delta_y = delta(x1, x2), delta(y1, y2)
    x, y = x1, y1
    while x != x2 or y != y2:
        field[x,y] = field.get((x,y),0) + 1
        x += delta_x
        y += delta_y
    field[x,y] = field.get((x,y),0) + 1

num_points = sum(list(map(lambda x: x >= 2, field.values())))
print("Dangerous Points: " + str(num_points))
```

```bash
❯ python3 solution5.py input5
Dangerous Points: 19081
```