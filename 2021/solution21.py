#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
p1start, p2start = tuple(map(lambda l: int(l[-1]), file_input[0:2]))

game_states = {}
def count_wins(p1, p2, p1score=0, p2score=0):
    if p1score >= 21:
        return (1,0)
    if p2score >= 21:
        return (0,1)
    if (p1, p2, p1score, p2score) in game_states:
        return game_states[p1, p2, p1score, p2score]
    result = (0,0)
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                _p1 = ((p1 + d1 + d2 + d3 - 1) % 10) + 1
                _p1score = p1score + _p1
                swap = count_wins(p2, _p1, p2score, _p1score)
                result = (result[0] + swap[1], result[1] + swap[0])
    game_states[p1, p2, p1score, p2score] = result
    return result

print("max(count_wins(p1start, p2start)): {}".format(max(count_wins(p1start, p2start))))

