import os
import numpy as np


def load_one_month_data(self):
    lines = []
    

    stationpath = "abs0123.dat"

    filepath = os.path.join(self.dirpath, stationpath)

    parsing = False
    location_line = False

    try:
        with open(filepath, "r") as f:
            for i, line in enumerate(f):
                if i == 1:
                    month, year = line.strip().split()[1], line.strip().split()[2]

                line = line.strip()

                j = 0
                if line.startswith("*U0004") or line.startswith("*C0004"):
                    parsing = True
                elif line.startswith("*U0005") or line.startswith("*C000"):
                    parsing == False
                if parsing:
                    j += 1
                    if j == 6:
                       info = line.strip().split()
                       location = [info[0], info[1], info[2]] 

                if line.startswith("*U0100") or line.startswith("*C0100"):
                    parsing = True
                elif line.startswith("*U1100") or line.startswith("*C1100"):
                    parsing == False
                if parsing:
                    lines.append(line)

    except FileNotFoundError as e:
        print(f"An error ocurred while opening file: {e}")

    conc_lines = []
    for i in range(len(lines) - 1):
        if i % 2 == 0:
            conc_line = " ".join([lines[i], lines[i + 1]])
            conc_lines.append(conc_line)

    df = pd.DataFrame([line.split() for line in conc_lines])
    return location, df
