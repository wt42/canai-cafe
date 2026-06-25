"""
Generate a Power BI-ready Excel file with pre-calculated sheets.
Each sheet maps directly to a visual in Power BI — just drag and drop.

Run from project root:
    python scripts/generate_powerbi_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "clean_output.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "powerbi_ready.xlsx"


def main():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["transaction_date"])

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

        # Sheet 1: Full cleaned data (for slicers and custom visuals)
        clean = df[["transaction_id", "item", "quantity", "price_per_unit", "total_spent",
                     "payment_method", "location", "transaction_date", "transaction_month",
                     "weekday_name", "day_type", "province"]].copy()
        clean.to_excel(writer, sheet_name="Transactions", index=False)
        print("  Sheet: Transactions (10,000 rows - full clean data)")

        # Sheet 2: Monthly Sales
        dated = df[df["transaction_date"].notna()].copy()
        monthly = dated.groupby("transaction_month").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count"),
            Units_Sold=("quantity", "sum")
        ).reset_index()
        monthly.columns = ["Month", "Revenue", "Transactions", "Units Sold"]
        monthly.to_excel(writer, sheet_name="Monthly Sales", index=False)
        print("  Sheet: Monthly Sales (revenue by month)")

        # Sheet 3: Product Performance
        products = df.groupby("item").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count"),
            Units_Sold=("quantity", "sum")
        ).reset_index()
        products.columns = ["Product", "Revenue", "Transactions", "Units Sold"]
        products["Avg Transaction"] = round(products["Revenue"] / products["Transactions"], 2)
        products["Revenue Share %"] = round(products["Revenue"] / products["Revenue"].sum() * 100, 1)
        products = products.sort_values("Revenue", ascending=False)
        products.to_excel(writer, sheet_name="Products", index=False)
        print("  Sheet: Products (revenue by product)")

        # Sheet 4: Province Performance
        prov = df[df["province"].notna()].groupby("province").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count"),
            Units_Sold=("quantity", "sum")
        ).reset_index()
        prov.columns = ["Province", "Revenue", "Transactions", "Units Sold"]
        prov["Revenue Share %"] = round(prov["Revenue"] / prov["Revenue"].sum() * 100, 1)
        prov = prov.sort_values("Revenue", ascending=False)
        prov.to_excel(writer, sheet_name="Provinces", index=False)
        print("  Sheet: Provinces (revenue by province)")

        # Sheet 5: Payment Methods
        pay = df.groupby("payment_method").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count")
        ).reset_index()
        pay.columns = ["Payment Method", "Revenue", "Transactions"]
        pay["Revenue Share %"] = round(pay["Revenue"] / pay["Revenue"].sum() * 100, 1)
        pay = pay.sort_values("Revenue", ascending=False)
        pay.to_excel(writer, sheet_name="Payments", index=False)
        print("  Sheet: Payments (revenue by payment method)")

        # Sheet 6: Location
        loc = df.groupby("location").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count")
        ).reset_index()
        loc.columns = ["Location", "Revenue", "Transactions"]
        loc["Revenue Share %"] = round(loc["Revenue"] / loc["Revenue"].sum() * 100, 1)
        loc = loc.sort_values("Revenue", ascending=False)
        loc.to_excel(writer, sheet_name="Locations", index=False)
        print("  Sheet: Locations (In-store vs Takeaway)")

        # Sheet 7: Weekday Analysis
        weekday = dated.groupby("weekday_name").agg(
            Revenue=("total_spent", "sum"),
            Transactions=("transaction_id", "count")
        ).reset_index()
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday["weekday_name"] = pd.Categorical(weekday["weekday_name"], categories=day_order, ordered=True)
        weekday = weekday.sort_values("weekday_name")
        weekday.columns = ["Day", "Revenue", "Transactions"]
        weekday.to_excel(writer, sheet_name="Weekday", index=False)
        print("  Sheet: Weekday (revenue by day of week)")

        # Sheet 8: KPI Summary (for cards)
        kpis = pd.DataFrame([
            {"KPI": "Total Revenue", "Value": round(df["total_spent"].sum(), 2)},
            {"KPI": "Total Transactions", "Value": len(df)},
            {"KPI": "Total Units Sold", "Value": int(df["quantity"].sum())},
            {"KPI": "Avg Transaction Value", "Value": round(df["total_spent"].sum() / len(df), 2)},
            {"KPI": "Top Product", "Value": df.groupby("item")["total_spent"].sum().idxmax()},
            {"KPI": "Top Province", "Value": df[df["province"].notna()].groupby("province")["total_spent"].sum().idxmax()},
        ])
        kpis.to_excel(writer, sheet_name="KPIs", index=False)
        print("  Sheet: KPIs (summary numbers for cards)")

    print(f"\n  Saved to: {OUTPUT_FILE}")
    print("\nOpen this file in Power BI Desktop: Get Data → Excel Workbook")


if __name__ == "__main__":
    main()
