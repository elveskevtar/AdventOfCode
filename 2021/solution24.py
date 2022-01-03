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

