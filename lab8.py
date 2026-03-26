import duckdb
import pandas as pd

# creating three duckdb databases

file = "data.db"
con = duckdb.connect(file)

df_original_1 = con.sql(
    "CREATE OR REPLACE TABLE cpi_append AS SELECT * FROM read_csv('data\PCPI24M1.csv')"
)

df_original_2 = con.sql(
    "CREATE OR REPLACE TABLE cpi_trunc AS SELECT * FROM read_csv('data\PCPI24M1.csv')"
)

df_original_3 = con.sql(
    "CREATE OR REPLACE TABLE cpi_inc AS SELECT * FROM read_csv('data\PCPI24M1.csv')"
)

# load new data
df_new = pd.read_csv("data\PCPI25M2.csv")


# append
def append_load(con, data):
    # getting max date
    max_id = con.sql("SELECT MAX(DATE) FROM cpi_append").fetchone()[0]
    # selecting the new data
    data = data[data["DATE"] > max_id]
    # appending the new data
    for _, row in data.iterrows():
        con.sql(f"INSERT INTO cpi_append VALUES ('{row['DATE']}', '{row['CPI']}')")


with duckdb.connect(file) as con:
    con.sql(
        "BEGIN TRANSACTION"
    )  # starting a transaction -- changes are synced once = improves performance
    append_load(con, df_new)
    con.sql("COMMIT")  # committing the transaction
    print(con.sql("SELECT * FROM cpi_append"))
