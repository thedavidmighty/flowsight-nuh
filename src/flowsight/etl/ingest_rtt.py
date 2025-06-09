import pandas as pd
import logging
import pathlib
import re


from flowsight.etl.db import write_to_db



logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

RAW_DATA_DIR=pathlib.Path("data/raw")
rtt_xls=RAW_DATA_DIR/"rtt_latest.xls"




def to_int(series):
    """Remove commas, and convert to integer"""

    cleaned = (series.astype(str)                 # force string
                     .str.replace(",", "", regex=False)
                     .str.strip()
                     .replace({"-": "0", "": "0"}))

    # drop any trailing .0
    cleaned = cleaned.str.replace(r"\.0$", "", regex=True)

    # convert safely to numeric then int
    return pd.to_numeric(cleaned, errors="coerce").fillna(0).astype(int)

def main():
    """
    Maihn function to read the excel file and write it to the database"""

    x1 = pd.ExcelFile(rtt_xls)
    sheet = next(s for s in x1.sheet_names if "provider" in s.lower())
    raw = x1.parse(sheet)
    # print("DEBUG - first 5 columns:", list(raw.columns)[:5])
    # print("DEBUG - all columns:", list(raw.columns))
    # return

    tidy=(raw.rename(columns=lambda c: re.sub(r"\s+", " ", str(c)).strip())
            .loc[:, ['month', 'median wait', 'no. < 18 weeks', 'no. > 18 weeks',
                     'no. > 52 weeks', 'no. > 65 weeks', 'no. > 78 weeks', 
                     'no. > 104 weeks', 'total waiting (mil)'
                     ]]
                     .rename(columns = {"month": "month",
                               "median wait": "average_waiting_time",
                               "no. < 18 weeks": "within_18_weeks",
                               "no. > 18 weeks": "beyond_18_weeks",
                               "no. > 52 weeks": "52_plus_weeks",
                               "no. > 65 weeks": "65_plus_weeks",
                               "no. > 78 weeks": "78_plus_weeks",
                               "no. > 104 weeks": "104_plus_weeks",
                               "total waiting (mil)": "incomplete_pathways"
                               }))
    
    # Cleaning the data
    tidy["incomplete_pathways"]=to_int(tidy["incomplete_pathways"])
    tidy["month"]=pd.to_datetime(tidy["month"], format="%m/%Y", errors="coerce")


    logging.info("RTT rows loaded: %d  (sheet = '%s')", len(tidy), sheet)
    write_to_db(tidy, "rtt")

if __name__ == "__main__":
    main()
