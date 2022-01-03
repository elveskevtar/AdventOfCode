#!/usr/bin/env python3
import sys

N = 5

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

class BingoSheet:
    def __init__(self, sheet):
        self.rows = sheet
        self.columns = [[] for i in range(N)]
        for row in sheet:
            for column, value in enumerate(row):
                self.columns[column].append(value)

    def mark_number(self, num):
        for row in self.rows:
            if num in row:
                row.remove(num)
                if len(row) == 0:
                    return True
                break
        for column in self.columns:
            if num in column:
                column.remove(num)
                if len(column) == 0:
                    return True
                break
        return False

    def board_sum(self):
        return sum([n for n in [sum(row) for row in self.rows]])

file_input = open(sys.argv[1], "r").read().strip().split("\n")
draw_nums = [int(x) for x in file_input[0].split(",")]

sheets = []
for i in range(2, len(file_input), 6):
    sheet = []
    for row in file_input[i:i+5]:
        nums = [int(num) for num in row.split()]
        sheet.append(nums)
    sheets.append(BingoSheet(sheet))

first = False
for num in draw_nums:
    for sheet in list(sheets):
        if sheet.mark_number(num):
            if not first:
                print("First Board Final Score: " + str(num * sheet.board_sum()))
                first = True
            sheets.remove(sheet)
        if len(sheets) == 0:
            print("Last Board Final Score: " + str(num * sheet.board_sum()))
            sys.exit(0)

