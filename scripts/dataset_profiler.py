"""
CanAI Cafe Dataset Profiler
---------------------------
Purpose:
    Profile the raw dataset and cleaned dataset to support the hackathon cleaning summary.

Run from project root:
    python scripts/dataset_profiler.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from dataset_cleaner import (
    INPUT_FILE,
    OUTPUT_FILE,
    clean_province,
    standardize_column_names,
    standardize_items,
)

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_FILE = ROOT_DIR / "data" / "processed" / "profile_report.txt"


def section(title: str) -> str:
    return "\n" + "=" * 90 + f"\n{title}\n" + "=" * 90 + "\n"


def format_counts(series: pd.Series) -> str:
    return series.value_counts(dropna=False).sort_index().to_string()


def profile_raw_dataset() -> str:
    df = pd.read_excel(INPUT_FILE)
    normalized_df = standardize_column_names(df)

    output = []
    output.append(section("RAW DATASET SHAPE"))
    output.append(f"Rows: {len(df):,}\n")
    output.append(f"Columns: {len(df.columns):,}\n")
    output.append("Column names:\n" + "\n".join(f"- {col}" for col in df.columns) + "\n")

    output.append(section("RAW MISSING VALUES"))
    output.append(normalized_df.isna().sum().sort_values(ascending=False).to_string() + "\n")

    output.append(section("RAW UNIQUE ITEM NAMES"))
    output.append(format_counts(df["Item"].astype("string").str.strip()) + "\n")

    output.append(section("STANDARDIZED ITEM NAMES"))
    output.append(format_counts(standardize_items(df["Item"])) + "\n")

    output.append(section("RAW UNIQUE PROVINCE NAMES"))
    output.append(format_counts(df["Province"].astype("string").str.strip()) + "\n")

    output.append(section("STANDARDIZED PROVINCE NAMES"))
    output.append(format_counts(clean_province(df["Province"])) + "\n")

    output.append(section("RAW PAYMENT METHODS"))
    output.append(format_counts(df["Payment Method"].astype("string").str.strip()) + "\n")

    output.append(section("RAW LOCATIONS"))
    output.append(format_counts(df["Location"].astype("string").str.strip()) + "\n")

    output.append(section("DUPLICATE TRANSACTION ID CHECK"))
    duplicate_rows = normalized_df["transaction_id"].duplicated(keep=False).sum()
    duplicate_ids = normalized_df.loc[
        normalized_df["transaction_id"].duplicated(keep=False), "transaction_id"
    ].nunique()
    output.append(f"Duplicate transaction ID rows: {duplicate_rows:,}\n")
    output.append(f"Duplicate transaction IDs: {duplicate_ids:,}\n")

    return "".join(output)


def profile_cleaned_dataset() -> str:
    if not OUTPUT_FILE.exists():
        return section("CLEANED DATASET") + "clean_output.csv not found. Run dataset_cleaner.py first.\n"

    df = pd.read_csv(OUTPUT_FILE)
    output = []
    output.append(section("CLEANED DATASET SHAPE"))
    output.append(f"Rows: {len(df):,}\n")
    output.append(f"Columns: {len(df.columns):,}\n")

    output.append(section("CLEANED MISSING VALUES"))
    output.append(df.isna().sum().sort_values(ascending=False).to_string() + "\n")

    output.append(section("REVENUE SUMMARY"))
    output.append(f"Total revenue: {df['total_spent'].sum():,.2f}\n")
    output.append(f"Total units: {df['quantity'].sum():,.0f}\n")
    output.append(f"Average transaction value: {df['total_spent'].mean():,.2f}\n")

    output.append(section("PRODUCT REVENUE"))
    output.append(
        df.groupby("item")["total_spent"].sum().sort_values(ascending=False).to_string() + "\n"
    )

    output.append(section("PROVINCE REVENUE"))
    output.append(
        df.groupby("province")["total_spent"].sum().sort_values(ascending=False).to_string() + "\n"
    )

    output.append(section("PAYMENT METHOD REVENUE"))
    output.append(
        df.groupby("payment_method")["total_spent"].sum().sort_values(ascending=False).to_string() + "\n"
    )

    output.append(section("LOCATION REVENUE"))
    output.append(
        df.groupby("location")["total_spent"].sum().sort_values(ascending=False).to_string() + "\n"
    )

    output.append(section("QUALITY FLAGS"))
    flag_cols = [col for col in df.columns if col.endswith("_flag")]
    output.append(df[flag_cols].sum().sort_values(ascending=False).to_string() + "\n")

    return "".join(output)


def main() -> None:
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report = profile_raw_dataset() + profile_cleaned_dataset()
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nProfile report written to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
