#!/usr/bin/env python3
from collections import deque
from math import prod
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

decode_table = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

operator_map = {
    0: lambda x: sum(x),
    1: lambda x: prod(x),
    2: lambda x: min(x),
    3: lambda x: max(x),
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1])
}

file_input = open(sys.argv[1], "r").read().strip().split("\n")
hex_string = file_input[0]
#print(hex_string)

bin_string = ""
for char in hex_string:
    bin_string += decode_table[char]
#print(bin_string)

stack = deque()
unbin = lambda x: int(x, 2)
result, num_packets, version_total, i = 0, 0, 0, 0
while i < len(bin_string):
    if len(bin_string) - i < 11 and unbin(bin_string[i:len(bin_string)]) == 0:
        # break out of loop when we hit trailing zeroes less than minimum packet length
        break
    start_i = i
    version = unbin(bin_string[i:i+3]) # first three bits are version
    version_total += version
    type_id = unbin(bin_string[i+3:i+6]) # next three bits are packet type id
    if type_id != 4:
        # process operator packets
        length_type = unbin(bin_string[i+6])
        length = 11 if length_type else 15
        length_num = unbin(bin_string[i+7:i+7+length])
        i += 7 + length # move i to start of first sub-packet
        if len(stack) != 0:
            # track new bits and sub-packets in parent packet
            stack[-1]["num_bits"] += i - start_i
            stack[-1]["num_packets"] += 1
        stack.append({
            "result": [],
            "length_type": length_type,
            "length_num": length_num,
            "type_id": type_id,
            "num_bits": 0,
            "num_packets": 0
        })
        continue
    # process literals and stack reduction
    i += 6 # move i to the start of the literal
    literal = ""
    while unbin(bin_string[i]) == 1:
        # loop until we hit the last block
        literal += bin_string[i+1:i+5]
        i += 5
    literal += bin_string[i+1:i+5]
    literal = unbin(literal)
    i += 5
    if len(stack) == 0:
        # if packet is just a literal, we're done
        result = literal
        break
    stack[-1]["result"].append(literal) # track literal in top of operator stack

    if len(stack) != 0:
        # track new bits and sub-packets in parent operator packet
        stack[-1]["num_bits"] += i - start_i
        stack[-1]["num_packets"] += 1
    while len(stack) != 0:
        top = stack[-1]
        if not (top["length_type"] and top["length_num"] == top["num_packets"]) \
                and not (not top["length_type"] and top["length_num"] == top["num_bits"]):
            # if we are not finished with the top operator packet, continue
            break
        top = stack.pop()
        operation_result = operator_map[top["type_id"]](top["result"])
        if len(stack) == 0:
            # when done with our top-level operator packet, we are done
            result = operation_result
        else:
            # bubble up new bits to parent operator packet
            # note: no need to bubble up num_packets since we care about immediate children
            stack[-1]["num_bits"] += top["num_bits"]
            # take operation result from current packet and append to parent operator
            stack[-1]["result"].append(operation_result)

print("Version Total: {}".format(version_total))
print("Packet Result: {}".format(result))

