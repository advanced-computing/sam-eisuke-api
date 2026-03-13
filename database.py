import duckdb

def connection():
    con = duckdb.connect("file.db")
    con.sql("CREATE TABLE IF NOT EXISTS Cause_of_Death AS SELECT * FROM read_csv_auto('Causes_of_Death_2026.csv')")

    return con

def create_users_table():
    con = connection()

    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
                username VARCHAR,
                age INTEGER,
                country VARCHAR
                )
                """)
    con.close()