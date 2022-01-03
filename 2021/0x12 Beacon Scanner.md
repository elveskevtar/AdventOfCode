## --- Day 19: Beacon Scanner ---

As your [probe](https://adventofcode.com/2021/day/17) drifted down through this area, it released an assortment of _beacons_ and _scanners_ into the water. It's difficult to navigate in the pitch black open waters of the ocean trench, but if you can build a map of the trench using data from the scanners, you should be able to safely reach the bottom.

The beacons and scanners float motionless in the water; they're designed to maintain the same position for long periods of time. Each scanner is capable of detecting all beacons in a large cube centered on the scanner; beacons that are at most 1000 units away from the scanner in each of the three axes (`x`, `y`, and `z`) have their precise position determined relative to the scanner. However, scanners cannot detect other scanners. The submarine has automatically summarized the relative positions of beacons detected by each scanner (your puzzle input).

For example, if a scanner is at `x,y,z` coordinates `500,0,-500` and there are beacons at `-500,1000,-1500` and `1501,0,-500`, the scanner could report that the first beacon is at `-1000,1000,-1000` (relative to the scanner) but would not detect the second beacon at all.

Unfortunately, while each scanner can report the positions of all detected beacons relative to itself, _the scanners do not know their own position_. You'll need to determine the positions of the beacons and scanners yourself.

The scanners and beacons map a single contiguous 3d region. This region can be reconstructed by finding pairs of scanners that have overlapping detection regions such that there are _at least 12 beacons_ that both scanners detect within the overlap. By establishing 12 common beacons, you can precisely determine where the scanners are relative to each other, allowing you to reconstruct the beacon map one scanner at a time.

For a moment, consider only two dimensions. Suppose you have the following scanner reports:

```
--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1
```

Drawing `x` increasing rightward, `y` increasing upward, scanners as `S`, and beacons as `B`, scanner `0` detects this:

```
...B.
B....
....B
S....
```

Scanner `1` detects this:

```
...B..
B....S
....B.
```

For this example, assume scanners only need 3 overlapping beacons. Then, the beacons visible to both scanners overlap to produce the following complete map:

```
...B..
B....S
....B.
S.....
```

Unfortunately, there's a second problem: the scanners also don't know their _rotation or facing direction_. Due to magnetic alignment, each scanner is rotated some integer number of 90-degree turns around all of the `x`, `y`, and `z` axes. That is, one scanner might call a direction positive `x`, while another scanner might call that direction negative `y`. Or, two scanners might agree on which direction is positive `x`, but one scanner might be upside-down from the perspective of the other scanner. In total, each scanner could be in any of 24 different orientations: facing positive or negative `x`, `y`, or `z`, and considering any of four directions "up" from that facing.

For example, here is an arrangement of beacons as seen from a scanner in the same position but in different orientations:

```
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
```

By finding pairs of scanners that both see at least 12 of the same beacons, you can assemble the entire map. For example, consider the following report:

```
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
```

Because all coordinates are relative, in this example, all "absolute" positions will be expressed relative to scanner `0` (using the orientation of scanner `0` and as if scanner `0` is at coordinates `0,0,0`).

Scanners `0` and `1` have overlapping detection cubes; the 12 beacons they both detect (relative to scanner `0`) are at the following coordinates:

```
-618,-824,-621
-537,-823,-458
-447,-329,318
404,-588,-901
544,-627,-890
528,-643,409
-661,-816,-575
390,-675,-793
423,-701,434
-345,-311,381
459,-707,401
-485,-357,347
```

These same 12 beacons (in the same order) but from the perspective of scanner `1` are:

```
686,422,578
605,423,415
515,917,-361
-336,658,858
-476,619,847
-460,603,-452
729,430,532
-322,571,750
-355,545,-477
413,935,-424
-391,539,-444
553,889,-390
```

Because of this, scanner `1` must be at `68,-1246,-43` (relative to scanner `0`).

Scanner `4` overlaps with scanner `1`; the 12 beacons they both detect (relative to scanner `0`) are:

```
459,-707,401
-739,-1745,668
-485,-357,347
432,-2009,850
528,-643,409
423,-701,434
-345,-311,381
408,-1815,803
534,-1912,768
-687,-1600,576
-447,-329,318
-635,-1737,486
```

So, scanner `4` is at `-20,-1133,1061` (relative to scanner `0`).

Following this process, scanner `2` must be at `1105,-1205,1229` (relative to scanner `0`) and scanner `3` must be at `-92,-2380,-20` (relative to scanner `0`).

The full list of beacons (relative to scanner `0`) is:

```
-892,524,684
-876,649,763
-838,591,734
-789,900,-551
-739,-1745,668
-706,-3180,-659
-697,-3072,-689
-689,845,-530
-687,-1600,576
-661,-816,-575
-654,-3158,-753
-635,-1737,486
-631,-672,1502
-624,-1620,1868
-620,-3212,371
-618,-824,-621
-612,-1695,1788
-601,-1648,-643
-584,868,-557
-537,-823,-458
-532,-1715,1894
-518,-1681,-600
-499,-1607,-770
-485,-357,347
-470,-3283,303
-456,-621,1527
-447,-329,318
-430,-3130,366
-413,-627,1469
-345,-311,381
-36,-1284,1171
-27,-1108,-65
7,-33,-71
12,-2351,-103
26,-1119,1091
346,-2985,342
366,-3059,397
377,-2827,367
390,-675,-793
396,-1931,-563
404,-588,-901
408,-1815,803
423,-701,434
432,-2009,850
443,580,662
455,729,728
456,-540,1869
459,-707,401
465,-695,1988
474,580,667
496,-1584,1900
497,-1838,-617
527,-524,1933
528,-643,409
534,-1912,768
544,-627,-890
553,345,-567
564,392,-477
568,-2007,-577
605,-1665,1952
612,-1593,1893
630,319,-379
686,-3108,-505
776,-3184,-501
846,-3110,-434
1135,-1161,1235
1243,-1093,1063
1660,-552,429
1693,-557,386
1735,-437,1738
1749,-1800,1813
1772,-405,1572
1776,-675,371
1779,-442,1789
1780,-1548,337
1786,-1538,337
1847,-1591,415
1889,-1729,1762
1994,-1805,1792
```

In total, there are `_79_` beacons.

Assemble the full map of beacons. _How many beacons are there?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

rotation_funcs = [
    lambda x,y,z: ( x, y, z),
    lambda x,y,z: ( x, z,-y),
    lambda x,y,z: ( x,-y,-z),
    lambda x,y,z: ( x,-z, y),
    lambda x,y,z: (-x,-y, z),
    lambda x,y,z: (-x, z, y),
    lambda x,y,z: (-x, y,-z),
    lambda x,y,z: (-x,-z,-y),
    lambda x,y,z: ( y,-x, z),
    lambda x,y,z: ( y, z, x),
    lambda x,y,z: ( y, x,-z),
    lambda x,y,z: ( y,-z,-x),
    lambda x,y,z: (-y, x, z),
    lambda x,y,z: (-y, z,-x),
    lambda x,y,z: (-y,-x,-z),
    lambda x,y,z: (-y,-z, x),
    lambda x,y,z: ( z, y,-x),
    lambda x,y,z: ( z,-x,-y),
    lambda x,y,z: ( z,-y, x),
    lambda x,y,z: ( z, x, y),
    lambda x,y,z: (-z, y, x),
    lambda x,y,z: (-z, x,-y),
    lambda x,y,z: (-z,-y,-x),
    lambda x,y,z: (-z,-x, y)
]

scanners = {}
for line in file_input:
    if line == "":
        continue
    if "scanner" in line:
        i = int(line.split()[2])
        scanners[i] = {
            "beacons": set(),
            "position": None
        }
        continue
    x, y, z = tuple(map(lambda x: int(x), line.split(",")))
    scanners[i]["beacons"].add((x,y,z))
scanners[0]["position"] = (0,0,0)

scanner = 0
rotated_set, translated_set = set(), set()
not_located = lambda elem: elem[1]["position"] is None
missing = {k for k,v in list(filter(not_located, scanners.items()))}
while len(missing) > 0:
    found = False
    i = list(missing)[scanner]
    for j in set(scanners.keys()) - missing:
        for func in rotation_funcs:
            rotated_set.clear()
            for coord in scanners[i]["beacons"]:
                rotated_set.add(func(*coord))

            for init_coord in scanners[j]["beacons"]:
                for compare_coord in rotated_set:
                    delta = tuple(compare_coord[i] - init_coord[i] for i in range(3))
                    translated_set.clear()
                    for coord in rotated_set:
                        translated_set.add(tuple(coord[i] - delta[i] for i in range(3)))
                    intersection = translated_set.intersection(scanners[j]["beacons"])
                    if len(intersection) >= 12:
                        delta = tuple(-delta[i] for i in range(3))
                        print("Scanner {} position discovered: {}".format(i, delta))
                        scanners[i]["position"] = delta
                        scanners[i]["beacons"] = set(translated_set)
                        missing.remove(i)
                        found = True
                    if found: break
                if found: break
            if found: break
        if found: break
    scanner = 0 if found else (scanner + 1) % len(missing)

beacons = set()
for vals in scanners.values():
    beacons |= vals["beacons"]

print("Number of unique beacons: {}".format(len(beacons)))
```

```bash
❯ python3 solution19.py input19
Scanner 38 position discovered: (147, 155, -1150)
Scanner 15 position discovered: (-1111, -15, -1172)
Scanner 17 position discovered: (84, -12, -2408)
Scanner 4 position discovered: (152, 57, -3678)
Scanner 10 position discovered: (140, 1336, -2439)
Scanner 6 position discovered: (73, 2415, -2429)
Scanner 29 position discovered: (130, 2535, -3661)
Scanner 8 position discovered: (-1166, 2471, -3551)
Scanner 23 position discovered: (-7, 2465, -4812)
Scanner 28 position discovered: (61, 1318, -4788)
Scanner 3 position discovered: (-1230, 1218, -4909)
Scanner 21 position discovered: (1189, 1325, -4821)
Scanner 25 position discovered: (1176, 1237, -5981)
Scanner 30 position discovered: (1182, 2551, -6086)
Scanner 31 position discovered: (-1172, 1211, -2375)
Scanner 2 position discovered: (-2296, 1210, -2351)
Scanner 33 position discovered: (91, 1367, -3627)
Scanner 35 position discovered: (-1069, 1334, -1335)
Scanner 5 position discovered: (-1125, 2470, -1239)
Scanner 18 position discovered: (-2300, 2420, -1172)
Scanner 26 position discovered: (-1061, 3690, -1300)
Scanner 7 position discovered: (-1041, 3750, -2376)
Scanner 16 position discovered: (-1168, 4811, -2507)
Scanner 34 position discovered: (37, 3619, -1177)
Scanner 14 position discovered: (86, 4852, -1290)
Scanner 12 position discovered: (10, 4959, 1)
Scanner 19 position discovered: (51, 6081, -1202)
Scanner 24 position discovered: (139, 7342, -1144)
Scanner 27 position discovered: (-1201, 6159, -1249)
Scanner 32 position discovered: (4, 6024, -123)
Scanner 36 position discovered: (25, -1081, -3562)
Scanner 22 position discovered: (40, -2227, -3679)
Scanner 1 position discovered: (39, -3432, -3735)
Scanner 13 position discovered: (-1133, -2226, -3620)
Scanner 9 position discovered: (-2428, -2405, -3634)
Scanner 20 position discovered: (43, -2315, -2539)
Scanner 37 position discovered: (30, 2407, -5973)
Scanner 39 position discovered: (-1091, 4964, -52)
Scanner 11 position discovered: (-2393, 4828, -81)
Number of unique beacons: 483
```

## --- Part Two ---

Sometimes, it's a good idea to appreciate just how big the ocean is. Using the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry), how far apart do the scanners get?

In the above example, scanners `2` (`1105,-1205,1229`) and `3` (`-92,-2380,-20`) are the largest Manhattan distance apart. In total, they are `1197 + 1175 + 1249 = _3621_` units apart.

_What is the largest Manhattan distance between any two scanners?_

```python
#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

rotation_funcs = [
    lambda x,y,z: ( x, y, z),
    lambda x,y,z: ( x, z,-y),
    lambda x,y,z: ( x,-y,-z),
    lambda x,y,z: ( x,-z, y),
    lambda x,y,z: (-x,-y, z),
    lambda x,y,z: (-x, z, y),
    lambda x,y,z: (-x, y,-z),
    lambda x,y,z: (-x,-z,-y),
    lambda x,y,z: ( y,-x, z),
    lambda x,y,z: ( y, z, x),
    lambda x,y,z: ( y, x,-z),
    lambda x,y,z: ( y,-z,-x),
    lambda x,y,z: (-y, x, z),
    lambda x,y,z: (-y, z,-x),
    lambda x,y,z: (-y,-x,-z),
    lambda x,y,z: (-y,-z, x),
    lambda x,y,z: ( z, y,-x),
    lambda x,y,z: ( z,-x,-y),
    lambda x,y,z: ( z,-y, x),
    lambda x,y,z: ( z, x, y),
    lambda x,y,z: (-z, y, x),
    lambda x,y,z: (-z, x,-y),
    lambda x,y,z: (-z,-y,-x),
    lambda x,y,z: (-z,-x, y)
]

scanners = {}
for line in file_input:
    if line == "":
        continue
    if "scanner" in line:
        i = int(line.split()[2])
        scanners[i] = {
            "beacons": set(),
            "position": None
        }
        continue
    x, y, z = tuple(map(lambda x: int(x), line.split(",")))
    scanners[i]["beacons"].add((x,y,z))
scanners[0]["position"] = (0,0,0)

scanner = 0
rotated_set, translated_set = set(), set()
not_located = lambda elem: elem[1]["position"] is None
missing = {k for k,v in list(filter(not_located, scanners.items()))}
while len(missing) > 0:
    found = False
    i = list(missing)[scanner]
    for j in set(scanners.keys()) - missing:
        for func in rotation_funcs:
            rotated_set.clear()
            for coord in scanners[i]["beacons"]:
                rotated_set.add(func(*coord))

            for init_coord in scanners[j]["beacons"]:
                for compare_coord in rotated_set:
                    delta = tuple(compare_coord[i] - init_coord[i] for i in range(3))
                    translated_set.clear()
                    for coord in rotated_set:
                        translated_set.add(tuple(coord[i] - delta[i] for i in range(3)))
                    intersection = translated_set.intersection(scanners[j]["beacons"])
                    if len(intersection) >= 12:
                        delta = tuple(-delta[i] for i in range(3))
                        print("Scanner {} position discovered: {}".format(i, delta))
                        scanners[i]["position"] = delta
                        scanners[i]["beacons"] = set(translated_set)
                        missing.remove(i)
                        found = True
                    if found: break
                if found: break
            if found: break
        if found: break
    scanner = 0 if found else (scanner + 1) % len(missing)

max_dist = 0
beacons = set()
for vals1 in scanners.values():
    beacons |= vals1["beacons"]
    for vals2 in scanners.values():
        if vals1 == vals2:
            continue
        pos1, pos2 = vals1["position"], vals2["position"]
        max_dist = max(max_dist, sum([abs(pos1[i]-pos2[i]) for i in range(3)]))

print("Number of unique beacons: {}".format(len(beacons)))
print("Maximum manhattan distance: {}".format(max_dist))
```

```bash
❯ python3 solution19.py input19
Scanner 38 position discovered: (147, 155, -1150)
Scanner 15 position discovered: (-1111, -15, -1172)
Scanner 17 position discovered: (84, -12, -2408)
Scanner 4 position discovered: (152, 57, -3678)
Scanner 10 position discovered: (140, 1336, -2439)
Scanner 6 position discovered: (73, 2415, -2429)
Scanner 29 position discovered: (130, 2535, -3661)
Scanner 8 position discovered: (-1166, 2471, -3551)
Scanner 23 position discovered: (-7, 2465, -4812)
Scanner 28 position discovered: (61, 1318, -4788)
Scanner 3 position discovered: (-1230, 1218, -4909)
Scanner 21 position discovered: (1189, 1325, -4821)
Scanner 25 position discovered: (1176, 1237, -5981)
Scanner 30 position discovered: (1182, 2551, -6086)
Scanner 31 position discovered: (-1172, 1211, -2375)
Scanner 2 position discovered: (-2296, 1210, -2351)
Scanner 33 position discovered: (91, 1367, -3627)
Scanner 35 position discovered: (-1069, 1334, -1335)
Scanner 5 position discovered: (-1125, 2470, -1239)
Scanner 18 position discovered: (-2300, 2420, -1172)
Scanner 26 position discovered: (-1061, 3690, -1300)
Scanner 7 position discovered: (-1041, 3750, -2376)
Scanner 16 position discovered: (-1168, 4811, -2507)
Scanner 34 position discovered: (37, 3619, -1177)
Scanner 14 position discovered: (86, 4852, -1290)
Scanner 12 position discovered: (10, 4959, 1)
Scanner 19 position discovered: (51, 6081, -1202)
Scanner 24 position discovered: (139, 7342, -1144)
Scanner 27 position discovered: (-1201, 6159, -1249)
Scanner 32 position discovered: (4, 6024, -123)
Scanner 36 position discovered: (25, -1081, -3562)
Scanner 22 position discovered: (40, -2227, -3679)
Scanner 1 position discovered: (39, -3432, -3735)
Scanner 13 position discovered: (-1133, -2226, -3620)
Scanner 9 position discovered: (-2428, -2405, -3634)
Scanner 20 position discovered: (43, -2315, -2539)
Scanner 37 position discovered: (30, 2407, -5973)
Scanner 39 position discovered: (-1091, 4964, -52)
Scanner 11 position discovered: (-2393, 4828, -81)
Number of unique beacons: 483
Maximum manhattan distance: 14804
```