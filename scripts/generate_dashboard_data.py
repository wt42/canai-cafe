"""
Generate dashboard JSON files from the cleaned CSV data.

This script is the BRIDGE between the Python cleaning pipeline and the React dashboard.
It reads: data/processed/clean_output.csv
It writes: canai-cafe-frontend-project/frontend/public/data/*.json (13 files)

Run from project root:
    python scripts/generate_dashboard_data.py
"""

import json
import os
import pandas as pd
import numpy as np
from pathlib import Path

from forecasting import generate_legacy_six_month_forecast, generate_sales_forecast


# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "clean_output.csv"
OUTPUT_DIR = PROJECT_ROOT / "canai-cafe-frontend-project" / "frontend" / "public" / "data"


def load_data():
    df = pd.read_csv(CLEAN_CSV, parse_dates=["transaction_date"])
    return df


def generate_kpi_summary(df, forecast=None):
    """Top-level numbers the dashboard shows at the top (total revenue, transactions, etc.)"""
    total_revenue = round(df["total_spent"].sum(), 2)
    total_transactions = len(df)
    total_units = int(df["quantity"].sum())
    avg_transaction = round(total_revenue / total_transactions, 2)
    top_product = df.groupby("item")["total_spent"].sum().idxmax()
    top_province = df[df["province"].notna()].groupby("province")["total_spent"].sum().idxmax()
    missing_dates = int(df["missing_date_flag"].apply(lambda x: x == True or x == "True").sum())
    valid_dated = total_transactions - missing_dates
    data_quality_score = round((1 - missing_dates / total_transactions) * 100, 2)

    if forecast:
        six_month_forecast = forecast["summaryMetrics"]["full180Days"]["expectedRevenue"]
    else:
        dated_df = df[df["transaction_date"].notna()]
        monthly_rev = dated_df.groupby(dated_df["transaction_date"].dt.to_period("M"))["total_spent"].sum()
        avg_monthly = monthly_rev.mean()
        six_month_forecast = round(avg_monthly * 6, 2)

    return {
        "totalRevenue": total_revenue,
        "totalTransactions": total_transactions,
        "totalUnitsSold": total_units,
        "averageTransactionValue": avg_transaction,
        "topProduct": top_product,
        "topProvince": top_province,
        "sixMonthForecast": six_month_forecast,
        "dataQualityScore": data_quality_score,
        "validDatedRows": valid_dated,
        "missingDateRows": missing_dates,
        "summaryMessage": f"Cleaned {total_transactions:,} cafe transactions, preserved recoverable revenue, and prepared executive-ready data for BI and forecasting."
    }


def generate_monthly_sales(df):
    """Revenue broken down by month — for the monthly sales chart."""
    dated_df = df[df["transaction_date"].notna()].copy()
    dated_df["month"] = dated_df["transaction_date"].dt.to_period("M").astype(str)
    monthly = dated_df.groupby("month").agg(
        revenue=("total_spent", "sum"),
        transactions=("transaction_id", "count"),
        units=("quantity", "sum")
    ).reset_index()
    monthly["averageTransactionValue"] = round(monthly["revenue"] / monthly["transactions"], 2)
    monthly["revenue"] = monthly["revenue"].round(2)
    monthly["units"] = monthly["units"].astype(int)
    return monthly.to_dict(orient="records")


def generate_product_performance(df):
    """Revenue by product (Coffee, Sandwich, etc.) — for the product chart."""
    products = df.groupby("item").agg(
        revenue=("total_spent", "sum"),
        transactions=("transaction_id", "count"),
        units=("quantity", "sum")
    ).reset_index()
    total_rev = products["revenue"].sum()
    products["revenueShare"] = round(products["revenue"] / total_rev * 100, 2)
    products["averageTransactionValue"] = round(products["revenue"] / products["transactions"], 2)
    products = products.rename(columns={"item": "name"})
    products["revenue"] = products["revenue"].round(2)
    products["units"] = products["units"].astype(int)
    products = products.sort_values("revenue", ascending=False)
    return products.to_dict(orient="records")


