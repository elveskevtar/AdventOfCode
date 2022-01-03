## --- Day 23: Amphipod ---

A group of [amphipods](https://en.wikipedia.org/wiki/Amphipoda) notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod says, "surely you can help us with a question that has stumped our best scientists."

They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods live there: _Amber_ (`A`), _Bronze_ (`B`), _Copper_ (`C`), and _Desert_ (`D`). They live in a burrow that consists of a _hallway_ and four _side rooms_. The side rooms are initially full of amphipods, and the hallway is initially empty.

They give you a _diagram of the situation_ (your puzzle input), including locations of each amphipod (`A`, `B`, `C`, or `D`, each of which is occupying an otherwise open space), walls (`#`), and open space (`.`).

For example:

```
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
```

The amphipods would like a method to organize every amphipod into side rooms so that each side room contains one type of amphipod and the types are sorted `A`-`D` going left to right, like this:

```
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
```

Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each type of amphipod requires a different amount of _energy_ to move one step: Amber amphipods require `1` energy per step, Bronze amphipods require `10` energy, Copper amphipods require `100`, and Desert ones require `1000`. The amphipods would like you to find a way to organize the amphipods that requires the _least total energy_.

However, because they are timid and stubborn, the amphipods have some extra rules:

-   Amphipods will never _stop on the space immediately outside any room_. They can move into that space so long as they immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly above an amphipod starting position.)
-   Amphipods will never _move from the hallway into a room_ unless that room is their destination room _and_ that room contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.)
-   Once an amphipod stops moving in the hallway, _it will stay in that spot until it can move into a room_. (That is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move again until they can move fully into a room.)

In the above example, the amphipods can be organized using a minimum of `_12521_` energy. One way to do this is shown below.

Starting configuration:

```
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
```

One Bronze amphipod moves into the hallway, taking 4 steps and using `40` energy:

```
#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
```

The only Copper amphipod not in its side room moves there, taking 4 steps and using `400` energy:

```
#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########
```

A Desert amphipod moves out of the way, taking 3 steps and using `3000` energy, and then the Bronze amphipod takes its place, taking 3 steps and using `30` energy:

```
#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########
```

The leftmost Bronze amphipod moves to its room using `40` energy:

```
#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
```

Both amphipods in the rightmost room move into the hallway, using `2003` energy in total:

```
#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
```

Both Desert amphipods move into the rightmost room using `7000` energy:

```
#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########
```

Finally, the last Amber amphipod moves into its room, using `8` energy:

```
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
```

_What is the least energy required to organize the amphipods?_

