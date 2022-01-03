## --- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit [seven-segment displays](https://en.wikipedia.org/wiki/Seven-segment_display) in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named `a` through `g`:

```
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
```

So, to render a `1`, only segments `c` and `f` would be turned on; the rest would be off. To render a `7`, only segments `a`, `c`, and `f` would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires `a` through `g`, but those wires are connected to segments _randomly_. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits _within_ a display use the same connections, though.)

So, you might know that only signal wires `b` and `g` are turned on, but that doesn't mean _segments_ `b` and `g` are turned on: the only digit that uses two segments is `1`, so it must mean segments `c` and `f` are meant to be on. With just that information, you still can't tell which wire (`b`/`g`) goes to which segment (`c`/`f`). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of _all ten unique signal patterns_ you see, and then write down a single _four digit output value_ (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

```
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
```

(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten _unique signal patterns_, a `|` delimiter, and finally the _four digit output value_. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because `7` is the only digit that uses three segments, `dab` in the above example means that to render a `7`, signal lines `d`, `a`, and `b` are on. Because `4` is the only digit that uses four segments, `eafb` means that to render a `4`, signal lines `e`, `a`, `f`, and `b` are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (`cdfeb fcadb cdfeb cdbaf`) use five segments and are more difficult to deduce.

For now, _focus on the easy digits_. Consider this larger example:

```
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
```

Because the digits `1`, `4`, `7`, and `8` each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting _only digits in the output values_ (the part after `|` on each line), in the above example, there are `_26_` instances of digits that use a unique number of segments (highlighted above).

_In the output values, how many times do digits `1`, `4`, `7`, or `8` appear?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

simple_digits = 0
for line in file_input:
    output = line.split("|")[1].split()
    for code in output:
        if len(code) in [2,4,3,7]:
            simple_digits += 1

print("Simple digits: " + str(simple_digits))
```

```bash
❯ python3 solution8.py input8
Simple digits: 416
```

## --- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

```
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
```

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

```
 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
```

So, the unique signal patterns would correspond to the following digits:

-   `acedgfb`: `8`
-   `cdfbe`: `5`
-   `gcdfa`: `2`
-   `fbcad`: `3`
-   `dab`: `7`
-   `cefabd`: `9`
-   `cdfgeb`: `6`
-   `eafb`: `4`
-   `cagedb`: `0`
-   `ab`: `1`

Then, the four digits of the output value can be decoded:

-   `cdfeb`: `_5_`
-   `fcadb`: `_3_`
-   `cdfeb`: `_5_`
-   `cdbaf`: `_3_`

Therefore, the output value for this entry is `_5353_`.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

-   `fdgacbe cefdb cefbgd gcbe`: `8394`
-   `fcgedb cgb dgebacf gc`: `9781`
-   `cg cg fdcagb cbg`: `1197`
-   `efabcd cedba gadfec cb`: `9361`
-   `gecf egdcabf bgf bfgea`: `4873`
-   `gebdcfa ecba ca fadegcb`: `8418`
-   `cefg dcbef fcge gbcadfe`: `4548`
-   `ed bcgafe cdgba cbgef`: `1625`
-   `gbdfcae bgc cg cgb`: `8717`
-   `fgae cfgab fg bagce`: `4315`

Adding all of the output values in this larger example produces `_61229_`.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. _What do you get if you add up all of the output values?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

# set(1) = len(2)
# set(7) = len(3)
# set(4) = len(4)
# set(8) = len(7)
# len(6) = set(9) | set(6) | set(0)
# len(5) = set(3) | set(2) | set(5)
# top    = set(7) - set(1)
# set(9) = len(6) & issubset(set(4))
# bottom = set(9) - set(4) - top
# set(0) = len(6) & not(set(9)) & issubset(set(1))
# set(6) = len(6) & not(set(9)) & not(set(0))
# set(3) = len(5) & issubset(set(1))
# set(5) = len(5) & not(set(3)) & set(5) + set(9) == set(9)
# set(2) = len(5) & not(set(3)) & not(set(5))

total = 0
for line in file_input:
    length_map = {i:[] for i in range(2,8)}
    inp, output = [x.split() for x in line.split("|")]
    for i in inp:
        length_map[len(i)].append(i)
    set1 = set(length_map[2][0])
    set7 = set(length_map[3][0])
    set4 = set(length_map[4][0])
    set8 = set(length_map[7][0])
    len5 = [set(x) for x in length_map[5]]
    len6 = [set(x) for x in length_map[6]]
    top = set7 - set1
    set9 = list(filter(lambda x: set4.issubset(x), len6))[0]
    bottom = set9 - set4 - top
    set0 = list(filter(lambda x: x != set9 and set1.issubset(x), len6))[0]
    set6 = list(filter(lambda x: x != set0 and x != set9, len6))[0]
    set3 = list(filter(lambda x: set1.issubset(x), len5))[0]
    set5 = list(filter(lambda x: x != set3 and x.union(set9) == set9, len5))[0]
    set2 = list(filter(lambda x: x != set3 and x != set5, len5))[0]
    configurations = {
        frozenset(set0): 0,
        frozenset(set1): 1,
        frozenset(set2): 2,
        frozenset(set3): 3,
        frozenset(set4): 4,
        frozenset(set5): 5,
        frozenset(set6): 6,
        frozenset(set7): 7,
        frozenset(set8): 8,
        frozenset(set9): 9
    }
    result = ""
    for num in output:
        result += str(configurations[frozenset(num)])
    result = int(result)
    total += result

print("Final total: " + str(total))
```

```bash
❯ python3 solution8.py input8
Final total: 1043697
```