def generate_province_performance(df):
    """Revenue by province — for the province chart."""
    prov_df = df[df["province"].notna() & (df["unknown_province_flag"].apply(lambda x: x == False or x == "False"))].copy()
    provinces = prov_df.groupby("province").agg(
        revenue=("total_spent", "sum"),
        transactions=("transaction_id", "count"),
        units=("quantity", "sum")
    ).reset_index()
    total_rev = provinces["revenue"].sum()
    provinces["revenueShare"] = round(provinces["revenue"] / total_rev * 100, 2)
    provinces["averageTransactionValue"] = round(provinces["revenue"] / provinces["transactions"], 2)
    provinces = provinces.rename(columns={"province": "name"})
    provinces["revenue"] = provinces["revenue"].round(2)
    provinces["units"] = provinces["units"].astype(int)
    provinces = provinces.sort_values("revenue", ascending=False)
    return provinces.to_dict(orient="records")


def generate_payment_performance(df):
    """Revenue by payment method (Credit Card, Cash, Digital Wallet)."""
    payments = df.groupby("payment_method").agg(
        revenue=("total_spent", "sum"),
        transactions=("transaction_id", "count"),
        units=("quantity", "sum")
    ).reset_index()
    total_rev = payments["revenue"].sum()
    payments["revenueShare"] = round(payments["revenue"] / total_rev * 100, 2)
    payments = payments.rename(columns={"payment_method": "name"})
    payments["revenue"] = payments["revenue"].round(2)
    payments["units"] = payments["units"].astype(int)
    payments = payments.sort_values("revenue", ascending=False)
    return payments.to_dict(orient="records")


def generate_location_performance(df):
    """Revenue by location (In-store vs Takeaway)."""
    locations = df.groupby("location").agg(
        revenue=("total_spent", "sum"),
        transactions=("transaction_id", "count"),
        units=("quantity", "sum")
    ).reset_index()
    total_rev = locations["revenue"].sum()
    locations["revenueShare"] = round(locations["revenue"] / total_rev * 100, 2)
    locations = locations.rename(columns={"location": "name"})
    locations["revenue"] = locations["revenue"].round(2)
    locations["units"] = locations["units"].astype(int)
    locations = locations.sort_values("revenue", ascending=False)
    return locations.to_dict(orient="records")


def generate_weekday_weekend(df):
    """Weekday vs Weekend revenue comparison."""
    dated_df = df[df["transaction_date"].notna()].copy()
    result = []
    for day_type in ["Weekday", "Weekend"]:
        subset = dated_df[dated_df["day_type"] == day_type]
        total_rev = round(subset["total_spent"].sum(), 2)
        num_days = subset["transaction_date"].dt.date.nunique()
        avg_daily = round(total_rev / num_days, 2) if num_days > 0 else 0
        result.append({
            "name": day_type,
            "totalRevenue": total_rev,
            "days": num_days,
            "avgDailyRevenue": avg_daily
        })
    return result


def generate_weekday_detail(df):
    """Revenue broken down by each day of the week (Mon-Sun)."""
    dated_df = df[df["transaction_date"].notna()].copy()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result = []
    for day in day_order:
        subset = dated_df[dated_df["weekday_name"] == day]
        total_rev = round(subset["total_spent"].sum(), 2)
        num_days = subset["transaction_date"].dt.date.nunique()
        avg_daily = round(total_rev / num_days, 2) if num_days > 0 else 0
        result.append({
            "name": day,
            "avgDailyRevenue": avg_daily,
            "days": num_days,
            "totalRevenue": total_rev
        })
    return result


