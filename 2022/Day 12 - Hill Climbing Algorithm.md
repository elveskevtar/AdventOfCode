## --- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where `a` is the lowest elevation, `b` is the next-lowest, and so on up to the highest elevation, `z`.

Also included on the heightmap are marks for your current position (`S`) and the location that should get the best signal (`E`). Your current position (`S`) has elevation `a`, and the location that should get the best signal (`E`) has elevation `z`.

You'd like to reach `E`, but to save energy, you should do it in _as few steps as possible_. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be _at most one higher_ than the elevation of your current square; that is, if your current elevation is `m`, you could step to elevation `n`, but not to elevation `o`. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

```
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
```

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the `e` at the bottom. From there, you can spiral around to the goal:

```
v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
```

In the above diagram, the symbols indicate whether the path exits each square moving up (`^`), down (`v`), left (`<`), or right (`>`). The location that should get the best signal is still `E`, and `.` marks unvisited squares.

This path reaches the goal in `_31_` steps, the fewest possible.

_What is the fewest steps required to move from your current position to the location that should get the best signal?_

```python
#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def add_coords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def create_map(input):
    height_map = {}
    start_point = end_point = None
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            height = char
            if height == "S":
                height = "a"
                start_point = (x, y)
            elif height == "E":
                height = "z"
                end_point = (x, y)
            height_map[x, y] = ord(height)
    return height_map, start_point, end_point

def shortest_path(height_map, start_point, end_point):
    steps = 0
    visited_points = {}
    next_moves = deque([(start_point, steps)])
    while len(next_moves) > 0:
        next_point, steps = next_moves.pop()
        if next_point == end_point:
            visited_points[end_point] = min(visited_points.get(next_point, steps), steps)
            continue
        if next_point in visited_points and steps >= visited_points[next_point]:
            continue
        visited_points[next_point] = min(visited_points.get(next_point, steps), steps)
        delta_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        delta_moves = [add_coords(next_point, delta) for delta in delta_moves]
        for delta_move in delta_moves:
            if delta_move not in height_map:
                continue
            if height_map[delta_move] - height_map[next_point] <= 1:
                next_moves.append((delta_move, steps + 1))
    return visited_points[end_point]

data = open(sys.argv[1], "r").read().strip().split("\n")
height_map, start_point, end_point = create_map(data)
min_steps = shortest_path(height_map, start_point, end_point)
print(f"Minimum steps to good signal: {min_steps}")
```

```bash
❯ time python3 solution12.py input12
Minimum steps to good signal: 420
python3 solution12.py input12  3.18s user 0.01s system 99% cpu 3.185 total
```

## --- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation `a`. The goal is still the square marked `E`. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from _any square at elevation `a`_ to the square marked `E`.

Again consider the example from above:

```
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
```

Now, there are six choices for starting position (five marked `a`, plus the square marked `S` that counts as being at elevation `a`). If you start at the bottom-left square, you can reach the goal most quickly:

```
...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
```

This path reaches the goal in only `_29_` steps, the fewest possible.

_What is the fewest steps required to move starting from any square with elevation `a` to the location that should get the best signal?_

```python
def shortest_path(height_map, start_point, end_point):
    steps = 0
    visited_points = {}
    next_moves = deque([(start_point, steps)])
    while len(next_moves) > 0:
        next_point, steps = next_moves.pop()
        if next_point == end_point:
            visited_points[end_point] = min(visited_points.get(next_point, steps), steps)
            continue
        if next_point in visited_points and steps >= visited_points[next_point]:
            continue
        visited_points[next_point] = min(visited_points.get(next_point, steps), steps)
        delta_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        delta_moves = [add_coords(next_point, delta) for delta in delta_moves]
        for delta_move in delta_moves:
            if delta_move not in height_map:
                continue
            if height_map[delta_move] - height_map[next_point] <= 1:
                next_steps = steps + 1
                if height_map[delta_move] == ord("a"):
                    next_steps = 0
                next_moves.append((delta_move, next_steps))
    return visited_points[end_point]
```

```bash
❯ time python3 solution12.py input12
Minimum steps to good signal: 414
python3 solution12.py input12  0.78s user 0.01s system 99% cpu 0.787 total
```