```python
#!/usr/bin/env python3
from collections import deque
from copy import deepcopy
from heapq import heappush
from math import copysign
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
amphipod_dst = {"A": 2, "B": 4, "C": 6, "D": 8}

class Amphipod:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.moved = False
        self.points = 0

    def move(self, new_pos, field):
        self.moved = True
        moves = abs(self.pos[0] - new_pos[0]) + abs(self.pos[1] - new_pos[1])
        self.points += moves * multiplier[self.label]
        field[new_pos] = self
        field[self.pos] = None
        self.pos = new_pos

    def __repr__(self):
        return "Amphipod({})".format(self.label)

    def __eq__(self, other):
        return other and self.label == other.label \
                and self.pos == other.pos and self.moved == other.moved \
                and self.points == other.points

    def __hash__(self):
        return hash((self.label, self.pos, self.moved, self.points))

def field_score(field):
    points = 0
    for pod in field.values():
        if pod is not None:
            points += pod.points
    return points

def hash_field(field):
    states = []
    for pod in field.values():
        if pod is not None:
            states.append(hash(pod))
    states.sort()
    return hash(tuple(states))

def field_solved(field):
    return field[2,1] and field[2,2] and field[4,1] and field[4,2] \
            and field[6,1] and field[6,2] and field[8,1] and field[8,2] \
            and field[2,1].label == "A" and field[2,2].label == "A" \
            and field[4,1].label == "B" and field[4,2].label == "B" \
            and field[6,1].label == "C" and field[6,2].label == "C" \
            and field[8,1].label == "D" and field[8,2].label == "D"

def print_field(field):
    for y in range(3):
        result = ""
        for x in range(11):
            if (x,y) not in field:
                result += "#"
            elif field[x,y] is None:
                result += "."
            else:
                result += field[x,y].label
        print(result)
    print("")

field = {(x,0):None for x in range(11)}

for x in range(4):
    x = x*2 + 3
    field[x-1,1] = Amphipod(file_input[2][x], (x-1,1))
    field[x-1,2] = Amphipod(file_input[3][x], (x-1,2))

visited_states = set()
queue = deque()
queue.append(field)
room_rows = [2,4,6,8]
min_energy_cost = sys.maxsize
while len(queue) != 0:
    field = queue.pop()
    field_hash = hash_field(field)
    if field_hash in visited_states or field_score(field) > min_energy_cost:
        continue
    visited_states.add(field_hash)
    if field_solved(field):
        min_energy_cost = min(min_energy_cost, field_score(field))
        print(min_energy_cost)
        continue
    for y in range(1,3):
        for x in range(4):
            x = x*2 + 2
            if field[x,y-1]: continue
            if field[x,y] and not field[x,y].moved:
                for x2 in range(x-1, -1, -1):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = deepcopy(field)
                    amphipod = new_field[x,y]
                    amphipod.move((x2,0), new_field)
                    queue.append(new_field)
                for x2 in range(x+1, 11):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = deepcopy(field)
                    amphipod = new_field[x,y]
                    amphipod.move((x2,0), new_field)
                    queue.append(new_field)
    for x in range(11):
        if not field[x,0]: continue
        dest = amphipod_dst[field[x,0].label]
        if field[dest,1]: continue
        if field[dest,2] and field[dest,2].label != field[x,0].label: continue
        direction = int(copysign(1, dest-x))
        for x2 in range(x+direction, dest+direction, direction):
            if field[x2,0]: break
            if x2 != dest: continue
            if field[x2,2]:
                new_field = deepcopy(field)
                amphipod = new_field[x,0]
                amphipod.move((x2,1), new_field)
                queue.append(new_field)
            else:
                new_field = deepcopy(field)
                amphipod = new_field[x,0]
                amphipod.move((x2,2), new_field)
                queue.append(new_field)
```

