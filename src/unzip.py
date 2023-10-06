import os
from dotenv import load_dotenv
import gzip
import utils as utils
import random
import logging


class GzFileExtract:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_station_list_path(self, input_dir=None):
        if input_dir == None:
            input_dir = self.input_dir

        stations = [
            files
            for files in os.listdir(input_dir)
            if not os.path.isfile(os.path.join(input_dir, files))
        ]

        return stations

    def unzip_station(self, station, input_dir=None):
        if input_dir == None:
            input_dir = self.input_dir

        stationpath = os.path.join(input_dir, station)

        datafiles = [
            os.path.join(stationpath, files)
            for files in os.listdir(stationpath)
            if os.path.isfile(os.path.join(stationpath, files))
        ]

        try:
            for file in datafiles:
                unzip_path = utils.unzip_file(file, self.output_dir)
        except Exception as e:
            print(f"An error ocurred unzipping file -- {file} -- : {e}")

    def unzip_N_files_per_station(self, station, N=10, input_dir=None):
        if input_dir == None:
            input_dir = self.input_dir

        stationpath = os.path.join(input_dir, station)

        random_files = [
            files
            for files in os.listdir(stationpath)
            if os.path.isfile(os.path.join(stationpath, files))
        ]

        Nfiles = min(len(random_files), N)

        random.seed(10)

        random_files = random.sample(random_files, Nfiles)

        datafiles = [
            os.path.join(stationpath, files)
            for files in random_files
            if os.path.isfile(os.path.join(stationpath, files))
        ]

        try:
            for file in datafiles:
                unzip_path = utils.unzip_file(file, self.output_dir)
        except Exception as e:
            print(f"An error ocurred unzipping file -- {file} -- : {e}")

        print(f"{Nfiles} files from station {station} unzipped")


if __name__ == "__main__":
    load_dotenv()
    EXT_DATAPATH = os.environ.get("EXT_DATAPATH")
    RAW_DATAPATH = os.environ.get("RAW_DATAPATH")
    extract = GzFileExtract(EXT_DATAPATH, RAW_DATAPATH)
    stations = extract.get_station_list_path()
    for station in stations:
        extract.unzip_N_files_per_station(station=station, N=5)
