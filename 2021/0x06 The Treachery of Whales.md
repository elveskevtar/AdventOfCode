## --- Day 7: The Treachery of Whales ---

A giant [whale](https://en.wikipedia.org/wiki/Sperm_whale) has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a _massive underground cave system_ just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of _the horizontal position of each crab_ (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

```
16,1,2,0,4,2,7,1,2,14
```

This means there's a crab with horizontal position `16`, a crab with horizontal position `1`, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position `2`:

-   Move from `16` to `2`: `14` fuel
-   Move from `1` to `2`: `1` fuel
-   Move from `2` to `2`: `0` fuel
-   Move from `0` to `2`: `2` fuel
-   Move from `4` to `2`: `2` fuel
-   Move from `2` to `2`: `0` fuel
-   Move from `7` to `2`: `5` fuel
-   Move from `1` to `2`: `1` fuel
-   Move from `2` to `2`: `0` fuel
-   Move from `14` to `2`: `12` fuel

This costs a total of `_37_` fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position `1` (`41` fuel), position `3` (`39` fuel), or position `10` (`71` fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. _How much fuel must they spend to align to that position?_

Some things I immediately noticed is that in this example the median of the dataset is where the crabs should meetup. This makes sense since it accounts for the dataset being skewed to somewhere not in the middle of the min/max.

My hypothesis was that we could sort the list, find the median, and that would be the meetup spot. Then we just loop through and calculate the fuel cost giving us `O(n log n)` time complexity (for sorting) and constant extra space.

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
positions = [int(x) for x in file_input[0].split(",")]
positions.sort()
meetup = positions[len(positions) // 2]

total = 0
for position in positions:
    total += abs(meetup - position)
print("Total Fuel Cost: " + str(total))
```

```bash
❯ python3 solution7.py input7
Total Fuel Cost: 341534
```

## --- Part Two ---

The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs `1`, the second step costs `2`, the third step costs `3`, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes `5`:

-   Move from `16` to `5`: `66` fuel
-   Move from `1` to `5`: `10` fuel
-   Move from `2` to `5`: `6` fuel
-   Move from `0` to `5`: `15` fuel
-   Move from `4` to `5`: `1` fuel
-   Move from `2` to `5`: `6` fuel
-   Move from `7` to `5`: `3` fuel
-   Move from `1` to `5`: `10` fuel
-   Move from `2` to `5`: `6` fuel
-   Move from `14` to `5`: `45` fuel

This costs a total of `_168_` fuel. This is the new cheapest possible outcome; the old alignment position (`2`) now costs `206` fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! _How much fuel must they spend to align to that position?_

I found a solution but it seems it can be off by one for the meetup location. Using the mean here works but the rounding can be tricky. One thing that should work is to take the mean rounded up and rounded down, calculate fuel cost for both and take the minimum. I was lazy and just tried this manually:

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
positions = [int(x) for x in file_input[0].split(",")]
positions.sort()
meetup = sum(positions) // len(positions)

total = 0
for position in positions:
    total += sum([i for i in range(1, abs(meetup - position)+1)])
print("Total Fuel Cost: " + str(total))
```

```bash
❯ python3 solution7.py input7
Total Fuel Cost: 93397632
```