With heap instead of queue:
```python
#!/usr/bin/env python3
from copy import deepcopy
from heapq import heappush, heappop
from math import copysign
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
amphipod_dst = {"A": 2, "B": 4, "C": 6, "D": 8}

class Amphipod:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.moved = False

    def move(self, new_pos, field):
        self.moved = True
        moves = abs(self.pos[0] - new_pos[0]) + abs(self.pos[1] - new_pos[1])
        field.field[new_pos] = self
        field.field[self.pos] = None
        self.pos = new_pos
        field.points += moves * multiplier[self.label]

    def __repr__(self):
        return "Amphipod({})".format(self.label)

    def __eq__(self, other):
        return other and self.label == other.label \
                and self.pos == other.pos and self.moved == other.moved

    def __hash__(self):
        return hash((self.label, self.pos, self.moved))

class Field:
    def __init__(self, field, points):
        self.field = field
        self.points = points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.field == other.field and self.points == other.points

    def __hash__(self):
        states = []
        for pod in self.field.values():
            if pod:
                states.append(hash(pod))
        states.sort()
        return hash(tuple(states))

    def solved(self):
        field = self.field
        return field[2,1] and field[2,2] and field[4,1] and field[4,2] \
            and field[6,1] and field[6,2] and field[8,1] and field[8,2] \
            and field[2,1].label == "A" and field[2,2].label == "A" \
            and field[4,1].label == "B" and field[4,2].label == "B" \
            and field[6,1].label == "C" and field[6,2].label == "C" \
            and field[8,1].label == "D" and field[8,2].label == "D"

def print_field(field):
    for y in range(3):
        result = ""
        for x in range(11):
            if (x,y) not in field:
                result += "#"
            elif field[x,y] is None:
                result += "."
            else:
                result += field[x,y].label
        print(result)
    print("")

field = {(x,0):None for x in range(11)}
for x in range(4):
    x = x*2 + 3
    field[x-1,1] = Amphipod(file_input[2][x], (x-1,1))
    field[x-1,2] = Amphipod(file_input[3][x], (x-1,2))
field = Field(field, 0)

queue = []
heappush(queue, field)
visited_states = set()
room_rows = [2,4,6,8]
min_energy_cost = sys.maxsize
while len(queue) != 0:
    field_obj = heappop(queue)
    field_hash, field, score = hash(field_obj), field_obj.field, field_obj.points
    if field_hash in visited_states or score > min_energy_cost:
        continue
    visited_states.add(field_hash)
    if field_obj.solved():
        min_energy_cost = min(min_energy_cost, score)
        print(min_energy_cost)
        continue
    for y in range(1,3):
        for x in range(4):
            x = x*2 + 2
            if field[x,y-1]: continue
            if field[x,y] and not field[x,y].moved:
                for x2 in range(x-1, -1, -1):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = deepcopy(field_obj)
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
                for x2 in range(x+1, 11):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = deepcopy(field_obj)
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
    for x in range(11):
        if not field[x,0]: continue
        dest = amphipod_dst[field[x,0].label]
        if field[dest,1]: continue
        if field[dest,2] and field[dest,2].label != field[x,0].label: continue
        direction = int(copysign(1, dest-x))
        for x2 in range(x+direction, dest+direction, direction):
            if field[x2,0]: break
            if x2 != dest: continue
            if field[x2,2]:
                new_field = deepcopy(field_obj)
                new_field.field[x,0].move((x2,1), new_field)
                heappush(queue, new_field)
            else:
                new_field = deepcopy(field_obj)
                new_field.field[x,0].move((x2,2), new_field)
                heappush(queue, new_field)
```

```bash
❯ time python3 solution23.py input23
15472
python3 solution23.py input23  22.77s user 0.02s system 99% cpu 22.799 total
```

