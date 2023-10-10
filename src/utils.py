import gzip
import os
import shutil
import numpy as np


def unzip_file(input_file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.splitext(os.path.basename(input_file_path))[0]

    output_file_path = os.path.join(output_dir, output_filename)

    if os.path.exists(output_file_path):
        print(f"{output_file_path} already exists, skipping the unzip this file")
        return output_file_path

    with gzip.open(input_file_path, "rb") as f_in:
        with open(output_file_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    return output_file_path
