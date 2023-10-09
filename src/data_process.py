import os
import numpy as np
import pandas as pd
from timezonefinder import TimezoneFinder


def load_one_month_data(dirpath):
    irr_data = []
    date = None
    location = None
    metadata = {}

    stationpath = "abs0122.dat"
    filepath = os.path.join(dirpath, stationpath)

    parsing = False
    parsing_location = False
    data_columns = [
        "day",
        "minute",
        "ghi",
        "ghi_sd",
        "ghi_min",
        "ghi_max",
        "dni",
        "dni_sd",
        "dni_min",
        "dni_max",
        "dhi",
        "dhi_sd",
        "dhi_min",
        "dhi_max",
        "lwd",
        "lwd_sd",
        "lwd_min",
        "lwd_max",
        "temp_air",
        "relative_humidity",
        "pressure",
    ]
    try:
        with open(filepath, "r") as f:
            j = 0
            k = 0
            for i, line in enumerate(f):
                if i == 1:
                    date = line.strip().split()[1:3]
                    start_date = pd.Timestamp(
                        year=int(date[1]), month=int(date[0]), day=1, tz="UTC"
                    )
                    metadata["start_date"] = start_date

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
                        metadata["latitude"] = float(location[0]) - 90.0  # ISO 19115
                        metadata["longitude"] = float(location[1]) - 180.0
                        metadata["altitude"] = int(location[2])

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
                            num for num in " ".join([irr_data[-1], line]).split()
                        ]
            irr_data = pd.DataFrame(irr_data)
            irr_data = irr_data.replace(to_replace=["-999", "-99.9"], value=np.nan).astype(float)
            irr_data.columns = data_columns
            irr_data.index = (
                start_date
                + pd.to_timedelta(irr_data["day"] - 1, unit="day")
                + pd.to_timedelta(irr_data["minute"], unit="m")
            )
            tf = TimezoneFinder()
            tz = tf.timezone_at(lng=metadata['longitude'], lat=metadata['latitude']) 
            irr_data['local time'] = irr_data.index.tz_convert(tz)
            irr_data = irr_data.drop(["day", "minute"], axis=1)
    except FileNotFoundError as e:
        print(f"An error ocurred while opening file: {e}")
    return irr_data, metadata


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    RAW_DATAPATH = os.environ.get("RAW_DATAPATH")
    irradiance, metadata = load_one_month_data(RAW_DATAPATH)
    print(irradiance['local time'])
