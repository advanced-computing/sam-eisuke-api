from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
from database import connection 
from database import create_users_table
import duckdb
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>This is lab 4. Hello!</p>"


@app.get("/api/list")
def list():

    # Get the query parameters
    format = request.args.get("format", "json")
    filterby = request.args.get("filterby", None)
    filtervalue = request.args.get("filtervalue", None)
    limit = int(request.args.get("limit", 1000)) # limit
    offset = int(request.args.get("offset", 0)) # offset

    # Load the data
    con = duckdb.connect("file.db")
    data = con.sql("SELECT * FROM Cause_of_Death").df()

    # filter the data
    data = filter_by_value(data, filterby, filtervalue)
    if isinstance(data, str):
        return data

    # applying the limit and offset
    data = apply_limit_offset(data, limit, offset)

    # convert the data to the requested format
    data = convert_to_format(data, format)

    return data


def filter_by_value(data, filterby, filtervalue):

    if filterby:
        if filtervalue is None:
            return "Invalid filtervalue"
        elif filterby not in data.columns:
            return "Invalid filterby column"
        else:
            data = data[data[filterby] == int(filtervalue)]
    return data


def apply_limit_offset(data, limit, offset):
    return data.iloc[offset : offset + limit]


def convert_to_format(data, format):
    if format == "json":
        return data.to_json(orient="records")
    elif format == "csv":
        return data.to_csv(index=False)
    else:
        return "Invalid format"

@app.get("/api/record/<int:id>") # used chatgpt for <int:id>
def index_find(id):
    format = request.args.get("format", "json")
    data = pd.read_csv("Causes_of_Death_2026.csv") 
    location = data.iloc[[id]]    
    return convert_to_format(location,format)

@app.get("/api/i_want_extra_credit")
def hehe():
    return """<img src="/static/PLEASE.png" width="500">"""

@app.get("/api/covid_death")
def covid_death():
    format = request.args.get("format", "json")
    data = pd.read_csv("Causes_of_Death_2026.csv") 
    covid_df = data[data["Leading Cause"] == "Covid-19"]
    covid_df = covid_df.drop(columns = ["Death Rate", "Age Adjusted Death Rate"])
    return convert_to_format(covid_df, format)

create_users_table()
@app.route("/users",methods = ["POST"])
def add_user():
    data = request.get_json()
    
    username = data.get("username")
    age = data.get("age")
    country = data.get("country")

    con = duckdb.connect("file.db")

    con.execute(
        "INSERT INTO users (username, age, country) VALUES (?, ?, ?)",
        [username, age, country],
    )
    con.close()
    return jsonify({"message": f"PUser '{username}' added"})

@app.route("/users/stats", methods=["GET"])
def get_user_stats():

    con = duckdb.connect("file.db")

    count = con.sql("SELECT COUNT(*) FROM users").fetchone()[0]

    avg_age = con.sql("SELECT AVG(age) FROM users").fetchone()[0]

    top_countries = con.sql("""
        SELECT country, COUNT(*) as total
        FROM users
        GROUP BY country
        ORDER BY total DESC
        LIMIT 3
    """).fetchall()

    con.close()

    return {
        "num_users": count,
        "average_age": round(avg_age, 2) if avg_age else None,
        "Top_3_countries": [
            {"country": r[0], "count": r[1]} for r in top_countries
        ]
    }
    

if __name__ == "__main__":
    app.run(debug=True)
