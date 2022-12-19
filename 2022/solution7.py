#!/usr/bin/env python3
from collections import deque
import heapq
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.sub_directories = {}
        self.files = []
    
    def add_file(self, name, size):
        self.files.append(File(name, size))

    def add_directory(self, name):
        self.sub_directories[name] = Directory(name, self)

    def calculate_size(self):
        running_total = 0
        for dir in self.sub_directories.values():
            running_total += dir.calculate_size()
        for next_file in self.files:
            running_total += next_file.size
        return running_total


def parse_commands(command_stream):
    curr_dir = root_dir = Directory("/", None)
    for line in command_stream[1:]:
        if line[0] == "$":
            command = line.split()[1]
            if command == "cd":
                dest = line.split()[2]
                if dest == "..":
                    curr_dir = curr_dir.parent
                elif dest == "/":
                    curr_dir = root_dir
                else:
                    curr_dir = curr_dir.sub_directories[dest]
            elif command == "ls":
                continue
        else:
            entry = line.split()
            if entry[0] == "dir":
                curr_dir.add_directory(entry[1])
            else:
                curr_dir.add_file(entry[1], int(entry[0]))
    
    dir_sizes = []
    dir_tree = deque()
    dir_tree.append(root_dir)
    while len(dir_tree) != 0:
        next_dir = dir_tree.pop()
        dir_tree.extend(next_dir.sub_directories.values())
        heapq.heappush(dir_sizes, next_dir.calculate_size())

    total_size = max(dir_sizes)
    next_size = heapq.heappop(dir_sizes)
    while total_size - next_size > 40_000_000:
        next_size = heapq.heappop(dir_sizes)
    print(f"Directory size to delete: {next_size}")

data = open(sys.argv[1], "r").read().strip().split("\n")
parse_commands(data)
