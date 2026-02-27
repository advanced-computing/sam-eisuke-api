import pandas as pd

def deaths_by_year(data):

    grouped = (
        data.groupby("Year")["Deaths"]
        .sum()
        .reset_index()
        .sort_values("Year")
    )

    return grouped

def cause_share_by_year(data, year,cause):
    df = data.copy()
    year_df = df[df["Year"] == year]
    if year_df.empty:
        raise ValueError("Year not found")
    
    total_deaths = year_df["Deaths"].sum()

    cause_deaths = year_df[year_df["Cause"] == cause]["Deaths"].sum()
    if year_df[year_df["Cause"] == cause].empty:
        raise ValueError("Cause not found")
    
    return cause_deaths/total_deaths

def clean_empty(data):
    df = data.copy()
    df["Death Rate"] = pd.to_numeric(df["Death Rate"], errors="coerce")
    df["Age Adjusted Death Rate"] = pd.to_numeric(df["Age Adjusted Death Rate"], errors = "coerce")
    df = df.dropna()

    return df

