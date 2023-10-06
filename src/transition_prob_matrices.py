import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
RAW_DATAPATH = os.environ.get("RAW_DATAPATH")


class TransitionProbabilityMatices:
    def __init__(self, dirpath, n_months, clear_sky_model="noon_gaussian"):
        self.clear_sky_model = clear_sky_model
        self.dirpath = dirpath
        self.n_months = n_months

    def get_TPM(self):
        lines = []
        

        stationpath = 'abs0123.dat'

        filepath = os.path.join(self.dirpath, stationpath)

        ghi_lines = False
        location_line = False

        with open(filepath, "r") as f:
            for i, line in enumerate(f):
                if i==1:
                    month, year = line.strip().split()[1], line.strip().split()[2]  

                line = line.strip()
                if line.startswith("*U0100") or line.startswith("*C0100"):
                    ghi_lines = True
                elif line.startswith("*U1100") or line.startswith("*C1100"):
                    ghi_lines == False
                elif ghi_lines:
                    lines.append(line)
                
        conc_lines = []
        for i in range(len(lines) - 1):
            if i % 2 == 0:
                conc_line = " ".join([lines[i], lines[i + 1]])
                conc_lines.append(conc_line)

        df = pd.DataFrame([line.split() for line in conc_lines])
        return df


if __name__ == "__main__":
    TPM = TransitionProbabilityMatices(os.path.join(RAW_DATAPATH, "new0719.dat"))
    df = TPM.load_ghi_data()
    print(df.head())
