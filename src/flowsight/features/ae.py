# src/flowsight/features/ae.py
from flowsight.etl.db import read_from_db
import pandas as pd


# NUH_CODE = "RX1"


def breaches_timeseries() -> pd.DataFrame:
    sql = """
        SELECT month::date AS date,
                breaches    AS breaches,
                non_breaches AS non_breaches
        FROM   ae
        ORDER  BY month
    """
    return read_from_db(sql)
