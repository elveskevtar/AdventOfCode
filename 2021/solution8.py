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

