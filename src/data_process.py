import os
import numpy as np
import pandas as pd


def load_one_month_data(dirpath):
    irr_data = []

    stationpath = "abs0123.dat"

    filepath = os.path.join(dirpath, stationpath)

    parsing = False
    parsing_location = False

    try:
        with open(filepath, "r") as f:
            j = 0
            k = 0
            for i, line in enumerate(f):
                if i == 1:
                    date = line.strip().split()[1:3]

                line = line.strip()

                if line.startswith("*U0004") or line.startswith("*C0004"):
                    parsing_location = True
                elif line.startswith("*U0005") or line.startswith("*C0005"):
                    parsing_location = False
                elif parsing_location:
                    j += 1
                    if j == 6:
                        location = line.strip().split()[0:3]
                        parsing_location = False

                if line.startswith("*U0100") or line.startswith("*C0100"):
                    parsing = True
                elif line.startswith("*U1000") or line.startswith("*C1000"):
                    parsing = False
                elif parsing:
                    k += 1
                    if k % 2 != 0:
                        irr_data.append(line)
                    elif k % 2 == 0:
                        irr_data[-1] = [
                            float(num) for num in " ".join([irr_data[-1], line]).split()
                        ]

    except FileNotFoundError as e:
        print(f"An error ocurred while opening file: {e}")
    return date, location, irr_data


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    RAW_DATAPATH = os.environ.get("RAW_DATAPATH")
    date, location, irradiance = load_one_month_data(RAW_DATAPATH)
    print(f"Station Date: Month: {date[0]}, Year: {date[1]}")
