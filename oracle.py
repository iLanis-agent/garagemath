#!/usr/bin/env python3
"""Python mirror of engine.js - regenerates expected.json. Exact float-for-float mirror."""
import json, math, os

MIRROR_CM = 25

def r0(x): return math.floor(x + 0.5)
def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100
def jsnum(x):
    if isinstance(x, float) and x == int(x): return int(x)
    return x
def fmt(x): return repr(jsnum(x))
def pos(nums, msg):
    for n in nums:
        if not (n > 0) or n != n or n == float('inf'): return {"error": msg}
    return None

def fitPlan(garageL, garageW, carL, carW):
    bad = pos([garageL, garageW, carL, carW], "garage and car dimensions must be positive")
    if bad: return bad
    side = r0((garageW - carW) / 2)
    end = r0((garageL - carL) / 2)
    return {"sideCm": side, "endCm": end, "fits": side >= 0 and end >= 0}

def doorPlan(doorW, doorH, carW, carH):
    bad = pos([doorW, doorH, carW, carH], "door and car dimensions must be positive")
    if bad: return bad
    wClear = r0(doorW - (carW + MIRROR_CM))
    hClear = r0(doorH - carH)
    return {"wClear": wClear, "hClear": hClear, "clears": wClear >= 0 and hClear >= 0}

def shelfPlan(wallM, depthM, spacingM, heightM):
    bad = pos([wallM, depthM, spacingM, heightM], "wall, depth, spacing and height must be positive")
    if bad: return bad
    if spacingM > heightM: return {"error": "the shelf spacing must not exceed the wall height"}
    levels = math.floor(heightM / spacingM)
    area = r2(levels * wallM * depthM)
    board = r1(levels * wallM)
    volume = r2(levels * wallM * depthM * spacingM)
    return {"levels": levels, "areaM2": jsnum(area), "boardM": jsnum(board), "volumeM3": jsnum(volume)}

def plural(n, w): return str(n) + " " + w + ("" if n == 1 else "s")

def renderFit(r):
    if r["fits"]:
        return "Centered in the garage, the car gets " + str(r["sideCm"]) + " cm on each side and " + str(r["endCm"]) + " cm at each end."
    parts = []
    if r["sideCm"] < 0: parts.append(str(-r["sideCm"] * 2) + " cm too wide")
    if r["endCm"] < 0: parts.append(str(-r["endCm"] * 2) + " cm too long")
    return "The car does not fit: " + " and ".join(parts) + " for that garage."

def renderDoor(r):
    if r["clears"]:
        return "Through the door: " + str(r["wClear"]) + " cm of width to spare counting a labeled " + str(MIRROR_CM) + " cm for open mirrors, and " + str(r["hClear"]) + " cm of height."
    parts = []
    if r["wClear"] < 0: parts.append(str(-r["wClear"]) + " cm of width")
    if r["hClear"] < 0: parts.append(str(-r["hClear"]) + " cm of height")
    return "The car will not clear the door: short " + " and ".join(parts) + ", counting a labeled " + str(MIRROR_CM) + " cm for open mirrors."

def renderShelf(r):
    return plural(r["levels"], "level") + " on that wall: " + fmt(r["areaM2"]) + " m² of shelf, " + fmt(r["boardM"]) + " m of board, and about " + fmt(r["volumeM3"]) + " m³ of storage."

cases = []
fit_args = [(500,300,450,180),(600,350,500,190),(540,300,470,185),(480,280,445,175),
            (520,310,460,182),(700,400,530,200),(500,300,510,180),(500,300,450,310),
            (450,250,445,180),(610,305,490,185),(560,320,470,183),(580,330,505,195)]
for a in fit_args:
    r = fitPlan(*a)
    case = {"fn": "fitPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderFit(r)
    cases.append(case)
door_args = [(240,210,180,160),(250,220,185,155),(230,200,175,158),(260,215,190,162),
             (240,210,205,170),(240,210,180,225),(220,205,195,165),(300,240,200,180),
             (245,215,183,161),(255,218,187,159),(235,208,178,163),(265,225,192,166)]
for a in door_args:
    r = doorPlan(*a)
    case = {"fn": "doorPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderDoor(r)
    cases.append(case)
shelf_args = [(3,0.4,0.35,2.1),(4,0.5,0.4,2.0),(2.5,0.3,0.3,1.8),(3.5,0.45,0.35,2.2),
              (3,0.4,0.5,2.1),(5,0.6,0.4,2.4),(2,0.35,0.25,1.5),(3.2,0.4,0.32,1.92),
              (4.5,0.5,0.45,2.25),(2.8,0.38,0.28,1.68),(3.6,0.42,0.36,2.16),(6,0.5,0.3,2.1),
              (3,0.4,2.5,2.1),(0,0.4,0.35,2.1),(3,0.4,-0.35,2.1),(2,0.3,0.3,1.2)]
for a in shelf_args:
    r = shelfPlan(*a)
    case = {"fn": "shelfPlan", "args": list(a), "result": r}
    if "error" not in r: case["render"] = renderShelf(r)
    cases.append(case)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected.json")
with open(out, "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(cases), "cases")
