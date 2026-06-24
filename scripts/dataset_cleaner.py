from pathlib import Path
import pandas as pd
import numpy as np


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

INPUT_FILE = DATA_DIR / "CanAI Cafe 2023 Sales Information.xlsx"
OUTPUT_FILE = DATA_DIR / "clean_output.csv"


def clean_province(provinces):
    provinces = provinces.astype(str).str.strip().str.lower()

    province_map = {
        "bc": "British Columbia",
        "b.c.": "British Columbia",
        "british columbia": "British Columbia",
        "britishcolumbia": "British Columbia", 
        "british columba": "British Columbia",
        "british columbi": "British Columbia",

        "mb": "Manitoba",
        "manitba": "Manitoba",
        "manitoba": "Manitoba",
        "manitobaa": "Manitoba",

        "nfld": "Newfoundland",
        "newfoundland": "Newfoundland",
        "nl": "Newfoundland",
        "newfoundlan": "Newfoundland",
        "new foundland": "Newfoundland",
        "newfoundland and labrador": "Newfoundland",

        "sk": "Saskatchewan",
        "sask.": "Saskatchewan",
        "saskatchewa": "Saskatchewan",
        "saskatchewan": "Saskatchewan",
        "sasktchewan": "Saskatchewan",
        "saskatchewn": "Saskatchewan", 

        "on": "Ontario",
        "ont.": "Ontario",
        "ontairo": "Ontario",
        "ontaroi": "Ontario",
        "ontario": "Ontario"
    }

    provinces = provinces.replace(province_map)
    provinces = provinces.replace([""," "], np.nan)

    return provinces


def standardize_items(items):
    items = items.astype(str).str.strip().str.lower()

    item_map = {
    
    "C0ffee": "Coffee",
    "Cofee": "Coffee",
    "cofee": "Coffee",
    "coffe": "Coffee",
    "coffee": "Coffee",

    "Donutt": "Donut",
    "Doughnut": "Donut",
    "donut": "Donut",

    "Juic": "Juice",
    "Juicee": "Juice",
    "juice": "Juice",

    "Sandwhich": "Sandwich",
    "sandwich": "Sandwich",

    "TEA": "Tea",
    "Tee": "Tea",
    "tee": "Tea",
    }

    items = items.replace(item_map)
    items = items.replace([""," "], np.nan)

    return items
    


def main():

    df = pd.read_excel(INPUT_FILE)

    # standardize column names
    df.columns = (
        df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
    )
    # print(df.columns)

    # clean province names
    df["province"] = clean_province(df["province"])

    # Standardize item names
    df["item"] = standardize_items(df["item"])

    # Clean payment methods
    df["payment_method"] = df["payment_method"].replace(["ERR_PM_102"], np.nan)

    # Handle unknown dates
    df["transaction_date"] = df["transaction_date"].replace(["UNKNOWN"], np.nan)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # Remove invalid numeric values
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
    df["total_spent"] = pd.to_numeric(df["total_spent"], errors="coerce")
    df = df[
        (df["quantity"] > 0) &
        (df["price_per_unit"] > 0) &
        (df["total_spent"] > 0)
    ]

    # Fill missing total_spent
    mask = df["total_spent"].isna() & df["quantity"].notna() & df["price_per_unit"].notna()

    df.loc[mask, "total_spent"] = (
        df.loc[mask, "quantity"] * df.loc[mask, "price_per_unit"]
    )

    # Fill missing quantity
    mask = df["quantity"].isna() & df["total_spent"].isna() & df["price_per_unit"].notna()

    df.loc[mask, "quantity"] = (
        df.loc[mask, "total_spent"] / df.loc[mask, "price_per_unit"]
    )
    
    # Fill missing price per unit
    mask = df["price_per_unit"].isna() & df["total_spent"].isna() & df["quantity"].notna()

    df.loc[mask, "price_per_unit"] = (
        df.loc[mask, "total_spent"] / df.loc[mask, "quantity"]
    )

    # check price consistency per item 
    price_check = df.groupby("item")["price_per_unit"].nunique()
    # print(price_check)

    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