```bash
❯ python3 -m cProfile solution23.py input23
15472
         232307975 function calls (192139718 primitive calls) in 64.252 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1002(_find_and_load)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:112(release)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:152(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:156(__enter__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:160(__exit__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:166(_get_module_lock)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:185(cb)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:220(_call_with_frames_removed)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:231(_verbose_message)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:241(_requires_builtin_wrapper)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:351(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:398(parent)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:406(has_location)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:415(spec_from_loader)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:486(_init_module_attrs)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:558(module_from_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:58(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:659(_load_unlocked)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:736(find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:757(create_module)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:765(exec_module)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:782(is_package)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:87(acquire)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:874(__enter__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:878(__exit__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:901(_find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:967(_find_and_load_unlocked)
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:319(decode)
33405220/204940   25.224    0.000   58.382    0.000 copy.py:128(deepcopy)
 23977980    1.640    0.000    1.640    0.000 copy.py:182(_deepcopy_atomic)
  5533380    5.778    0.000   18.299    0.000 copy.py:209(_deepcopy_tuple)
  5533380    2.337    0.000   12.156    0.000 copy.py:210(<listcomp>)
2049400/204940    4.862    0.000   56.003    0.000 copy.py:226(_deepcopy_dict)
  3893860    1.744    0.000    2.412    0.000 copy.py:242(_keep_alive)
1844460/204940    4.039    0.000   57.399    0.000 copy.py:258(_reconstruct)
  3688920    0.736    0.000    2.583    0.000 copy.py:263(<genexpr>)
        2    0.000    0.000    0.000    0.000 copyreg.py:103(_slotnames)
  1844460    0.510    0.000    0.761    0.000 copyreg.py:94(__newobj__)
        1    0.000    0.000    0.000    0.000 solution23.py:16(Amphipod)
        8    0.000    0.000    0.000    0.000 solution23.py:17(__init__)
        1    2.074    2.074   64.252   64.252 solution23.py:2(<module>)
   204940    0.339    0.000    0.384    0.000 solution23.py:22(move)
  1639528    0.532    0.000    0.717    0.000 solution23.py:37(__hash__)
        1    0.000    0.000    0.000    0.000 solution23.py:40(Field)
        1    0.000    0.000    0.000    0.000 solution23.py:41(__init__)
  3432138    0.643    0.000    0.643    0.000 solution23.py:45(__lt__)
   204941    0.720    0.000    2.023    0.000 solution23.py:51(__hash__)
    80584    0.028    0.000    0.028    0.000 solution23.py:59(solved)
        1    0.000    0.000    0.000    0.000 solution23.py:81(<dictcomp>)
  1844460    0.251    0.000    0.251    0.000 {built-in method __new__ of type object at 0x8f32e0}
        1    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
   204941    0.437    0.000    1.003    0.000 {built-in method _heapq.heappop}
   204941    0.112    0.000    0.190    0.000 {built-in method _heapq.heappush}
        3    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.exec_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
        3    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
        1    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        2    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
        2    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
   409880    0.045    0.000    0.045    0.000 {built-in method builtins.abs}
        1    0.000    0.000   64.252   64.252 {built-in method builtins.exec}
  3688924    0.462    0.000    0.462    0.000 {built-in method builtins.getattr}
  1844466    0.211    0.000    0.211    0.000 {built-in method builtins.hasattr}
3688938/204941    0.617    0.000    2.108    0.000 {built-in method builtins.hash}
 46931260    3.257    0.000    3.257    0.000 {built-in method builtins.id}
  3688920    0.427    0.000    0.427    0.000 {built-in method builtins.isinstance}
  1844460    0.215    0.000    0.215    0.000 {built-in method builtins.issubclass}
   204943    0.025    0.000    0.025    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.min}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
   206436    0.047    0.000    0.047    0.000 {built-in method math.copysign}
        2    0.000    0.000    0.000    0.000 {method '__exit__' of '_thread.lock' objects}
  1844460    0.832    0.000    0.832    0.000 {method '__reduce_ex__' of 'object' objects}
    80584    0.012    0.000    0.012    0.000 {method 'add' of 'set' objects}
  5328448    0.497    0.000    0.497    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 68654902    4.899    0.000    4.899    0.000 {method 'get' of 'dict' objects}
        2    0.000    0.000    0.000    0.000 {method 'get' of 'mappingproxy' objects}
  2049400    0.214    0.000    0.214    0.000 {method 'items' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'pop' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'read' of '_io.TextIOWrapper' objects}
        2    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
   204941    0.103    0.000    0.103    0.000 {method 'sort' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
  1844460    0.359    0.000    0.359    0.000 {method 'update' of 'dict' objects}
   204941    0.026    0.000    0.026    0.000 {method 'values' of 'dict' objects}
```

New custom copy down to five seconds:
```bash
❯ time python3 solution23.py input23
Minimum energy cost: 15472
python3 solution23.py input23  4.66s user 0.02s system 99% cpu 4.685 total
```

