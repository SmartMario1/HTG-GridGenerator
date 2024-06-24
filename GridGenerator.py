import numpy as np
import random
import sys
import argparse

# for now assume the grid is square
GRIDSIZE = 2
ROUNDTRIP = True
# If not random, movable starts at (0,0) (topleft)
RANDOMSTART = False
# For remembering the movable start if randomstart and roundtrip
LOC = []

AMOUNT_OBJECTIVES = 1
OBJECTIVE_LOCS = []

file = None
out_str = ""

def gen_objects():
    global out_str
    out_str += "(:objects\n"
    out_str += "\tmov - movable\n"

    out_str += "\t"
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            out_str += f"x{i}y{j} "
    out_str += "- node\n"

    out_str += "\t"
    for i in range(AMOUNT_OBJECTIVES):
        out_str += f"obj{i} "
    out_str +=  "- objective\n"

    out_str += ")\n\n"

def gen_init():
    global out_str

    out_str += "(:init\n"

    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            if i != 0:
                out_str += f"\t(connected x{i}y{j} x{i - 1}y{j})\n"
                out_str += f"\t(connected x{i - 1}y{j} x{i}y{j})\n"
            if j != 0:
                out_str += f"\t(connected x{i}y{j - 1} x{i}y{j})\n"
                out_str += f"\t(connected x{i}y{j} x{i}y{j - 1})\n"

    for i in range(AMOUNT_OBJECTIVES):
        loc = (random.randint(0, GRIDSIZE - 1), random.randint(0, GRIDSIZE - 1))
        j = 0
        while loc in LOC:
            loc = (random.randint(0, GRIDSIZE - 1), random.randint(0, GRIDSIZE - 1))
            j += 1
            if j > 500:
                print("ERROR GENERATING LOCATION, perhaps too many objectives?")
                exit(1)
        LOC.append(loc)
        out_str += f"\t(at-objective obj{i} x{loc[0]}y{loc[1]})\n"

    if (not RANDOMSTART):
        out_str += "\t(at-movable mov x0y0)\n"

    out_str += ")\n\n"

def gen_goals():
    global out_str

    out_str += "(:goal (and\n"
    for i in range(AMOUNT_OBJECTIVES):
        out_str += f"\t(collected obj{i})\n"
    if (ROUNDTRIP):
        if (not RANDOMSTART):
            out_str += f"\t(at-movable mov x0y0)\n"
    out_str += "))\n\n"


def generate_file(out_loc = ""):
    global out_str
    global AMOUNT_OBJECTIVES
    global GRIDSIZE

    if AMOUNT_OBJECTIVES > GRIDSIZE**2:
        AMOUNT_OBJECTIVES = GRIDSIZE**2

    out_str += "(define (problem GENgrid) (:domain htg-grid)\n"
    gen_objects()
    gen_init()
    gen_goals()
    out_str += ")\n"
    if out_loc:
        file = open(out_loc, 'w')
        file.write(out_str)
        file.close()
    else:
        print(out_str)

def reset():
    global OBJECTIVE_LOCS
    global LOC
    global out_str
    OBJECTIVE_LOCS = []
    LOC = []
    out_str = ""


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--destination', help="Path where you want to save generated problem", dest='d')
    parser.add_argument('-g', '--grid', help="Specify the grid size", dest='grid', required=True)
    parser.add_argument('-o', '--objectives', help="Specify the amount of objectives", dest='obj', required=True)
    parser.add_argument('-r', '--random_seed', help="Specify the random seed used to generate objective locations", dest='seed')
    options = parser.parse_args()

    if (options.seed):
        random.seed(int(options.seed))

    AMOUNT_OBJECTIVES = int(options.obj)
    GRIDSIZE = int(options.grid)

    if (options.d):
        generate_file(out_loc=options.d)
    else:
        generate_file()