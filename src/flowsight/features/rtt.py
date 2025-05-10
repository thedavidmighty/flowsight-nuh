# src/flowsight/features/ae.py
from flowsight.etl.db import read_from_db
import pandas as pd


NUH_CODE = "RX1"


def backlog_timeseries(provider: str = NUH_CODE) -> pd.DataFrame:
    sql = """
        SELECT month::date AS date,
                incomplete_pathways AS incomplete_pathways,
                provider_name AS provider_name,
                provider_code AS provider_code
        FROM   rtt
        WHERE  provider_code = %(prov)s
        ORDER  BY month
    """
    return read_from_db(sql, {"prov": provider})