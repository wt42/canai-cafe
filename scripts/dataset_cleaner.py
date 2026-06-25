"""
CanAI Cafe Dataset Cleaner
--------------------------
Purpose:
    Clean the 2023 CanAI Cafe transaction dataset for BI, forecasting, and dashboard work.

Key principles:
    1. Do not delete recoverable rows.
    2. Repair numeric fields before filtering invalid rows.
    3. Standardize dirty text values.
    4. Keep unknown values explicit instead of hiding blanks.
    5. Flag duplicate Transaction IDs instead of blindly removing them.

Run from project root:
    python scripts/dataset_cleaner.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

INPUT_FILE = RAW_DIR / "CanAI Cafe 2023 Sales Information.xlsx"
OUTPUT_FILE = PROCESSED_DIR / "clean_output.csv"
SUMMARY_FILE = PROCESSED_DIR / "cleaning_summary.csv"
REJECTED_FILE = PROCESSED_DIR / "rejected_rows.csv"

# Price uniquely identifies item in this dataset.
UNIT_PRICE_ITEM_MAP: Dict[float, str] = {
    2.00: "Donut",
    2.50: "Cookie",
    3.00: "Tea",
    3.50: "Coffee",
    4.50: "Juice",
    5.00: "Refresher",
    8.00: "Sandwich",
    9.00: "Salad",
}

VALID_PAYMENT_METHODS = {"Cash", "Credit Card", "Digital Wallet"}
VALID_LOCATIONS = {"In-store", "Takeaway"}


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to snake_case."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def clean_text_series(values: pd.Series) -> pd.Series:
    """Trim text values and convert blanks / placeholder text to missing values."""
    cleaned = values.astype("string").str.strip()
    cleaned = cleaned.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
            "None": pd.NA,
            "UNKNOWN": pd.NA,
            "Unknown": pd.NA,
            "unknown": pd.NA,
        }
    )
    return cleaned


def standardize_items(items: pd.Series) -> pd.Series:
    """Standardize item spellings and casing."""
    cleaned = clean_text_series(items).str.lower()

    item_map = {
        "c0ffee": "Coffee",
        "coffee": "Coffee",
        "cofee": "Coffee",
        "coffe": "Coffee",
        "donut": "Donut",
        "donutt": "Donut",
        "doughnut": "Donut",
        "juice": "Juice",
        "juic": "Juice",
        "juicee": "Juice",
        "sandwich": "Sandwich",
        "sandwhich": "Sandwich",
        "tea": "Tea",
        "tee": "Tea",
        "cookie": "Cookie",
        "salad": "Salad",
        "refresher": "Refresher",
    }

    return cleaned.replace(item_map)


def clean_province(provinces: pd.Series) -> pd.Series:
    """Standardize Canadian province names found in the dataset."""
    cleaned = clean_text_series(provinces).str.lower()
    cleaned = cleaned.str.replace(r"\s+", " ", regex=True)

    province_map = {
        "bc": "British Columbia",
        "b.c.": "British Columbia",
        "british columbia": "British Columbia",
        "britishcolumbia": "British Columbia",
        "british columba": "British Columbia",
        "british columbi": "British Columbia",
        "mb": "Manitoba",
        "manitoba": "Manitoba",
        "manitob": "Manitoba",
        "manitba": "Manitoba",
        "manitobaa": "Manitoba",
        "nfld": "Newfoundland and Labrador",
        "nl": "Newfoundland and Labrador",
        "newfoundland": "Newfoundland and Labrador",
        "newfoundlan": "Newfoundland and Labrador",
        "new foundland": "Newfoundland and Labrador",
        "newfoundland and labrador": "Newfoundland and Labrador",
        "sk": "Saskatchewan",
        "sask.": "Saskatchewan",
        "saskatchewan": "Saskatchewan",
        "saskatchewa": "Saskatchewan",
        "sasktchewan": "Saskatchewan",
        "saskatchewn": "Saskatchewan",
        "on": "Ontario",
        "ont.": "Ontario",
        "ontario": "Ontario",
        "ontairo": "Ontario",
        "ontaroi": "Ontario",
    }

    return cleaned.replace(province_map)


def clean_payment_method(payment_methods: pd.Series) -> pd.Series:
    """Standardize payment method and make invalid/missing values explicit."""
    cleaned = clean_text_series(payment_methods).str.lower()

    payment_map = {
        "cash": "Cash",
        "credit card": "Credit Card",
        "creditcard": "Credit Card",
        "digital wallet": "Digital Wallet",
        "digitalwallet": "Digital Wallet",
        "err_pm_102": "Unknown Payment",
    }

    cleaned = cleaned.replace(payment_map)
    cleaned = cleaned.where(cleaned.isin(VALID_PAYMENT_METHODS), "Unknown Payment")
    return cleaned


def clean_location(locations: pd.Series) -> pd.Series:
    """Standardize transaction location and make missing values explicit."""
    cleaned = clean_text_series(locations).str.lower()

    location_map = {
        "in-store": "In-store",
        "instore": "In-store",
        "in store": "In-store",
        "takeaway": "Takeaway",
        "take away": "Takeaway",
    }

    cleaned = cleaned.replace(location_map)
    cleaned = cleaned.where(cleaned.isin(VALID_LOCATIONS), "Unknown Location")
    return cleaned


def repair_numeric_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Repair quantity, price_per_unit, and total_spent when two of the three fields are present.

    This fixes the earlier bug where missing quantity rows were dropped before repair.
    """
    df = df.copy()

    for col in ["quantity", "price_per_unit", "total_spent"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["quantity_repaired_flag"] = False
    df["price_per_unit_repaired_flag"] = False
    df["total_spent_repaired_flag"] = False

    quantity_mask = (
        df["quantity"].isna()
        & df["total_spent"].notna()
        & df["price_per_unit"].notna()
        & (df["price_per_unit"] > 0)
    )
    df.loc[quantity_mask, "quantity"] = (
        df.loc[quantity_mask, "total_spent"] / df.loc[quantity_mask, "price_per_unit"]
    )
    df.loc[quantity_mask, "quantity_repaired_flag"] = True

    total_mask = (
        df["total_spent"].isna()
        & df["quantity"].notna()
        & df["price_per_unit"].notna()
    )
    df.loc[total_mask, "total_spent"] = (
        df.loc[total_mask, "quantity"] * df.loc[total_mask, "price_per_unit"]
    )
    df.loc[total_mask, "total_spent_repaired_flag"] = True

    price_mask = (
        df["price_per_unit"].isna()
        & df["total_spent"].notna()
        & df["quantity"].notna()
        & (df["quantity"] > 0)
    )
    df.loc[price_mask, "price_per_unit"] = (
        df.loc[price_mask, "total_spent"] / df.loc[price_mask, "quantity"]
    )
    df.loc[price_mask, "price_per_unit_repaired_flag"] = True

    return df


def infer_missing_items_from_price(df: pd.DataFrame) -> pd.DataFrame:
    """Infer missing item values using the known price-to-item mapping."""
    df = df.copy()
    df["item_imputed_flag"] = False

    rounded_price = df["price_per_unit"].round(2)
    item_mask = df["item"].isna() & rounded_price.isin(UNIT_PRICE_ITEM_MAP.keys())

    df.loc[item_mask, "item"] = rounded_price.loc[item_mask].map(UNIT_PRICE_ITEM_MAP)
    df.loc[item_mask, "item_imputed_flag"] = True

    return df


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add date-derived fields useful for dashboarding and forecasting.

    Dates may arrive as Excel/Pandas datetime values or text values such as
    "2023-01-01". This function avoids forcing one strict text format so
    valid datetime values are not accidentally converted to missing dates.
    """
    df = df.copy()

    raw_dates = df["transaction_date"].copy()

    # Clean obvious string placeholders while preserving real datetime objects.
    text_mask = raw_dates.apply(lambda value: isinstance(value, str))
    raw_dates.loc[text_mask] = raw_dates.loc[text_mask].str.strip().replace(
        {
            "": pd.NA,
            "UNKNOWN": pd.NA,
            "Unknown": pd.NA,
            "unknown": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
            "None": pd.NA,
        }
    )

    df["transaction_date"] = pd.to_datetime(raw_dates, errors="coerce")

    df["missing_date_flag"] = df["transaction_date"].isna()
    df["transaction_month"] = df["transaction_date"].dt.to_period("M").astype("string")
    df["weekday_name"] = df["transaction_date"].dt.day_name()
    df["day_type"] = np.where(
        df["transaction_date"].dt.dayofweek >= 5, "Weekend", "Weekday"
    )
    df.loc[df["transaction_date"].isna(), ["transaction_month", "weekday_name", "day_type"]] = pd.NA

    return df


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add transparent quality flags for reporting and auditability."""
    df = df.copy()

    df["duplicate_transaction_id_flag"] = df["transaction_id"].duplicated(keep=False)
    df["unknown_payment_flag"] = df["payment_method"].eq("Unknown Payment")
    df["unknown_location_flag"] = df["location"].eq("Unknown Location")
    df["unknown_province_flag"] = df["province"].eq("Unknown Province")

    expected_total = df["quantity"] * df["price_per_unit"]
    df["revenue_mismatch_flag"] = (expected_total - df["total_spent"]).abs() > 0.01

    rounded_price = df["price_per_unit"].round(2)
    df["item_price_mismatch_flag"] = False
    known_price_rows = rounded_price.isin(UNIT_PRICE_ITEM_MAP.keys()) & df["item"].notna()
    df.loc[known_price_rows, "item_price_mismatch_flag"] = (
        df.loc[known_price_rows, "item"]
        != rounded_price.loc[known_price_rows].map(UNIT_PRICE_ITEM_MAP)
    )

    return df


def build_cleaning_summary(original_df: pd.DataFrame, cleaned_df: pd.DataFrame, rejected_df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact cleaning summary for documentation and presentation."""
    summary_rows = [
        ("Original rows", len(original_df)),
        ("Cleaned rows", len(cleaned_df)),
        ("Rejected rows", len(rejected_df)),
        ("Rows with missing/invalid transaction date", int(cleaned_df["missing_date_flag"].sum())),
        ("Rows with missing item inferred from price", int(cleaned_df["item_imputed_flag"].sum())),
        ("Rows with quantity repaired", int(cleaned_df["quantity_repaired_flag"].sum())),
        ("Rows with total_spent repaired", int(cleaned_df["total_spent_repaired_flag"].sum())),
        ("Rows with price_per_unit repaired", int(cleaned_df["price_per_unit_repaired_flag"].sum())),
        ("Rows with Unknown Payment", int(cleaned_df["unknown_payment_flag"].sum())),
        ("Rows with Unknown Location", int(cleaned_df["unknown_location_flag"].sum())),
        ("Rows with Unknown Province", int(cleaned_df["unknown_province_flag"].sum())),
        ("Duplicate Transaction ID rows flagged", int(cleaned_df["duplicate_transaction_id_flag"].sum())),
        ("Revenue mismatch rows", int(cleaned_df["revenue_mismatch_flag"].sum())),
        ("Item/price mismatch rows", int(cleaned_df["item_price_mismatch_flag"].sum())),
        ("Total revenue in cleaned data", round(float(cleaned_df["total_spent"].sum()), 2)),
    ]

    return pd.DataFrame(summary_rows, columns=["metric", "value"])


def clean_dataset(input_file: Path = INPUT_FILE) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Main reusable cleaning function."""
    original_df = pd.read_excel(input_file)
    df = standardize_column_names(original_df)

    required_columns = {
        "transaction_id",
        "item",
        "quantity",
        "price_per_unit",
        "total_spent",
        "payment_method",
        "location",
        "transaction_date",
        "province",
    }
    missing_columns = sorted(required_columns - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df.insert(0, "source_row_number", np.arange(2, len(df) + 2))  # Excel data starts on row 2.

    # Text cleaning first.
    df["item"] = standardize_items(df["item"])
    df["province"] = clean_province(df["province"])
    df["payment_method"] = clean_payment_method(df["payment_method"])
    df["location"] = clean_location(df["location"])

    # Numeric repair before numeric filtering.
    df = repair_numeric_fields(df)

    # Recover missing item values after price is numeric.
    df = infer_missing_items_from_price(df)

    # Explicit unknown labels for dashboard friendliness.
    df["item"] = df["item"].fillna("Unknown Item")
    df["province"] = df["province"].fillna("Unknown Province")

    # Date features.
    df = add_date_features(df)

    # Now reject only truly invalid numeric rows.
    invalid_numeric_mask = (
        df["quantity"].isna()
        | df["price_per_unit"].isna()
        | df["total_spent"].isna()
        | (df["quantity"] <= 0)
        | (df["price_per_unit"] <= 0)
        | (df["total_spent"] <= 0)
    )
    rejected_df = df.loc[invalid_numeric_mask].copy()
    cleaned_df = df.loc[~invalid_numeric_mask].copy()

    # Make quantity integer where repaired calculation produced whole numbers.
    cleaned_df["quantity"] = cleaned_df["quantity"].round(0).astype("Int64")

    # Add audit/reporting flags after final numeric cleanup.
    cleaned_df = add_quality_flags(cleaned_df)

    # Format date cleanly for CSV output.
    cleaned_df["transaction_date"] = cleaned_df["transaction_date"].dt.strftime("%Y-%m-%d")

    # Reorder columns for readability.
    preferred_order = [
        "source_row_number",
        "transaction_id",
        "item",
        "quantity",
        "price_per_unit",
        "total_spent",
        "payment_method",
        "location",
        "transaction_date",
        "transaction_month",
        "weekday_name",
        "day_type",
        "province",
        "duplicate_transaction_id_flag",
        "missing_date_flag",
        "item_imputed_flag",
        "quantity_repaired_flag",
        "price_per_unit_repaired_flag",
        "total_spent_repaired_flag",
        "unknown_payment_flag",
        "unknown_location_flag",
        "unknown_province_flag",
        "revenue_mismatch_flag",
        "item_price_mismatch_flag",
    ]
    remaining_columns = [col for col in cleaned_df.columns if col not in preferred_order]
    cleaned_df = cleaned_df[preferred_order + remaining_columns]

    summary_df = build_cleaning_summary(original_df, cleaned_df, rejected_df)

    return cleaned_df, summary_df, rejected_df


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_df, summary_df, rejected_df = clean_dataset(INPUT_FILE)

    cleaned_df.to_csv(OUTPUT_FILE, index=False)
    summary_df.to_csv(SUMMARY_FILE, index=False)
    rejected_df.to_csv(REJECTED_FILE, index=False)

    print("Cleaning completed successfully.")
    print(f"Clean output: {OUTPUT_FILE}")
    print(f"Cleaning summary: {SUMMARY_FILE}")
    print(f"Rejected rows: {REJECTED_FILE}")
    print("\nSummary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
