# src/flowsight/features/ae.py
from flowsight.etl.db import read_from_db
import pandas as pd




def backlog_timeseries() -> pd.DataFrame:
    sql = """
        SELECT month::date AS date,
                incomplete_pathways AS incomplete_pathways,
                within_18_weeks AS within_18_weeks,
                beyond_18_weeks AS beyond_18_weeks
        FROM   rtt
        ORDER  BY month
    """
    return read_from_db(sql)