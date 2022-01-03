## --- Day 24: Arithmetic Logic Unit ---

[Magic smoke](https://en.wikipedia.org/wiki/Magic_smoke) starts leaking from the submarine's [arithmetic logic unit](https://en.wikipedia.org/wiki/Arithmetic_logic_unit) (ALU). Without the ability to perform basic arithmetic and logic functions, the submarine can't produce cool patterns with its Christmas lights!

It also can't navigate. Or run the oxygen system.

Don't worry, though - you _probably_ have enough oxygen left to give you enough time to build a new ALU.

The ALU is a four-dimensional processing unit: it has integer variables `w`, `x`, `y`, and `z`. These variables all start with the value `0`. The ALU also supports _six instructions_:

-   `inp a` - Read an input value and write it to variable `a`.
-   `add a b` - Add the value of `a` to the value of `b`, then store the result in variable `a`.
-   `mul a b` - Multiply the value of `a` by the value of `b`, then store the result in variable `a`.
-   `div a b` - Divide the value of `a` by the value of `b`, truncate the result to an integer, then store the result in variable `a`. (Here, "truncate" means to round the value toward zero.)
-   `mod a b` - Divide the value of `a` by the value of `b`, then store the _remainder_ in variable `a`. (This is also called the [modulo](https://en.wikipedia.org/wiki/Modulo_operation) operation.)
-   `eql a b` - If the value of `a` and `b` are equal, then store the value `1` in variable `a`. Otherwise, store the value `0` in variable `a`.

In all of these instructions, `a` and `b` are placeholders; `a` will always be the variable where the result of the operation is stored (one of `w`, `x`, `y`, or `z`), while `b` can be either a variable or a number. Numbers can be positive or negative, but will always be integers.

The ALU has no _jump_ instructions; in an ALU program, every instruction is run exactly once in order from top to bottom. The program halts after the last instruction has finished executing.

(Program authors should be especially cautious; attempting to execute `div` with `b=0` or attempting to execute `mod` with `a<0` or `b<=0` will cause the program to crash and might even damage the ALU. These operations are never intended in any serious ALU program.)

For example, here is an ALU program which takes an input number, negates it, and stores it in `x`:

```
inp x
mul x -1
```

Here is an ALU program which takes two input numbers, then sets `z` to `1` if the second input number is three times larger than the first input number, or sets `z` to `0` otherwise:

```
inp z
inp x
mul z 3
eql z x
```

Here is an ALU program which takes a non-negative integer as input, converts it into binary, and stores the lowest (1's) bit in `z`, the second-lowest (2's) bit in `y`, the third-lowest (4's) bit in `x`, and the fourth-lowest (8's) bit in `w`:

```
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
```

Once you have built a replacement ALU, you can install it in the submarine, which will immediately resume what it was doing when the ALU failed: validating the submarine's _model number_. To do this, the ALU will run the MOdel Number Automatic Detector program (MONAD, your puzzle input).

Submarine model numbers are always _fourteen-digit numbers_ consisting only of digits `1` through `9`. The digit `0` _cannot_ appear in a model number.

When MONAD checks a hypothetical fourteen-digit model number, it uses fourteen separate `inp` instructions, each expecting a _single digit_ of the model number in order of most to least significant. (So, to check the model number `13579246899999`, you would give `1` to the first `inp` instruction, `3` to the second `inp` instruction, `5` to the third `inp` instruction, and so on.) This means that when operating MONAD, each input instruction should only ever be given an integer value of at least `1` and at most `9`.

Then, after MONAD has finished running all of its instructions, it will indicate that the model number was _valid_ by leaving a `0` in variable `z`. However, if the model number was _invalid_, it will leave some other non-zero value in `z`.

MONAD imposes additional, mysterious restrictions on model numbers, and legend says the last copy of the MONAD documentation was eaten by a [tanuki](https://en.wikipedia.org/wiki/Japanese_raccoon_dog). You'll need to _figure out what MONAD does_ some other way.

To enable as many submarine features as possible, find the largest valid fourteen-digit model number that contains no `0` digits. _What is the largest model number accepted by MONAD?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 3:
    print("Usage: {} <input file> <model #>".format(sys.argv[0]))
    sys.exit(1)

model_num = sys.argv[2]
if len(model_num) != 14 or not model_num.isnumeric() or "0" in model_num:
    print("Model number must be 14 digits with no 0's")
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

i = 0
variables = {var: 0 for var in ["w", "x", "y", "z"]}
for line in file_input:
    if line == "":
        continue
    instr = line.split()
    if instr[0] == "inp":
		print(variables)
        variables[instr[1]] = model_num[i]
        i += 1
    if instr[0] == "add":
        operand = instr[2] if instr[2].strip("-").isnumeric() else variables[instr[2]]
        variables[instr[1]] += int(operand)
    if instr[0] == "mul":
        operand = instr[2] if instr[2].strip("-").isnumeric() else variables[instr[2]]
        variables[instr[1]] *= int(operand)
    if instr[0] == "div":
        operand = instr[2] if instr[2].strip("-").isnumeric() else variables[instr[2]]
        if int(operand) == 0:
            print("Divide by zero error")
            sys.exit(1)
        variables[instr[1]] //= int(operand)
    if instr[0] == "mod":
        if variables[instr[1]] < 0:
            print("Modulo dividend < 0")
            sys.exit(1)
        operand = instr[2] if instr[2].strip("-").isnumeric() else variables[instr[2]]
        if int(operand) <= 0:
            print("Modulo divisor <= 0")
            sys.exit(1)
        variables[instr[1]] %= int(operand)
    if instr[0] == "eql":
        operand = instr[2] if instr[2].strip("-").isnumeric() else variables[instr[2]]
        variables[instr[1]] = int(variables[instr[1]] == int(operand))

print(variables)
```

```bash
❯ python3 solution24.py input24 11111111111111
{'w': '1', 'x': 1, 'y': 10, 'z': 3118601834}
```

```python
❯ python3 solution24.py input24 29991993698469
{'w': 0, 'x': 0, 'y': 0, 'z': 0}
{'w': '2', 'x': 1, 'y': 11, 'z': 11}
{'w': '9', 'x': 1, 'y': 10, 'z': 296}
{'w': '9', 'x': 1, 'y': 20, 'z': 7716}
{'w': '9', 'x': 1, 'y': 12, 'z': 200628}
{'w': '1', 'x': 0, 'y': 0, 'z': 7716}
{'w': '9', 'x': 1, 'y': 14, 'z': 200630}
{'w': '9', 'x': 1, 'y': 9, 'z': 5216389}
{'w': '3', 'x': 0, 'y': 0, 'z': 200630}
{'w': '6', 'x': 1, 'y': 15, 'z': 5216395}
{'w': '9', 'x': 0, 'y': 0, 'z': 200630}
{'w': '8', 'x': 0, 'y': 0, 'z': 7716}
{'w': '4', 'x': 0, 'y': 0, 'z': 296}
{'w': '6', 'x': 0, 'y': 0, 'z': 11}
{'w': '9', 'x': 0, 'y': 0, 'z': 0}
```

See handwritten notes for this one.

## --- Part Two ---

As the submarine starts booting up things like the [Retro Encabulator](https://www.youtube.com/watch?v=RXJKdh1KZ0w), you realize that maybe you don't need all these submarine features after all.

_What is the smallest model number accepted by MONAD?_

```bash
❯ python3 solution24.py input24 14691271141118
{'w': 0, 'x': 0, 'y': 0, 'z': 0}
{'w': '1', 'x': 1, 'y': 10, 'z': 10}
{'w': '4', 'x': 1, 'y': 5, 'z': 265}
{'w': '6', 'x': 1, 'y': 17, 'z': 6907}
{'w': '9', 'x': 1, 'y': 12, 'z': 179594}
{'w': '1', 'x': 0, 'y': 0, 'z': 6907}
{'w': '2', 'x': 1, 'y': 7, 'z': 179589}
{'w': '7', 'x': 1, 'y': 7, 'z': 4669321}
{'w': '1', 'x': 0, 'y': 0, 'z': 179589}
{'w': '1', 'x': 1, 'y': 10, 'z': 4669324}
{'w': '4', 'x': 0, 'y': 0, 'z': 179589}
{'w': '1', 'x': 0, 'y': 0, 'z': 6907}
{'w': '1', 'x': 0, 'y': 0, 'z': 265}
{'w': '1', 'x': 0, 'y': 0, 'z': 10}
{'w': '8', 'x': 0, 'y': 0, 'z': 0}
```

Same thing but with lowest numbers.