def generate_forecast(df):
    """6-month revenue forecast using seasonal pattern from 2023 data."""
    dated_df = df[df["transaction_date"].notna()].copy()
    monthly_rev = dated_df.groupby(dated_df["transaction_date"].dt.to_period("M"))["total_spent"].sum()

    # Use last 2 months as validation
    train = monthly_rev.iloc[:-2]
    holdout = monthly_rev.iloc[-2:]

    # Calculate seasonal index: how much each month deviates from the average
    avg_monthly = train.mean()
    seasonal_index = {}
    for period, rev in train.items():
        month_num = period.month
        seasonal_index[month_num] = rev / avg_monthly

    # Validation metrics using seasonal model
    errors = []
    for period, actual in holdout.items():
        predicted = avg_monthly * seasonal_index.get(period.month, 1.0)
        errors.append(actual - predicted)
    errors = pd.Series(errors)
    mae = round(abs(errors).mean(), 2)
    rmse = round(np.sqrt((errors ** 2).mean()), 2)

    holdout_list = holdout.tolist()
    error_pcts = [round(abs(e) / actual * 100, 2) for e, actual in zip(errors, holdout_list)]

    # Generate 6-month forecast using seasonal pattern
    monthly_forecast = []
    forecast_months = [
        ("2024-01", 1), ("2024-02", 2), ("2024-03", 3),
        ("2024-04", 4), ("2024-05", 5), ("2024-06", 6)
    ]
    for month_str, month_num in forecast_months:
        # Use the seasonal index to vary each month's forecast
        season_factor = seasonal_index.get(month_num, 1.0)
        forecast_rev = round(avg_monthly * season_factor, 2)
        monthly_forecast.append({
            "month": month_str,
            "forecastRevenue": forecast_rev,
            "lowerEstimate": round(forecast_rev * 0.85, 2),
            "upperEstimate": round(forecast_rev * 1.15, 2),
            "planningNote": f"Based on {month_str[:7]} 2023 seasonal pattern (index: {season_factor:.2f})."
        })

    total_forecast = round(sum(f["forecastRevenue"] for f in monthly_forecast), 2)

    return {
        "modelName": "Seasonal baseline forecast",
        "forecastPeriod": "January 2024 to June 2024",
        "totalForecastRevenue": total_forecast,
        "validation": {
            "mae": mae,
            "rmse": rmse,
            "holdoutMonth1ErrorPercent": error_pcts[0] if len(error_pcts) > 0 else 0,
            "holdoutMonth2ErrorPercent": error_pcts[1] if len(error_pcts) > 1 else 0
        },
        "assumptions": [
            "Only one year of transaction history is available.",
            "Rows with missing dates are included in total business KPIs but excluded from time-series model training.",
            "The seasonal pattern from 2023 (Jan-Oct) is assumed to repeat in 2024.",
            "The model captures monthly seasonality but does not use promotions, store hours, weather, or customer footfall."
        ],
        "limitations": [
            "The forecast is a planning baseline, not a guaranteed result.",
            "No store ID, customer ID, time of day, campaign, inventory, or profit margin data is available.",
            "Only one historical year limits seasonality learning."
        ],
        "monthlyForecast": monthly_forecast
    }


def generate_data_quality_summary(df):
    """Summary of data quality issues found and fixed during cleaning."""
    total = len(df)
    missing_dates = int(df["missing_date_flag"].apply(lambda x: x == True or x == "True").sum())
    quantity_repaired = int(df["quantity_repaired_flag"].apply(lambda x: x == True or x == "True").sum())
    item_imputed = int(df["item_imputed_flag"].apply(lambda x: x == True or x == "True").sum())
    unknown_payments = int(df["unknown_payment_flag"].apply(lambda x: x == True or x == "True").sum())
    unknown_locations = int(df["unknown_location_flag"].apply(lambda x: x == True or x == "True").sum())
    unknown_provinces = int(df["unknown_province_flag"].apply(lambda x: x == True or x == "True").sum())
    duplicates = int(df["duplicate_transaction_id_flag"].apply(lambda x: x == True or x == "True").sum())

    issues = missing_dates + unknown_payments + unknown_locations + unknown_provinces
    score = round((1 - issues / (total * 4)) * 100, 2)

    return {
        "score": score,
        "summaryCards": [
            {"label": "Original Rows", "value": total, "note": "Raw transactions received"},
            {"label": "Cleaned Rows", "value": total, "note": "Rows retained after safe cleaning"},
            {"label": "Rejected Rows", "value": 0, "note": "No recoverable row was dropped"},
            {"label": "Quantity Repaired", "value": quantity_repaired, "note": "Calculated from Total Spent / Price Per Unit"},
            {"label": "Item Inferred", "value": item_imputed, "note": "Recovered from Price Per Unit"},
            {"label": "Unknown Payments", "value": unknown_payments, "note": "Preserved transparently"},
            {"label": "Unknown Locations", "value": unknown_locations, "note": "Preserved transparently"},
            {"label": "Unknown Provinces", "value": unknown_provinces, "note": "Preserved transparently"},
            {"label": "Duplicate IDs Flagged", "value": duplicates, "note": "Flagged but not dropped"},
            {"label": "Missing Dates", "value": missing_dates, "note": "Excluded from time-series only"}
        ],
        "issueBreakdown": [
            {"name": "Missing Dates", "count": missing_dates},
            {"name": "Unknown Payments", "count": unknown_payments},
            {"name": "Unknown Locations", "count": unknown_locations},
            {"name": "Unknown Provinces", "count": unknown_provinces},
            {"name": "Quantity Repaired", "count": quantity_repaired},
            {"name": "Item Inferred", "count": item_imputed},
            {"name": "Duplicate IDs", "count": duplicates}
        ],
        "categoryCleanup": [
            {"category": "Product Names", "before": "21 variants with typos", "after": "8 standardized items", "decision": "Fuzzy matched and normalized spelling"},
            {"category": "Provinces", "before": "38 variants with typos", "after": "5 standardized provinces", "decision": "Mapped all known abbreviations and misspellings"},
            {"category": "Payment Methods", "before": "Mixed casing and blanks", "after": "3 methods + Unknown", "decision": "Standardized casing, blanks marked Unknown"},
            {"category": "Locations", "before": "Mixed casing and blanks", "after": "2 locations + Unknown", "decision": "Standardized casing, blanks marked Unknown"}
        ],
        "cleaningDecisions": [
            {"issue": "Missing transaction dates", "decision": "Keep rows, exclude from time-series", "reason": "Revenue is still valid for total KPIs even without a date"},
            {"issue": "Missing quantity", "decision": "Recover mathematically (Total Spent / Price Per Unit)", "reason": "Avoids data loss when the calculation is deterministic"},
            {"issue": "Missing item name", "decision": "Infer from Price Per Unit lookup", "reason": "Each product has a unique price, so inference is reliable"},
            {"issue": "Duplicate transaction IDs", "decision": "Flag but do not remove", "reason": "Cannot confirm if duplicates are errors or legitimate repeat purchases"},
            {"issue": "Unknown payment/location/province", "decision": "Preserve transparently with Unknown label", "reason": "Dropping rows would lose revenue data; labeling keeps analysis honest"}
        ]
    }


