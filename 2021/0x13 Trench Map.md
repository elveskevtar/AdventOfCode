## --- Day 20: Trench Map ---

With the scanners fully deployed, you turn their attention to mapping the floor of the ocean trench.

When you get back the image from the scanners, it seems to just be random noise. Perhaps you can combine an image enhancement algorithm and the input image (your puzzle input) to clean it up a little.

For example:

```
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
```

The first section is the _image enhancement algorithm_. It is normally given on a single line, but it has been wrapped to multiple lines in this example for legibility. The second section is the _input image_, a two-dimensional grid of _light pixels_ (`#`) and _dark pixels_ (`.`).

The image enhancement algorithm describes how to enhance an image by _simultaneously_ converting all pixels in the input image into an output image. Each pixel of the output image is determined by looking at a 3x3 square of pixels centered on the corresponding input image pixel. So, to determine the value of the pixel at (5,10) in the output image, nine pixels from the input image need to be considered: (4,9), (4,10), (4,11), (5,9), (5,10), (5,11), (6,9), (6,10), and (6,11). These nine input pixels are combined into a single binary number that is used as an index in the _image enhancement algorithm_ string.

For example, to determine the output pixel that corresponds to the very middle pixel of the input image, the nine pixels marked by `[...]` would need to be considered:

```
# . . # .
#[. . .].
#[# . .]#
.[. # .].
. . # # #
```

Starting from the top-left and reading across each row, these pixels are `...`, then `#..`, then `.#.`; combining these forms `...#...#.`. By turning dark pixels (`.`) into `0` and light pixels (`#`) into `1`, the binary number `000100010` can be formed, which is `34` in decimal.

The image enhancement algorithm string is exactly 512 characters long, enough to match every possible 9-bit binary number. The first few characters of the string (numbered starting from zero) are as follows:

```
0         10        20        30  34    40        50        60        70
|         |         |         |   |     |         |         |         |
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
```

In the middle of this first group of characters, the character at index 34 can be found: `#`. So, the output pixel in the center of the output image should be `#`, a _light pixel_.

This process can then be repeated to calculate every pixel of the output image.

Through advances in imaging technology, the images being operated on here are _infinite_ in size. _Every_ pixel of the infinite output image needs to be calculated exactly based on the relevant pixels of the input image. The small input image you have is only a small region of the actual infinite input image; the rest of the input image consists of dark pixels (`.`). For the purposes of the example, to save on space, only a portion of the infinite-sized input and output images will be shown.

The starting input image, therefore, looks something like this, with more dark pixels (`.`) extending forever in every direction not shown here:

```
...............
...............
...............
...............
...............
.....#..#......
.....#.........
.....##..#.....
.......#.......
.......###.....
...............
...............
...............
...............
...............
```

By applying the image enhancement algorithm to every pixel simultaneously, the following output image can be obtained:

```
...............
...............
...............
...............
.....##.##.....
....#..#.#.....
....##.#..#....
....####..#....
.....#..##.....
......##..#....
.......#.#.....
...............
...............
...............
...............
```

Through further advances in imaging technology, the above output image can also be used as an input image! This allows it to be enhanced _a second time_:

```
...............
...............
...............
..........#....
....#..#.#.....
...#.#...###...
...#...##.#....
...#.....#.#...
....#.#####....
.....#.#####...
......##.##....
.......###.....
...............
...............
...............
```

Truly incredible - now the small details are really starting to come through. After enhancing the original input image twice, `_35_` pixels are lit.

Start with the original input image and apply the image enhancement algorithm twice, being careful to account for the infinite size of the images. _How many pixels are lit in the resulting image?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
enhance = lambda x: 0 if enhancement[x] == "." else 1
enhancement = file_input[0]

default = 0
pixel_map = {}
for y, line in enumerate(file_input[2:]):
    if line == "":
        continue
    for x, char in enumerate(line):
        result = 0 if char == "." else 1
        pixel_map[x,y] = result
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0 or (x+dx,y+dy) in pixel_map:
                    continue
                pixel_map[x+dx,y+dy] = default

for i in range(2):
    new_default = enhance(int(str(default) * 9, 2))
    pixel_map_old = dict(pixel_map)
    for pos, val in pixel_map_old.items():
        x, y = pos
        result = ""
        for dy in range(-1,2):
            for dx in range(-1,2):
                if (x+dx,y+dy) not in pixel_map_old:
                    pixel_map[x+dx,y+dy] = new_default
                    result += str(default)
                    continue
                result += str(pixel_map_old[x+dx,y+dy])
        result = int(result, 2)
        pixel_map[x,y] = enhance(result)
    default = new_default

num_pixels = len(list(filter(lambda x: x == 1, pixel_map.values())))
print("Number Pixel Lit: {}".format(num_pixels))
```

```bash
❯ python3 solution20.py input20
Number Pixel Lit: 5359
```

## --- Part Two ---

You still can't quite make out the details in the image. Maybe you just didn't [enhance](https://en.wikipedia.org/wiki/Kernel_(image_processing)) it enough.

If you enhance the starting input image in the above example a total of _50_ times, `_3351_` pixels are lit in the final output image.

Start again with the original input image and apply the image enhancement algorithm 50 times. _How many pixels are lit in the resulting image?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
enhance = lambda x: 0 if enhancement[x] == "." else 1
enhancement = file_input[0]

default = 0
pixel_map = {}
for y, line in enumerate(file_input[2:]):
    if line == "":
        continue
    for x, char in enumerate(line):
        result = 0 if char == "." else 1
        pixel_map[x,y] = result
        for dx in range(-1,2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0 or (x+dx,y+dy) in pixel_map:
                    continue
                pixel_map[x+dx,y+dy] = default

for i in range(50):
    new_default = enhance(int(str(default) * 9, 2))
    pixel_map_old = dict(pixel_map)
    for pos, val in pixel_map_old.items():
        x, y = pos
        result = ""
        for dy in range(-1,2):
            for dx in range(-1,2):
                if (x+dx,y+dy) not in pixel_map_old:
                    pixel_map[x+dx,y+dy] = new_default
                    result += str(default)
                    continue
                result += str(pixel_map_old[x+dx,y+dy])
        result = int(result, 2)
        pixel_map[x,y] = enhance(result)
    default = new_default

num_pixels = len(list(filter(lambda x: x == 1, pixel_map.values())))
print("Number Pixel Lit: {}".format(num_pixels))
```

```bash
❯ python3 solution20.py input20
Number Pixel Lit: 12333
```