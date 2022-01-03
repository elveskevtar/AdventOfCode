#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

bitstr_len = len(file_input[0])
gamma_map = {k: 0 for k in range(bitstr_len)}
for line in file_input:
    for i, char in enumerate(line):
        bit = int(char)
        gamma_map[bitstr_len - i - 1] += bit

gamma = 0
for pos, val in gamma_map.items():
    bit = (val * 2) // len(file_input)
    gamma += bit << pos

epsilon = ~gamma & (1 << bitstr_len) - 1
print("Power consumption: " + str(gamma * epsilon))

pos, common_list, uncommon_list = 0, file_input, file_input
while pos < bitstr_len:
    if len(common_list) == 1 and len(uncommon_list) == 1:
        break
    if len(common_list) > 1:
        common_map = {k: [] for k in [0,1]}
        for line in common_list:
            bit = int(line[pos])
            common_map[bit].append(line)
        if len(common_map[0]) > len(common_map[1]):
            common_list = common_map[0]
        else:
            common_list = common_map[1]
    if len(uncommon_list) > 1:
        uncommon_map = {k: [] for k in [0,1]}
        for line in uncommon_list:
            bit = int(line[pos])
            uncommon_map[bit].append(line)
        if len(uncommon_map[1]) < len(uncommon_map[0]):
            uncommon_list = uncommon_map[1]
        else:
            uncommon_list = uncommon_map[0]
    pos += 1

oxygen_generator_rating = int(common_list[0], 2)
co2_scrubber_rating = int(uncommon_list[0], 2)
print("Oxygen generator rating = " + str(oxygen_generator_rating))
print("CO2 scrubber rating = " + str(co2_scrubber_rating))
print("Life support rating = " + str(oxygen_generator_rating * co2_scrubber_rating))