```python
#!/usr/bin/env python3
from copy import copy, deepcopy
from heapq import heappush, heappop
from math import copysign
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
amphipod_dst = {"A": 2, "B": 4, "C": 6, "D": 8}

class Amphipod:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.moved = False

    def move(self, new_pos, field):
        self.moved = True
        moves = abs(self.pos[0] - new_pos[0]) + abs(self.pos[1] - new_pos[1])
        field.field[new_pos] = self
        field.field[self.pos] = None
        self.pos = new_pos
        field.points += moves * multiplier[self.label]

    def __repr__(self):
        return "Amphipod({})".format(self.label)

    def __eq__(self, other):
        return other and self.label == other.label \
                and self.pos == other.pos and self.moved == other.moved

    def __hash__(self):
        return hash((self.label, self.pos, self.moved))

class Field:
    def __init__(self, field, points):
        self.field = field
        self.points = points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.field == other.field and self.points == other.points

    def __hash__(self):
        states = []
        for pod in self.field.values():
            if pod:
                states.append(hash(pod))
        states.sort()
        return hash(tuple(states))

    def custom_copy(self, pos):
        # shallow copy field dict and points
        field = copy(self.field)
        points = copy(self.points)
        obj = Field(field, points)
        # deepcopy single amphipod object at position
        obj.field[pos] = deepcopy(obj.field[pos])
        return obj

    def solved(self):
        field = self.field
        return field[2,1] and field[2,2] and field[4,1] and field[4,2] \
            and field[6,1] and field[6,2] and field[8,1] and field[8,2] \
            and field[2,1].label == "A" and field[2,2].label == "A" \
            and field[4,1].label == "B" and field[4,2].label == "B" \
            and field[6,1].label == "C" and field[6,2].label == "C" \
            and field[8,1].label == "D" and field[8,2].label == "D"

def print_field(field):
    for y in range(3):
        result = ""
        for x in range(11):
            if (x,y) not in field:
                result += "#"
            elif field[x,y] is None:
                result += "."
            else:
                result += field[x,y].label
        print(result)
    print("")

field = {(x,0):None for x in range(11)}
for x in range(4):
    x = x*2 + 3
    field[x-1,1] = Amphipod(file_input[2][x], (x-1,1))
    field[x-1,2] = Amphipod(file_input[3][x], (x-1,2))
field = Field(field, 0)

queue = []
heappush(queue, field)
visited_states = set()
room_rows = [2,4,6,8]
min_energy_cost = sys.maxsize
while len(queue) != 0:
    field_obj = heappop(queue)
    field_hash, field, score = hash(field_obj), field_obj.field, field_obj.points
    if field_hash in visited_states or score > min_energy_cost:
        continue
    visited_states.add(field_hash)
    if field_obj.solved():
        min_energy_cost = min(min_energy_cost, score)
        continue
    for y in range(1,3):
        for x in range(4):
            x = x*2 + 2
            if field[x,y-1]: continue
            if field[x,y] and not field[x,y].moved:
                for x2 in range(x-1, -1, -1):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
                for x2 in range(x+1, 11):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
    for x in range(11):
        if not field[x,0]: continue
        dest = amphipod_dst[field[x,0].label]
        if field[dest,1]: continue
        if field[dest,2] and field[dest,2].label != field[x,0].label: continue
        direction = int(copysign(1, dest-x))
        for x2 in range(x+direction, dest+direction, direction):
            if field[x2,0]: break
            if x2 != dest: continue
            if field[x2,2]:
                new_field = field_obj.custom_copy((x,0))
                new_field.field[x,0].move((x2,1), new_field)
                heappush(queue, new_field)
            else:
                new_field = field_obj.custom_copy((x,0))
                new_field.field[x,0].move((x2,2), new_field)
                heappush(queue, new_field)

print("Minimum energy cost: {}".format(min_energy_cost))
```

## --- Part Two ---

As you prepare to give the amphipods your solution, you notice that the diagram they handed you was actually folded up. As you unfold it, you discover an extra part of the diagram.

Between the first and second lines of text that contain amphipod starting positions, insert the following lines:

```
  #D#C#B#A#
  #D#B#A#C#
```

So, the above example now becomes:

```
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
```

The amphipods still want to be organized into rooms similar to before:

```
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
```

In this updated example, the least energy required to organize these amphipods is `_44169_`:

```
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
```

Using the initial configuration from the full diagram, _what is the least energy required to organize the amphipods?_

