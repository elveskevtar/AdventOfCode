## --- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads _behind_ the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your [familiarity](https://adventofcode.com/2018/day/17) with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly _air_ with structures made of _rock_.

Your scan traces the path of each solid rock structure and reports the `x,y` coordinates that form the shape of the path, where `x` represents distance to the right and `y` represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

```
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
```

This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from `498,4` through `498,6` and another line of rock from `498,6` through `496,6`.)

The sand is pouring into the cave from point `500,0`.

Drawing rock as `#`, air as `.`, and the source of the sand as `+`, this becomes:

```

  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
```

Sand is produced _one unit at a time_, and the next unit of sand is not produced until the previous unit of sand _comes to rest_. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls _down one step_ if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally _one step down and to the left_. If that tile is blocked, the unit of sand attempts to instead move diagonally _one step down and to the right_. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand _comes to rest_ and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as `o`, the first unit of sand simply falls straight down and then stops:

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
```

The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
```

After a total of five units of sand have come to rest, they form this pattern:

```
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
```

After a total of 22 units of sand:

```
......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
```

Finally, only two more units of sand can possibly come to rest:

```
......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
```

Once all `_24_` units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with `~`:

```
.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
```

Using your scan, simulate the falling sand. _How many units of sand come to rest before sand starts flowing into the abyss below?_

```python
#!/usr/bin/env python3
import os
import sys
import time

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def add_coords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def print_map(rock_map, xmin, xmax, ymin, ymax):
    print("\033c")
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) not in rock_map:
                print(" ", end="")
            else:
                print(rock_map[x, y], end="")
        print("")

def create_map(data):
    rock_map, ymax = {(500, 0): "+"}, 0
    for structure in data:
        points = structure.split(" -> ")
        for i in range(len(points) - 1):
            x1, y1 = [int(i) for i in points[i].split(",")]
            x2, y2 = [int(i) for i in points[i+1].split(",")]
            if x1 - x2 != 0:
                y = y1
                ymax = max(y, ymax)
                xdiff = (x2 - x1) // abs(x2 - x1)
                for x in range(x1, x2 + xdiff, xdiff):
                    rock_map[x, y] = "#"
            elif y1 - y2 != 0:
                x = x1
                ydiff = (y2 - y1) // abs(y2 - y1)
                for y in range(y1, y2 + ydiff, ydiff):
                    ymax = max(y, ymax)
                    rock_map[x, y] = "#"
    return rock_map, ymax

def simulate_sand(rock_map: dict, ymax):
    terminal_size = os.get_terminal_size()
    rows = terminal_size.lines - 1
    cols = terminal_size.columns
    sand_units, next_sand = 1, (500, 1)
    while next_sand[1] < ymax:
        rock_map[next_sand] = "o"
        # time.sleep(0.05)
        # print_map(
        #     rock_map, next_sand[0] - (cols // 2), next_sand[0] + (cols // 2),
        #     next_sand[1] - (rows // 2), next_sand[1] + (rows // 2) + 1
        # )
        if add_coords(next_sand, (0, 1)) not in rock_map:
            rock_map.pop(next_sand)
            next_sand = add_coords(next_sand, (0, 1))
        elif add_coords(next_sand, (-1, 1)) not in rock_map:
            rock_map.pop(next_sand)
            next_sand = add_coords(next_sand, (-1, 1))
        elif add_coords(next_sand, (1, 1)) not in rock_map:
            rock_map.pop(next_sand)
            next_sand = add_coords(next_sand, (1, 1))
        else:
            sand_units += 1
            next_sand = (500, 1)
    return sand_units - 1

data = open(sys.argv[1], "r").read().strip().split("\n")
rock_map, ymax = create_map(data)
print(f"Sand units: {simulate_sand(rock_map, ymax)}")
```

```bash
❯ python3 solution14.py input14
Sand units: 1298
```

## --- Part Two ---

You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a `y` coordinate equal to _two plus the highest `y` coordinate_ of any point in your scan.

In the example above, the highest `y` coordinate of any point is `9`, and so the floor is at `y=11`. (This is as if your scan contained one extra rock path like `-infinity,11 -> infinity,11`.) With the added floor, the example above now looks like this:

```
        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
```

To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at `500,0`, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after `_93_` units of sand come to rest:

```
............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
```

Using your scan, simulate the falling sand until the source of the sand becomes blocked. _How many units of sand come to rest?_

```python
def simulate_sand(rock_map: dict, ymax):
    terminal_size = os.get_terminal_size()
    rows = terminal_size.lines - 1
    cols = terminal_size.columns
    sand_units, next_sand = 1, (500, 0)
    while True:
        rock_map[next_sand] = "o"
        # time.sleep(0.05)
        # print_map(
        #     rock_map, next_sand[0] - (cols // 2), next_sand[0] + (cols // 2),
        #     next_sand[1] - (rows // 2), next_sand[1] + (rows // 2) + 1
        # )
        if next_sand[1] < ymax + 1:
            if add_coords(next_sand, (0, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (0, 1))
            elif add_coords(next_sand, (-1, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (-1, 1))
            elif add_coords(next_sand, (1, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (1, 1))
            elif next_sand == (500, 0):
                break
            else:
                sand_units += 1
                next_sand = (500, 0)
        else:
            sand_units += 1
            next_sand = (500, 0)
    return sand_units
```

```bash
❯ python3 solution14.py input14
Sand units: 25585
```