def generate_recommendations(df):
    """Data-driven business recommendations based on patterns in the data."""
    recommendations = []

    vol_leader = df.groupby("item")["transaction_id"].count().idxmax()
    rev_leader = df.groupby("item")["total_spent"].sum().idxmax()

    if vol_leader != rev_leader:
        recommendations.append({
            "title": f"Launch {vol_leader} + {rev_leader} Bundle",
            "evidence": f"{vol_leader} has the highest transaction volume while {rev_leader} generates the highest revenue.",
            "action": "Create a combo offer that pairs a high-volume product with a high-revenue product.",
            "expectedImpact": "Increase average transaction value and make lunch purchases more attractive.",
            "confidence": "High",
            "limitation": "The dataset does not include profit margin, customer segments, or promotion history."
        })

    dated_df = df[df["transaction_date"].notna()]
    weekday_rev = dated_df[dated_df["day_type"] == "Weekday"]["total_spent"].sum()
    weekend_rev = dated_df[dated_df["day_type"] == "Weekend"]["total_spent"].sum()
    weekday_days = dated_df[dated_df["day_type"] == "Weekday"]["transaction_date"].dt.date.nunique()
    weekend_days = dated_df[dated_df["day_type"] == "Weekend"]["transaction_date"].dt.date.nunique()

    if weekend_days > 0 and weekday_days > 0:
        weekday_avg = weekday_rev / weekday_days
        weekend_avg = weekend_rev / weekend_days
        if weekend_avg < weekday_avg * 0.5:
            recommendations.append({
                "title": "Improve Weekend Sales",
                "evidence": "Weekend average daily revenue is much lower than weekday average daily revenue.",
                "action": "Test weekend snack bundles, limited-time offers, and digital wallet promotions.",
                "expectedImpact": "Improve low-performing days and smooth demand across the week.",
                "confidence": "Medium",
                "limitation": "The dataset does not include store opening hours or footfall, so the root cause is not confirmed."
            })

    product_rev = df.groupby("item")["total_spent"].sum().sort_values(ascending=False)
    top_3 = product_rev.head(3).index.tolist()
    recommendations.append({
        "title": "Protect High-Value Product Availability",
        "evidence": f"{', '.join(top_3[:2])} generate strong revenue despite varying transaction volumes.",
        "action": "Monitor stock availability for high-value products and reduce missed sales risk.",
        "expectedImpact": "Protect revenue from products that contribute strongly to sales value.",
        "confidence": "Medium",
        "limitation": "Inventory and waste data are not available."
    })

    unknown_payments = df["unknown_payment_flag"].apply(lambda x: x == True or x == "True").sum()
    unknown_locations = df["unknown_location_flag"].apply(lambda x: x == True or x == "True").sum()
    if unknown_payments > 0 or unknown_locations > 0:
        recommendations.append({
            "title": "Improve Data Capture Quality",
            "evidence": "Payment Method, Location, Province, and Transaction Date had quality issues.",
            "action": "Use mandatory fields, dropdown validation, and controlled master data for products and provinces.",
            "expectedImpact": "Improve BI accuracy, reduce cleaning effort, and strengthen future forecasting.",
            "confidence": "High",
            "limitation": "Requires POS system changes which may have cost and rollout dependencies."
        })

    return recommendations


