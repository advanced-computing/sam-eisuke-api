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


# trunc
def trunc_and_load(con, data):
    # we simply truncate the table and load the new data
    con.sql("CREATE OR REPLACE TABLE cpi_trunc AS SELECT * FROM data")


with duckdb.connect(file) as con:
    trunc_and_load(con, df_new)
    print(con.sql("SELECT * FROM cpi_trunc"))


# incremental
def incremental_load(con, data):
    # deleting "outdated" rows
    new_earliest_date = data["DATE"].min()
    con.sql(f"DELETE FROM cpi_inc WHERE DATE < '{new_earliest_date}'")

    # removing rows that will be updated
    date = con.sql("SELECT * FROM cpi_inc").fetchdf()
    # merging new data to compare last_update
    data["CPI"] = data["CPI"].astype(float)
    date["CPI"] = date["CPI"].astype(float)
    date = date.merge(data[["DATE", "CPI"]], on="DATE", suffixes=("_old", "_new"))
    # finding ids for which the dates are different
    months_to_remove = date[date["CPI_old"] != date["CPI_new"]]
    # removing rows and
    for _, row in months_to_remove.iterrows():
        con.sql(f"DELETE FROM cpi_inc WHERE DATE = '{row['DATE']}'")
        con.sql(f"INSERT INTO cpi_inc VALUES ('{row['DATE']}', '{row['CPI_new']}')")

    # appending the new data
    most_recent_date = con.sql("SELECT MAX(DATE) FROM cpi_inc").fetchone()[0]
    data = data[data["DATE"] > most_recent_date]
    for _, row in data.iterrows():
        con.sql(f"INSERT INTO cpi_inc VALUES ('{row['DATE']}', '{row['CPI']}')")


with duckdb.connect(file) as con:
    con.sql(
        "BEGIN TRANSACTION"
    )  # starting a transaction -- changes are synced once = improves performance
    incremental_load(con, df_new)
    con.sql("COMMIT")  # committing the transaction
    print(con.sql("SELECT * FROM cpi_inc"))
