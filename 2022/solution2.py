#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

win_map = {
    "X": "Z",
    "Y": "X",
    "Z": "Y",
}
translation_map = {
    "A": "X",
    "B": "Y",
    "C": "Z",
}
choice_value = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

def calculate_score(games):
    total_score = 0
    for game in games:
        their_move, my_decision = game.split(" ")
        their_move = translation_map[their_move]
        if my_decision == "X":
            my_move = win_map[their_move]
        elif my_decision == "Y":
            total_score += 3
            my_move = their_move
        elif my_decision == "Z":
            total_score += 6
            my_move = list(
                filter(lambda i: i[1] == their_move, win_map.items())
            )[0][0]
        total_score += choice_value[my_move]
    return total_score

data = open(sys.argv[1], "r").read().strip().split("\n")
print(f"Total score would be {calculate_score(data)}")
