from sqlalchemy import create_engine
import pandas as pd
import os
PG_URI = os.getenv("PG_URI",
                   "postgresql+psycopg2://flowsight:flowsight@localhost:5432/nuh_staging")

ENGINE = create_engine(PG_URI, future=True)

def write_to_db(df, table_name):
    """
    write a dataframe to a database table using sqlalchemy
    """
    df.to_sql(table_name, ENGINE, if_exists="replace", index=False, method="multi")

def read_from_db(sql, params = None):
    """
    read a table from the datebase using sqlalchemy"""
    return pd.read_sql(sql, ENGINE, params= params or {})
