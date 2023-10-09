import pandas as pd
import pvlib as pv
from src.data_process import load_one_month_data


def get_clearness_index(ghi, latitude, longitude, times, tz="UTC", altitude=0):
    location = pv.location.Location(
        latitude=latitude, longitude=longitude, altitude=altitude, tz=tz
    )
    solar_position = location.get_solarposition(times)
    clear_sky = location.get_clearsky(times=times)
    kt = ghi / clear_sky["ghi"]
    kt = max(kt, 2)
    return kt


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    RAW_DATAPATH = os.environ.get("RAW_DATAPATH")
    irradiance, metadata = load_one_month_data(RAW_DATAPATH)
    kt = get_clearness_index(
        ghi=irradiance["ghi"],
        latitude=metadata["latitude"],
        longitude=metadata["longitude"],
        times=irradiance.index,
        altitude=metadata["altitude"],
    )
    print(kt)
