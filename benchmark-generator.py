import numpy as np
import GridGenerator as gg
import os

OUT_DIR = "./benchmark/"

SIZE_START = 3
SIZE_STEP = 2
SIZE_END = 20

GOAL_START = 6
GOAL_STEP = 2
GOAL_END = 11

try:
    os.mkdir(OUT_DIR)
except FileExistsError:
    print("Directory already exists.")
    for file in os.listdir(OUT_DIR):
        os.remove(f"{OUT_DIR}{file}")

for gridsize in range(SIZE_START, SIZE_END, SIZE_STEP):
    gg.GRIDSIZE = gridsize
    for goals in range(GOAL_START, GOAL_END, GOAL_STEP):
        gg.AMOUNT_OBJECTIVES = goals
        gg.generate_file(out_loc=f"{OUT_DIR}p-{gridsize}-{goals}.pddl")
        gg.reset()