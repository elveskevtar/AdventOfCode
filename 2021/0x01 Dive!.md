## --- Day 2: Dive! ---

Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like `forward 1`, `down 2`, or `up 3`:

-   `forward X` increases the horizontal position by `X` units.
-   `down X` _increases_ the depth by `X` units.
-   `up X` _decreases_ the depth by `X` units.

Note that since you're on a submarine, `down` and `up` affect your _depth_, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

```
forward 5
down 5
forward 8
up 3
down 8
forward 2
```

Your horizontal position and depth both start at `0`. The steps above would then modify them as follows:

-   `forward 5` adds `5` to your horizontal position, a total of `5`.
-   `down 5` adds `5` to your depth, resulting in a value of `5`.
-   `forward 8` adds `8` to your horizontal position, a total of `13`.
-   `up 3` decreases your depth by `3`, resulting in a value of `2`.
-   `down 8` adds `8` to your depth, resulting in a value of `10`.
-   `forward 2` adds `2` to your horizontal position, a total of `15`.

After following these instructions, you would have a horizontal position of `15` and a depth of `10`. (Multiplying these together produces `_150_`.)

Calculate the horizontal position and depth you would have after following the planned course. _What do you get if you multiply your final horizontal position by your final depth?_

To begin, [get your puzzle input](https://adventofcode.com/2021/day/2/input).

Saved puzzle as `input2`

`solution2.py`
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

position, depth = 0, 0
for instruction in file_input:
    instruction_type, instruction_val = instruction.split()
    instruction_val = int(instruction_val)
    if instruction_type == "forward":
        position += instruction_val
    elif instruction_type == "up":
        depth -= instruction_val
    elif instruction_type == "down":
        depth += instruction_val

print("Final position * depth = " + str(position * depth))
```

```bash
❯ python3 solution2.py input2
Final position * depth = 2120749
```

## --- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, _aim_, which also starts at `0`. The commands also mean something entirely different than you first thought:

-   `down X` _increases_ your aim by `X` units.
-   `up X` _decreases_ your aim by `X` units.
-   `forward X` does two things:
    -   It increases your horizontal position by `X` units.
    -   It increases your depth by your aim _multiplied by_ `X`.

Again note that since you're on a submarine, `down` and `up` do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

-   `forward 5` adds `5` to your horizontal position, a total of `5`. Because your aim is `0`, your depth does not change.
-   `down 5` adds `5` to your aim, resulting in a value of `5`.
-   `forward 8` adds `8` to your horizontal position, a total of `13`. Because your aim is `5`, your depth increases by `8*5=40`.
-   `up 3` decreases your aim by `3`, resulting in a value of `2`.
-   `down 8` adds `8` to your aim, resulting in a value of `10`.
-   `forward 2` adds `2` to your horizontal position, a total of `15`. Because your aim is `10`, your depth increases by `2*10=20` to a total of `60`.

After following these new instructions, you would have a horizontal position of `15` and a depth of `60`. (Multiplying these produces `_900_`.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. _What do you get if you multiply your final horizontal position by your final depth?_

Updated `solution2.py`
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
data = list(map(lambda x: x.split(" "), file_input))

position, aim, depth = 0, 0, 0
for instruction in data:
    instruction_type = instruction[0]
    instruction_val = int(instruction[1])
    if instruction_type == "forward":
        position += instruction_val
        depth += instruction_val * aim
    elif instruction_type == "up":
        aim -= instruction_val
    elif instruction_type == "down":
        aim += instruction_val

print("Final position * depth = " + str(position * depth))
```

```bash
❯ python3 solution2.py input2
Final position * depth = 2138382217
```