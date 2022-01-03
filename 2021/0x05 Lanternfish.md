## --- Day 6: Lanternfish ---

The sea floor is getting steeper. Maybe the sleigh keys got carried this way?

A massive school of glowing [lanternfish](https://en.wikipedia.org/wiki/Lanternfish) swims past. They must spawn quickly to reach such large numbers - maybe _exponentially_ quickly? You should model their growth rate to be sure.

Although you know nothing about this specific species of lanternfish, you make some guesses about their attributes. Surely, each lanternfish creates a new lanternfish once every _7_ days.

However, this process isn't necessarily synchronized between every lanternfish - one lanternfish might have 2 days left until it creates another lanternfish, while another might have 4. So, you can model each fish as a single number that represents _the number of days until it creates a new lanternfish_.

Furthermore, you reason, a _new_ lanternfish would surely need slightly longer before it's capable of producing more lanternfish: two more days for its first cycle.

So, suppose you have a lanternfish with an internal timer value of `3`:

-   After one day, its internal timer would become `2`.
-   After another day, its internal timer would become `1`.
-   After another day, its internal timer would become `0`.
-   After another day, its internal timer would reset to `6`, and it would create a _new_ lanternfish with an internal timer of `8`.
-   After another day, the first lanternfish would have an internal timer of `5`, and the second lanternfish would have an internal timer of `7`.

A lanternfish that creates a new fish resets its timer to `6`, _not `7`_ (because `0` is included as a valid timer value). The new lanternfish starts with an internal timer of `8` and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list of the ages of several hundred nearby lanternfish (your puzzle input). For example, suppose you were given the following list:

```
3,4,3,1,2
```

This list means that the first fish has an internal timer of `3`, the second fish has an internal timer of `4`, and so on until the fifth fish, which has an internal timer of `2`. Simulating these fish over several days would proceed as follows:

```
Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
```

Each day, a `0` becomes a `6` and adds a new `8` to the end of the list, while each other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of `26` fish. After 80 days, there would be a total of `_5934_`.

Find a way to simulate lanternfish. _How many lanternfish would there be after 80 days?_

I did this at first because it was quick:
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

class Lanternfish:
    def __init__(self, start: int):
        self.timer = start

    def tick(self) -> bool:
        reproduce = False
        if self.timer == 0:
            reproduce = True
        self.timer = (self.timer - 1) % max(7, self.timer)
        return reproduce

file_input = open(sys.argv[1], "r").read().strip().split("\n")
starts = file_input[0].split(",")

lanternfish = [Lanternfish(int(start)) for start in starts]
for x in range(80):
    for i in range(len(lanternfish)):
        if lanternfish[i].tick():
            lanternfish.append(Lanternfish(8))

print(len(lanternfish))
```

But it was slow and I knew there had to be better ways. This ends up being roughly `O(n * 2^(x/7))` where `n` is the length of the original list and the exponentially expression comes from the fish doubling roughly ever 7 days. This is not really precise, but I think the exact expression is something like a series formula.

```bash
❯ python3 solution6.py input6
380612
```

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

class Lanternfish:
    def __init__(self, start: int):
        self.timer = start

    def tick(self) -> bool:
        reproduce = False
        if self.timer == 0:
            reproduce = True
        self.timer = (self.timer - 1) % max(7, self.timer)
        return reproduce

file_input = open(sys.argv[1], "r").read().strip().split("\n")
starts = list(map(lambda x: int(x), file_input[0].split(",")))

freq_map = {}
for start in starts:
    if start not in freq_map:
        freq_map[start] = 1
    else:
        freq_map[start] += 1

total = 0
for start, frequency in freq_map.items():
    lanternfish = [Lanternfish(start)]
    for x in range(80):
        for i in range(len(lanternfish)):
            if lanternfish[i].tick():
                lanternfish.append(Lanternfish(8))
    total += len(lanternfish) * frequency

print("Total Lanternfish (80 days): " + str(total))
```

So now we're just counting the frequency with `O(n)` of the initial state list and only have to expand on the unique start times one each with `O(2^(x/7))` roughly, making it `O(n + 2^(x/7))` which is a significant upgrade from the former.

EDIT: actually better is to track the minimal states and their frequencies:
```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

freq_map = {}
for start in file_input[0].split(","):
    start = int(start)
    freq_map[start] = freq_map.get(start, 0) + 1

days = 80
for x in range(days):
    for start, frequency in dict(freq_map).items():
        freq_map[start] -= frequency
        if start == 0:
            freq_map[8] = freq_map.get(8, 0) + frequency
            freq_map[6] = freq_map.get(6, 0) + frequency
        else:
            freq_map[start-1] = freq_map.get(start-1, 0) + frequency

print("Total Lanternfish ({} days): {}".format(days, sum(freq_map.values())))
```

## --- Part Two ---

Suppose the lanternfish live forever and have unlimited food and space. Would they take over the entire ocean?

After 256 days in the example above, there would be a total of `_26984457539_` lanternfish!

_How many lanternfish would there be after 256 days?_

For part 2, the problem I initially ran into with my original solution was space. The space is also growing exponentially but I think the time would be an issue too even after space is addressed.

I was trying to avoid it, but we cannot store/calculate `2^256` on my machine in a reasonable amount of time. So we will have to figure out how to put this exponential growth into a formula.

Found a nice numpy package to do this for us:
```bash
❯ python3 solution6.py input6 256
Total Lanternfish (256 days): 1710166656900
```

```python
#!/usr/bin/env python3
import sys

import numpy as np

if len(sys.argv) != 3:
    print("Usage: {} <input file> <# days>".format(sys.argv[0]))
    sys.exit(1)

def calc_fish(data, days):
    uniq, cnts = np.unique(data, return_counts=True)
    fish = np.zeros(9, dtype=np.uint64)
    fish[uniq] = cnts
    for idx in range(days):
        num_zero = fish[0]
        fish[:-1] = fish[1:]
        fish[8] = num_zero
        fish[6] += num_zero
    return np.sum(fish)

days = int(sys.argv[2])
data = np.loadtxt(sys.argv[1], delimiter=",", dtype=int)
print("Total Lanternfish ({} days): {}".format(days, calc_fish(data, days)))
```