```python
#!/usr/bin/env python3
from copy import copy, deepcopy
from heapq import heappush, heappop
from math import copysign
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

multiplier = {"A": 1, "B": 10, "C": 100, "D": 1000}
amphipod_dst = {"A": 2, "B": 4, "C": 6, "D": 8}

class Amphipod:
    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.moved = False

    def move(self, new_pos, field):
        self.moved = True
        moves = abs(self.pos[0] - new_pos[0]) + abs(self.pos[1] - new_pos[1])
        field.field[new_pos] = self
        field.field[self.pos] = None
        self.pos = new_pos
        field.points += moves * multiplier[self.label]

    def __repr__(self):
        return "Amphipod({})".format(self.label)

    def __eq__(self, other):
        return other and self.label == other.label \
                and self.pos == other.pos and self.moved == other.moved

    def __hash__(self):
        return hash((self.label, self.pos, self.moved))

class Field:
    def __init__(self, field, points):
        self.field = field
        self.points = points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.field == other.field and self.points == other.points

    def __hash__(self):
        states = []
        for pod in self.field.values():
            if pod:
                states.append(hash(pod))
        states.sort()
        return hash(tuple(states))

    def custom_copy(self, pos):
        # shallow copy field dict and points
        field = copy(self.field)
        points = copy(self.points)
        obj = Field(field, points)
        # deepcopy single amphipod object at position
        obj.field[pos] = deepcopy(obj.field[pos])
        return obj

    def solved(self):
        field = self.field
        for y in range(1,5):
            for x in range(4):
                x = x*2 + 2
                if not field[x,y]: return False
                if amphipod_dst[field[x,y].label] != x: return False
        return True

def print_field(field):
    for y in range(5):
        result = ""
        for x in range(11):
            if (x,y) not in field:
                result += "#"
            elif field[x,y] is None:
                result += "."
            else:
                result += field[x,y].label
        print(result)
    print("")

field = {(x,0):None for x in range(11)}
field[2,2] = Amphipod("D", (2,2))
field[2,3] = Amphipod("D", (2,3))
field[4,2] = Amphipod("C", (4,2))
field[4,3] = Amphipod("B", (4,3))
field[6,2] = Amphipod("B", (6,2))
field[6,3] = Amphipod("A", (6,3))
field[8,2] = Amphipod("A", (8,2))
field[8,3] = Amphipod("C", (8,3))
for x in range(4):
    x = x*2 + 3
    field[x-1,1] = Amphipod(file_input[2][x], (x-1,1))
    field[x-1,4] = Amphipod(file_input[3][x], (x-1,4))
field = Field(field, 0)

queue = []
heappush(queue, field)
visited_states = set()
room_rows = [2,4,6,8]
min_energy_cost = sys.maxsize
while len(queue) != 0:
    field_obj = heappop(queue)
    field_hash, field, score = hash(field_obj), field_obj.field, field_obj.points
    if field_hash in visited_states or score > min_energy_cost:
        continue
    visited_states.add(field_hash)
    if field_obj.solved():
        min_energy_cost = min(min_energy_cost, score)
        continue
    for y in range(1,5):
        for x in range(4):
            x = x*2 + 2
            if field[x,y] and not field[x,y].moved:
                blocked = False
                for y2 in range(y-1, 0, -1):
                    if field[x,y2]:
                        blocked = True
                        break
                if blocked: continue
                for x2 in range(x-1, -1, -1):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
                for x2 in range(x+1, 11):
                    if x2 in room_rows: continue
                    if field[x2,0]: break
                    new_field = field_obj.custom_copy((x,y))
                    new_field.field[x,y].move((x2,0), new_field)
                    heappush(queue, new_field)
    for x in range(11):
        if not field[x,0]: continue
        dest = amphipod_dst[field[x,0].label]
        if field[dest,1]: continue
        room_available = True
        for y in range(4, 1, -1):
            if field[dest,y] and field[dest,y].label != field[x,0].label:
                room_available = False
        if not room_available: continue
        direction = int(copysign(1, dest-x))
        for x2 in range(x+direction, dest+direction, direction):
            if field[x2,0]: break
            if x2 != dest: continue
            for y in range(4, 0, -1):
                if not field[x2,y]:
                    new_field = field_obj.custom_copy((x,0))
                    new_field.field[x,0].move((x2,y), new_field)
                    heappush(queue, new_field)
                    break

print("Minimum energy cost: {}".format(min_energy_cost))
```

```bash
❯ time python3 solution23.py input23
Minimum energy cost: 46182
python3 solution23.py input23  5.93s user 0.02s system 99% cpu 5.949 total
```