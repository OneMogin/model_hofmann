import pandas as pd
import pvlib as pv
from data_process import load_one_month_data
import numpy as np


def get_clearness_index(ghi, latitude, longitude, times, tz="UTC", altitude=0):
    location = pv.location.Location(
        latitude=latitude, longitude=longitude, altitude=altitude, tz=tz
    )
    clear_sky = location.get_clearsky(times=times)
    kt = ghi / clear_sky["ghi"]
    kt = kt.apply(lambda x: min(x, 2))
    return kt


def get_hourly_kt_average(hourly_series):
    return hourly_series["kt"].sum() / 60.0


def get_daily_kt_average(month_data):
    n_days = int(len(month_data) / (60 * 24))
    daily_avg = []
    month_data["day"] = month_data.index.day
    month_data["hour"] = month_data.index.hour
    for i in range(1, n_days + 1):
        hourly_avg = []
        daily_data = month_data[month_data["day"] == i]
        for j in range(0, 24):
            hourly_avg.append(
                get_hourly_kt_average(daily_data[daily_data["hour"] == j])
            )
        n = sum(abs(x) != 0 and abs(x) != np.inf for x in hourly_avg)
        daily_avg.append(sum([x for x in hourly_avg if not np.isinf(abs(x))]) / n)
    return daily_avg


def get_daily_kt_variability(month_data):
    n_days = int(len(month_data) / (60 * 24))
    daily_var = []
    for i in range(1, n_days + 1):
        hourly_avg = []
        var_sum = []
        daily_data = month_data[month_data["day"] == i]
        for j in range(0, 24):
            hourly_avg.append(
                get_hourly_kt_average(daily_data[daily_data["hour"] == j])
            )
        n = sum(abs(x) != 0 and abs(x) != np.inf for x in hourly_avg)
        for j in range(1, 24):
            var_sum.append(abs(hourly_avg[j] - hourly_avg[j - 1]))
        vli = sum([x for x in var_sum if not np.isinf(abs(x))]) 
        daily_var.append(np.nansum([x for x in var_sum if not np.isinf(abs(x))]) / n)
    return daily_var




