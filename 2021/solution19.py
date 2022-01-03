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

