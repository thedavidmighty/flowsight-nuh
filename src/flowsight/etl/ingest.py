import pandas as pd
import logging
import pathlib
import os
import re

from flowsight.etl.db import write_to_db

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

RAW_DATA_DIR = pathlib.Path("data/raw")
ae_xls = RAW_DATA_DIR/"ae_march2025.xls"


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

    x1 = pd.ExcelFile(ae_xls)
    sheet = next(s for s in x1.sheet_names if "provider" in s.lower())
    raw = x1.parse(sheet)
    # print("DEBUG - first 5 columns:", list(raw.columns)[:5])
    # print("DEBUG - all columns:", list(raw.columns))
    # return

    tidy = (raw.rename(columns=lambda c: re.sub(r"\s+", " ", str(c)).strip())
            .loc[:, ["Code", "Region", "Name", "Total Attendances > 4 hours"]]
            .rename(columns = {"Code": "provider_code",
                               "Region": "provider_region",
                               "Name": "provider_name",
                               "Total Attendances > 4 hours": "breaches"
                               }))
    
    # Cleaning the data
    tidy["breaches"] = to_int(tidy["breaches"])
    tidy["month"] = pd.to_datetime("2025-03-01")


    logging.info("Rows loaded: %d (sheet = '%s')", len(tidy), sheet)
    write_to_db(tidy, "ae")

if __name__ == "__main__":
    main()
