import pandas as pd
import pvlib as pv
from data_process import load_one_month_data
import numpy as np
from irradiance import get_clearness_index, get_daily_kt_variability, get_daily_kt_average

def get_day_classification(kt_series):
    pass

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    RAW_DATAPATH = os.environ.get("RAW_DATAPATH")
    irradiance, metadata = load_one_month_data(RAW_DATAPATH)
    irradiance["kt"] = get_clearness_index(
        irradiance["ghi"],
        latitude=metadata["latitude"],
        longitude=metadata["longitude"],
        times=irradiance.index,
        altitude=metadata["altitude"],
    )
    daily_avg_kt = get_daily_kt_average(irradiance)
    daily_var_kt = get_daily_kt_variability(irradiance)