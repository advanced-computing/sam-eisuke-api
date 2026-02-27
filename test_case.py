import pandas as pd
from test import deaths_by_year, cause_share_by_year,clean_empty
import pytest
def test_deaths_by_year(): # summing total deaths by year
    df = pd.DataFrame({
        "Year": [2020, 2020, 2021],
        "Deaths": [100, 50, 200]
    })

    result = deaths_by_year(df)

    assert result.loc[result["Year"] == 2020, "Deaths"].values[0] == 150
    assert result.loc[result["Year"] == 2021, "Deaths"].values[0] == 200

def test_cause_share_by_year(): # compares number of deaths to the total
    df = pd.DataFrame({
        "Year": [2020,2020,2020],
        "Cause": ["Covid-19", "All Other Causes","Alzheimer's Disease (G30)"],
        "Deaths": [100,50,50]
    })

    result = cause_share_by_year(df,2020, "Covid-19")
    assert result == 100 / 200

def test_clean_empty(): # deletes empty rows 
    df = pd.DataFrame({
        "Death Rate": ["ABC", None],
        "Age Adjusted Death Rate": [1, "Xyz"]

    })
    result = clean_empty(df)

    assert len(result) == 0


