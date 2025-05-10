# src/flowsight/features/ae.py
from flowsight.etl.db import read_from_db
import pandas as pd


NUH_CODE = "RWD"


def breaches_timeseries(provider: str = NUH_CODE) -> pd.DataFrame:
    sql = """
        SELECT month::date AS date,
               breaches    AS breaches
        FROM   ae
        WHERE  provider_code = %(prov)s
        ORDER  BY month
    """
    return read_from_db(sql, {"prov": provider})
