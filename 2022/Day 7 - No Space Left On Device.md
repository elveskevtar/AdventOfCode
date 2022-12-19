You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

```
$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
```

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

```
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
```

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called `/`. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with `$` are _commands you executed_, very much like some modern computers:

-   `cd` means _change directory_. This changes which directory is the current directory, but the specific result depends on the argument:
    -   `cd x` moves _in_ one level: it looks in the current directory for the directory named `x` and makes it the current directory.
    -   `cd ..` moves _out_ one level: it finds the directory that contains the current directory, then makes that directory the current directory.
    -   `cd /` switches the current directory to the outermost directory, `/`.
-   `ls` means _list_. It prints out all of the files and directories immediately contained by the current directory:
    -   `123 abc` means that the current directory contains a file named `abc` with size `123`.
    -   `dir xyz` means that the current directory contains a directory named `xyz`.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

```
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
```

Here, there are four directories: `/` (the outermost directory), `a` and `d` (which are in `/`), and `e` (which is in `a`). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the _total size_ of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

-   The total size of directory `e` is _584_ because it contains a single file `i` of size 584 and no other directories.
-   The directory `a` has total size _94853_ because it contains files `f` (size 29116), `g` (size 2557), and `h.lst` (size 62596), plus file `i` indirectly (`a` contains `e` which contains `i`).
-   Directory `d` has total size _24933642_.
-   As the outermost directory, `/` contains every file. Its total size is _48381165_, the sum of the size of every file.

To begin, find all of the directories with a total size of _at most 100000_, then calculate the sum of their total sizes. In the example above, these directories are `a` and `e`; the sum of their total sizes is `_95437_` (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. _What is the sum of the total sizes of those directories?_

```python
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

    next_size, total_size = heapq.heappop(dir_sizes), 0
    while next_size <= 100000:
        total_size += next_size
        next_size = heapq.heappop(dir_sizes)
    print(f"Total sizes of small dirs: {total_size}")

data = open(sys.argv[1], "r").read().strip().split("\n")
parse_commands(data)
```

```bash
❯ python3 solution7.py input7
Total sizes of small dirs: 1555642
```

## --- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is `_70000000_`. To run the update, you need unused space of at least `_30000000_`. You need to find a directory you can delete that will _free up enough space_ to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is `48381165`; this means that the size of the _unused_ space must currently be `21618835`, which isn't quite the `30000000` required by the update. Therefore, the update still requires a directory with total size of at least `8381165` to be deleted before it can run.

To achieve this, you have the following options:

-   Delete directory `e`, which would increase unused space by `584`.
-   Delete directory `a`, which would increase unused space by `94853`.
-   Delete directory `d`, which would increase unused space by `24933642`.
-   Delete directory `/`, which would increase unused space by `48381165`.

Directories `e` and `a` are both too small; deleting them would not free up enough space. However, directories `d` and `/` are both big enough! Between these, choose the _smallest_: `d`, increasing unused space by `_24933642_`.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. _What is the total size of that directory?_

```python
    total_size = max(dir_sizes)
    next_size = heapq.heappop(dir_sizes)
    while total_size - next_size > 40_000_000:
        print(f"{total_size - next_size} {next_size}")
        next_size = heapq.heappop(dir_sizes)
    print(f"Directory size to delete: {next_size}")
```

```bash
❯ python3 solution7.py input7
Directory size to delete: 5974547
```