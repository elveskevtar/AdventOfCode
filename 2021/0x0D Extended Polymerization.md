## --- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has [polymerization](https://en.wikipedia.org/wiki/Polymerization) equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a _polymer template_ and a list of _pair insertion_ rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

```
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
```

The first line is the _polymer template_ - this is the starting point of the process.

The following section defines the _pair insertion_ rules. A rule like `AB -> C` means that when elements `A` and `B` are immediately adjacent, element `C` should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template `NNCB`, the first step simultaneously considers all three pairs:

-   The first pair (`NN`) matches the rule `NN -> C`, so element `_C_` is inserted between the first `N` and the second `N`.
-   The second pair (`NC`) matches the rule `NC -> B`, so element `_B_` is inserted between the `N` and the `C`.
-   The third pair (`CB`) matches the rule `CB -> H`, so element `_H_` is inserted between the `C` and the `B`.

Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes `N_C_N_B_C_H_B`.

Here are the results of a few steps using the above rules:

```
Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
```

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, `B` occurs 1749 times, `C` occurs 298 times, `H` occurs 161 times, and `N` occurs 865 times; taking the quantity of the most common element (`B`, 1749) and subtracting the quantity of the least common element (`H`, 161) produces `1749 - 161 = _1588_`.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. _What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

insertion_map = {}
for line in file_input[2:]:
    if line == "":
        continue
    template, insertion = line.split()[0], line.split()[-1]
    insertion_map[template] = insertion

start = file_input[0]
for i in range(10):
    result = ""
    for j in range(len(str(start)) - 1):
        template = start[j:j+2]
        if j == 0:
            result += template[0]
        result += insertion_map[template] + template[1]
    start = result

freq_count = {char:start.count(char) for char in set(start)}

least = min(freq_count.values())
most = max(freq_count.values())
print("Most - Least common = {}".format(most - least))
```

```bash
❯ python3 solution14.py input14
Most - Least common = 2937
```

## --- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of _40 steps_ should do it.

In the above example, the most common element is `B` (occurring `2192039569602` times) and the least common element is `H` (occurring `3849876073` times); subtracting these produces `_2188189693529_`.

Apply _40_ steps of pair insertion to the polymer template and find the most and least common elements in the result. _What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

insertion_map = {}
for line in file_input[2:]:
    if line == "":
        continue
    template, insertion = line.split()[0], line.split()[-1]
    insertion_map[template] = insertion

start = file_input[0]
templates = {}
for j in range(len(start)-1):
    template = start[j:j+2]
    templates[template] = templates.get(template, 0) + 1

freq_count = {char:start.count(char) for char in set(start)}
for i in range(40):
    for template, freq in dict(templates).items():
        templates[template] -= freq
        insertion = insertion_map[template]
        first, second = template[0] + insertion, insertion + template[1]
        templates[first] = templates.get(first, 0) + freq
        templates[second] = templates.get(second, 0) + freq
        freq_count[insertion] = freq_count.get(insertion, 0) + freq

least = min(freq_count.values())
most = max(freq_count.values())
print("Most - Least common = {}".format(most - least))
```

```bash
❯ python3 solution14.py input14
Most - Least common = 3390034818249
```