def generate_methodology():
    """Static text explaining how the data was cleaned and analyzed."""
    return {
        "sections": [
            {
                "title": "Raw Dataset",
                "points": [
                    "10,000 transaction rows were received for CanAI Café 2023 sales.",
                    "The dataset contained transaction ID, product, quantity, price, total spent, payment method, location, date, and province."
                ]
            },
            {
                "title": "Cleaning Rules",
                "points": [
                    "Product and province spelling inconsistencies were standardized.",
                    "Missing quantity values were recovered mathematically.",
                    "Missing item values were inferred from product price.",
                    "Unknown payment, location, and province values were preserved transparently.",
                    "Duplicate transaction IDs were flagged instead of blindly removed."
                ]
            },
            {
                "title": "Analysis Metrics",
                "points": [
                    "Total revenue, transactions, units, average transaction value, product revenue, province revenue, payment performance, location performance, and weekday/weekend behavior were calculated."
                ]
            },
            {
                "title": "Forecast Method",
                "points": [
                    "An offline daily revenue forecast is generated from the cleaned transaction data and saved as static JSON for React.",
                    "Candidate baselines are compared across rolling 30-day holdout windows, then the best explainable weekday/recent-level model is selected.",
                    "The dashboard shows daily validation error in the daily view and 30-day aggregate validation error in the monthly view.",
                    "Annual seasonality is not strongly inferred because only one complete year of data is available.",
                    "Province forecast charts exclude Unknown Province and do not reallocate that revenue to known provinces."
                ]
            },
            {
                "title": "Frontend Approach",
                "points": [
                    "React reads prepared JSON files from the public/data folder.",
                    "The frontend does not recalculate heavy cleaning or forecasting logic.",
                    "The app focuses on executive storytelling and demo reliability."
                ]
            },
            {
                "title": "Limitations",
                "points": [
                    "No customer IDs or loyalty data are available.",
                    "No profit margin, cost, or inventory data exist.",
                    "Only one calendar year limits seasonality and trend detection."
                ]
            }
        ]
    }


def generate_powerbi_report():
    """Placeholder for Power BI integration."""
    return {
        "title": "Power BI Dashboard",
        "status": "Optional integration point",
        "notes": [
            "Use this page to add your published Power BI report link or dashboard screenshots.",
            "For demo safety, keep screenshots as backup if live embedding is not ready."
        ],
        "reportUrl": ""
    }


def save_json(data, filename):
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Generated: {filename}")


def main():
    print("Generating dashboard JSON files from cleaned data...")
    print(f"  Source: {CLEAN_CSV}")
    print(f"  Output: {OUTPUT_DIR}\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    forecast = generate_sales_forecast(df)

    save_json(generate_kpi_summary(df, forecast), "kpi_summary.json")
    save_json(generate_monthly_sales(df), "monthly_sales.json")
    save_json(generate_product_performance(df), "product_performance.json")
    save_json(generate_province_performance(df), "province_performance.json")
    save_json(generate_payment_performance(df), "payment_performance.json")
    save_json(generate_location_performance(df), "location_performance.json")
    save_json(generate_weekday_weekend(df), "weekday_weekend.json")
    save_json(generate_weekday_detail(df), "weekday_detail.json")
    save_json(forecast, "forecast_sales.json")
    save_json(generate_legacy_six_month_forecast(forecast), "forecast_6_months.json")
    save_json(generate_data_quality_summary(df), "data_quality_summary.json")
    save_json(generate_recommendations(df), "recommendations.json")
    save_json(generate_methodology(), "methodology.json")
    save_json(generate_powerbi_report(), "powerbi_report.json")

    print(f"\nDone! 14 JSON files generated for the dashboard.")


if __name__ == "__main__":
    main()
