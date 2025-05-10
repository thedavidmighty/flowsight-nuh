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
            .loc[:, ['Region Code', 'Provider Code', 'Provider Name', 'Treatment Function',
                     'Total number of incomplete pathways', 'Total within 18 weeks', '% within 18 weeks', 
                     'Average (median) waiting time (in weeks)', '92nd percentile waiting time (in weeks)', 
                     'Total 52 plus weeks', 'Total 78 plus weeks', 'Total 65 plus weeks'
                     ]]
                     .rename(columns = {"Provider Code": "provider_code",
                               "Region": "provider_region",
                               "Region Code": "region_code",
                               "Provider Name": "provider_name",
                               "Treatment Function": "treatment_function",
                               "Total number of incomplete pathways": "incomplete_pathways",
                               "Total within 18 weeks": "within_18_weeks",
                               "% within 18 weeks": "within_18_weeks_percent",
                               "Average (median) waiting time (in weeks)": "average_waiting_time",
                               "92nd percentile waiting time (in weeks)": "percentile_waiting_time",
                               "Total 52 plus weeks": "52_plus_weeks",
                               "Total 78 plus weeks": "78_plus_weeks",
                               "Total 65 plus weeks": "65_plus_weeks",
                               }))
    
    # Cleaning the data
    tidy["incomplete_pathways"]=to_int(tidy["incomplete_pathways"])
    tidy["month"]=pd.to_datetime("2025-03-01")


    logging.info("RTT rows loaded: %d  (sheet = '%s')", len(tidy), sheet)
    write_to_db(tidy, "rtt")

if __name__ == "__main__":
    main()
