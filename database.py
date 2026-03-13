import duckdb

def connection():
    con = duckdb.connect("file.db")
    con.sql("SELECT * FROM read_csv_auto('sam-eisuke-api/Causes_of_Death_2026.csv')").df()

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