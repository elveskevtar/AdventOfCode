## --- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked _crates_, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a _giant cargo crane_ capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her _which_ crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates _and_ the rearrangement procedure (your puzzle input). For example:

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

In this example, there are three stacks of crates. Stack 1 contains two crates: crate `Z` is on the bottom, and crate `N` is on top. Stack 2 contains three crates; from bottom to top, they are crates `M`, `C`, and `D`. Finally, stack 3 contains a single crate, `P`.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

In the second step, three crates are moved from stack 1 to stack 3. Crates are moved _one at a time_, so the first crate to be moved (`D`) ends up below the second and third crates:

```
        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
```

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved _one at a time_, crate `C` ends up below crate `M`:

```
        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
```

Finally, one crate is moved from stack 1 to stack 2:

```
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
```

The Elves just need to know _which crate will end up on top of each stack_; in this example, the top crates are `C` in stack 1, `M` in stack 2, and `Z` in stack 3, so you should combine these together and give the Elves the message `_CMZ_`.

_After the rearrangement procedure completes, what crate ends up on top of each stack?_

```python
#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def get_rearrangement(instructions):
    num_stacks = 9
    stacks = [deque() for _ in range(num_stacks)]
    for instruction in instructions[:8]:
        for stack in range(num_stacks):
            label = instruction[stack * 4 + 1]
            if label != " ":
                stacks[stack].appendleft(label)
    
    for instruction in instructions[10:-1]:
        num_moves = int(instruction.split()[1])
        start = int(instruction.split()[3]) - 1
        dest = int(instruction.split()[5]) - 1
        for _ in range(num_moves):
            stacks[dest].append(stacks[start].pop())

    return "".join([stack.pop() for stack in stacks])

data = open(sys.argv[1], "r").read().split("\n")
print(f"Top of stacks labels: {get_rearrangement(data)}")
```

```bash
❯ python3 solution5.py input5
Top of stacks labels: VJSFHWGFT
```

## --- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a _CrateMover 9001_.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and _the ability to pick up and move multiple crates at once_.

Again considering the example above, the crates begin in the same configuration:

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

Moving a single crate from stack 2 to stack 1 behaves the same as before:

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates _stay in the same order_, resulting in this new configuration:

```
        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
```

Next, as both crates are moved from stack 2 to stack 1, they _retain their order_ as well:

```
        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
```

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate `C` that gets moved:

```
        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
```

In this example, the CrateMover 9001 has put the crates in a totally different order: `_MCD_`.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. _After the rearrangement procedure completes, what crate ends up on top of each stack?_

```python
def get_rearrangement(instructions):
    num_stacks = 9
    stacks = [deque() for _ in range(num_stacks)]
    for instruction in instructions[:8]:
        for stack in range(num_stacks):
            label = instruction[stack * 4 + 1]
            if label != " ":
                stacks[stack].appendleft(label)
    
    for instruction in instructions[10:-1]:
        num_moves = int(instruction.split()[1])
        start = int(instruction.split()[3]) - 1
        dest = int(instruction.split()[5]) - 1
        stacks[dest].extend(
            reversed([stacks[start].pop() for _ in range(num_moves)])
        )

    return "".join([stack.pop() for stack in stacks])
```

```bash
❯ python3 solution5.py input5
Top of stacks labels: LCTQFBVZV
```