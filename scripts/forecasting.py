"""
Offline sales forecasting for the CanAI Cafe dashboard.

This module turns the cleaned transaction dataset into a static JSON payload
that the React dashboard can load directly.

High-level workflow:

1. Aggregate valid dated transactions into one revenue value per calendar day.
2. Compare a few simple, explainable forecasting candidates with rolling
   holdout windows from the end of 2023.
3. Forecast exactly 180 days after the last historical transaction date.
4. Aggregate those daily forecasts into monthly rows for the dashboard toggle.
5. Allocate the top-level revenue forecast into item and province breakdowns.
6. Return a dashboard-friendly dictionary that can be written as JSON.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


UNKNOWN_PROVINCE = "Unknown Province"
FORECAST_DAYS = 180
FIRST_WINDOW_DAYS = 30

# Ridge penalty for the regression candidate
RIDGE_ALPHA = 8.0


@dataclass(frozen=True)
class Candidate:
    """A forecast option that can be trained on history and score holdout dates."""

    key: str
    label: str
    predictor: Callable[[pd.DataFrame, pd.Series], np.ndarray]


def _round_money(value: float) -> float:
    return round(float(value), 2)


def _round_number(value: float, digits: int = 1) -> float:
    return round(float(value), digits)


def _date_label(value: pd.Timestamp) -> str:
    return f"{value.strftime('%b')} {value.day}"


def _month_label(period: pd.Period) -> str:
    return period.to_timestamp().strftime("%b %Y")


def _day_type(value: pd.Timestamp) -> str:
    return "Weekday" if value.dayofweek < 5 else "Weekend"


def _as_daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert transaction-level data into daily model input.

    Forecast models need one target value at a consistent time grain. The
    cleaned source data is transaction-level, so we aggregate `total_spent` by
    day. Rows without a valid `transaction_date` are excluded because they
    cannot be placed on the time axis, but their revenue remains available to
    other non-time-series dashboard KPIs.

    Reindexing to the full date range makes any missing calendar day explicit.
    In the current dataset all 365 days exist, but keeping this guard makes the
    workflow safer if the source file changes.
    """
    dated = df[df["transaction_date"].notna()].copy()
    daily = (
        dated.groupby(dated["transaction_date"].dt.normalize())["total_spent"]
        .sum()
        .rename("revenue")
        .reset_index()
        .rename(columns={"transaction_date": "date"})
        .sort_values("date")
    )

    full_dates = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
    daily = (
        daily.set_index("date")
        .reindex(full_dates, fill_value=0)
        .rename_axis("date")
        .reset_index()
    )
    daily["weekday"] = daily["date"].dt.dayofweek
    return daily


def _ridge_design(dates: pd.Series, origin: pd.Timestamp) -> np.ndarray:
    """
    Build simple calendar features for the regression candidate.

    The design matrix deliberately stays small:
    - intercept: the baseline daily revenue level
    - light trend: allows the year to drift upward/downward
    - weekday indicators: captures weekday/weekend behavior

    There are no month dummies or annual Fourier terms because one year of data
    is not enough to prove recurring annual seasonality.
    """
    dates = pd.to_datetime(dates)
    trend = ((dates - origin).dt.days / 365.0).to_numpy(dtype=float)
    weekday = dates.dt.dayofweek.to_numpy()
    columns = [np.ones(len(dates)), trend]
    columns.extend((weekday == day).astype(float) for day in range(1, 7))
    return np.column_stack(columns)


def _predict_ridge_weekday_trend(train: pd.DataFrame, target_dates: pd.Series) -> np.ndarray:
    """
    Predict with a small ridge regression built from numpy.

    Ridge regularization is used because the dataset is small and hackathon
    friendly; it keeps coefficients from chasing noise while avoiding an extra
    dependency such as scikit-learn.
    """
    origin = train["date"].min()
    x_train = _ridge_design(train["date"], origin)
    y_train = train["revenue"].to_numpy(dtype=float)
    penalty = np.eye(x_train.shape[1]) * RIDGE_ALPHA
    penalty[0, 0] = 0
    coefficients = np.linalg.solve(x_train.T @ x_train + penalty, x_train.T @ y_train)
    predictions = _ridge_design(target_dates, origin) @ coefficients
    return np.clip(predictions, 0, None)


def _predict_trailing_mean(train: pd.DataFrame, target_dates: pd.Series) -> np.ndarray:
    """
    Naive baseline: assume the recent average daily revenue continues.

    This is intentionally simple. A forecasting workflow should beat a plain
    average before it claims to add value.
    """
    recent = train.tail(min(60, len(train)))
    prediction = recent["revenue"].mean()
    return np.full(len(target_dates), max(prediction, 0), dtype=float)


def _predict_recent_weekday_level(train: pd.DataFrame, target_dates: pd.Series) -> np.ndarray:
    """
    Baseline that preserves recent day-of-week behavior.

    Cafe sales can differ meaningfully between weekdays and weekends. This
    candidate uses the last 90 days so it responds to recent level changes
    without depending on annual seasonality.
    """
    recent = train.tail(min(90, len(train))).copy()
    fallback = recent["revenue"].mean()
    weekday_means = recent.groupby("weekday")["revenue"].mean().to_dict()
    predictions = [
        weekday_means.get(date.dayofweek, fallback)
        for date in pd.to_datetime(target_dates)
    ]
    return np.clip(np.array(predictions, dtype=float), 0, None)


def _predict_blended_weekday_model(train: pd.DataFrame, target_dates: pd.Series) -> np.ndarray:
    """
    Blend structural weekday regression with recent weekday level.

    The regression gives a stable full-year weekday pattern; the recent weekday
    baseline keeps the forecast grounded in the latest sales level. The fixed
    60/40 blend is simple enough to explain and is validated against holdouts
    rather than tuned on a large search space.
    """
    ridge = _predict_ridge_weekday_trend(train, target_dates)
    recent = _predict_recent_weekday_level(train, target_dates)
    return np.clip((ridge * 0.6) + (recent * 0.4), 0, None)


def _evaluate_candidates(daily: pd.DataFrame) -> Tuple[Candidate, Dict[str, object]]:
    """
    Pick the best candidate using rolling holdout windows.

    We score each candidate on three 30-day periods near the end of the
    historical year. This mimics the real task: train on earlier data and
    predict future days. A single split can be lucky or unlucky, so rolling
    windows give a more balanced read while staying easy to audit.

    The returned validation object includes:
    - daily MAE/RMSE/MAPE for the daily dashboard view
    - 30-day aggregate MAE/RMSE/MAPE for the monthly dashboard view
    - per-window actual and predicted totals for traceability
    """
    candidates = [
        Candidate("trailing_mean", "Trailing daily average", _predict_trailing_mean),
        Candidate("recent_weekday", "Recent weekday-level baseline", _predict_recent_weekday_level),
        Candidate("weekday_trend", "Day-of-week ridge regression", _predict_ridge_weekday_trend),
        Candidate("weekday_trend_blend", "Day-of-week regression blended with recent level", _predict_blended_weekday_model),
    ]

    validation_length = 30
    starts = [len(daily) - 90, len(daily) - 60, len(daily) - 30]
    windows = []
    scores = {}

    for candidate in candidates:
        actual_values = []
        predicted_values = []
        candidate_windows = []
        period_actuals = []
        period_predictions = []

        for start in starts:
            train = daily.iloc[:start].copy()
            holdout = daily.iloc[start:start + validation_length].copy()
            predictions = candidate.predictor(train, holdout["date"])
            actual = holdout["revenue"].to_numpy(dtype=float)
            errors = actual - predictions
            actual_total = float(actual.sum())
            predicted_total = float(predictions.sum())
            period_error = actual_total - predicted_total

            actual_values.extend(actual.tolist())
            predicted_values.extend(predictions.tolist())
            period_actuals.append(actual_total)
            period_predictions.append(predicted_total)
            candidate_windows.append({
                "startDate": holdout["date"].min().strftime("%Y-%m-%d"),
                "endDate": holdout["date"].max().strftime("%Y-%m-%d"),
                "mae": _round_money(np.mean(np.abs(errors))),
                "rmse": _round_money(np.sqrt(np.mean(errors ** 2))),
                "actualRevenue": _round_money(actual_total),
                "predictedRevenue": _round_money(predicted_total),
                "periodError": _round_money(period_error),
                "absolutePeriodError": _round_money(abs(period_error)),
            })

        actual_arr = np.array(actual_values)
        predicted_arr = np.array(predicted_values)
        period_actual_arr = np.array(period_actuals)
        period_predicted_arr = np.array(period_predictions)
        errors = actual_arr - predicted_arr
        period_errors = period_actual_arr - period_predicted_arr
        scores[candidate.key] = {
            "label": candidate.label,
            "mae": _round_money(np.mean(np.abs(errors))),
            "rmse": _round_money(np.sqrt(np.mean(errors ** 2))),
            "mape": _round_number(np.mean(np.abs(errors) / np.maximum(actual_arr, 1)) * 100, 2),
            "monthlyMae": _round_money(np.mean(np.abs(period_errors))),
            "monthlyRmse": _round_money(np.sqrt(np.mean(period_errors ** 2))),
            "monthlyMape": _round_number(np.mean(np.abs(period_errors) / np.maximum(period_actual_arr, 1)) * 100, 2),
            "windows": candidate_windows,
        }

    # Select by daily MAE because the model's base unit is daily revenue. The
    # monthly metric is still reported so the monthly UI can show period-level
    # validation instead of a daily statistic.
    selected = min(candidates, key=lambda item: scores[item.key]["mae"])
    selected_score = scores[selected.key]
    windows = selected_score["windows"]

    return selected, {
        "selectedCandidate": selected.key,
        "selectedModel": selected.label,
        "mae": selected_score["mae"],
        "rmse": selected_score["rmse"],
        "mape": selected_score["mape"],
        "monthlyMae": selected_score["monthlyMae"],
        "monthlyRmse": selected_score["monthlyRmse"],
        "monthlyMape": selected_score["monthlyMape"],
        "holdoutWindows": windows,
        "candidateScores": scores,
        "validationNote": "Compared simple baselines across three rolling 30-day holdout windows from late 2023.",
        "monthlyValidationNote": "Monthly error is the average absolute total-revenue miss across those 30-day holdout windows.",
    }


def _build_share_lookup(df: pd.DataFrame, dimension: str) -> Dict[str, object]:
    """
    Learn historical revenue shares for a breakdown dimension.

    The main model forecasts total revenue only. This helper prepares the
    historical mix needed to allocate that total into items or provinces for
    dashboard charts.

    Shares are stored at three fallback levels:
    - month + day type, if available
    - day type only
    - overall mix

    This keeps breakdowns sensitive to broad calendar context without fitting
    separate noisy models for every product/province segment.
    """
    dated = df[df["transaction_date"].notna()].copy()
    dated["month_num"] = dated["transaction_date"].dt.month
    dated["forecast_day_type"] = dated["transaction_date"].apply(_day_type)

    names = (
        dated.groupby(dimension)["total_spent"]
        .sum()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    def shares_for(frame: pd.DataFrame) -> Dict[str, float]:
        totals = frame.groupby(dimension)["total_spent"].sum()
        total = totals.sum()
        if total <= 0:
            return {name: 0 for name in names}
        return {name: float(totals.get(name, 0) / total) for name in names}

    overall = shares_for(dated)
    by_day_type = {
        day_type: shares_for(frame)
        for day_type, frame in dated.groupby("forecast_day_type")
    }
    by_month_day_type = {
        (int(month), day_type): shares_for(frame)
        for (month, day_type), frame in dated.groupby(["month_num", "forecast_day_type"])
    }

    return {
        "names": names,
        "overall": overall,
        "byDayType": by_day_type,
        "byMonthDayType": by_month_day_type,
    }


def _lookup_shares(lookup: Dict[str, object], date: pd.Timestamp) -> Dict[str, float]:
    """Return the best available historical mix for one forecast date."""
    key = (int(date.month), _day_type(date))
    by_month_day_type = lookup["byMonthDayType"]
    if key in by_month_day_type:
        return by_month_day_type[key]

    by_day_type = lookup["byDayType"]
    if _day_type(date) in by_day_type:
        return by_day_type[_day_type(date)]

    return lookup["overall"]


def _weighted_period_shares(
    rows: List[Dict[str, object]],
    lookup: Dict[str, object],
) -> Dict[str, float]:
    """
    Combine daily shares into one selected-period share.

    Dashboard breakdowns can represent a single day, the first 30 days, one
    month, or the full 180-day horizon. A simple average of daily shares would
    over-weight small revenue days, so this function weights each day's mix by
    that day's forecast revenue.
    """
    totals = {name: 0.0 for name in lookup["names"]}
    total_revenue = sum(float(row["forecastRevenue"]) for row in rows)

    if total_revenue <= 0:
        return lookup["overall"]

    for row in rows:
        date = pd.Timestamp(row["date"])
        revenue = float(row["forecastRevenue"])
        shares = _lookup_shares(lookup, date)
        for name in totals:
            totals[name] += revenue * shares.get(name, 0)

    return {name: amount / total_revenue for name, amount in totals.items()}


def _allocate_revenue(total: float, shares: Dict[str, float], names: Iterable[str]) -> Dict[str, float]:
    """
    Allocate a period total across named categories.

    Money is rounded to cents for JSON/UI display. The final rounding penny is
    applied to the largest category so item revenue totals still reconcile to
    the selected forecast total.
    """
    names = list(names)
    raw = {name: max(total * shares.get(name, 0), 0) for name in names}
    rounded = {name: _round_money(value) for name, value in raw.items()}
    difference = _round_money(total - sum(rounded.values()))

    if names and abs(difference) >= 0.01:
        largest = max(names, key=lambda name: raw[name])
        rounded[largest] = _round_money(rounded[largest] + difference)

    return rounded


def _sorted_records(values: Dict[str, float], total: float, value_key: str = "revenue") -> List[Dict[str, object]]:
    """Format category values as sorted chart records with share-of-total text."""
    records = []
    for name, value in sorted(values.items(), key=lambda item: item[1], reverse=True):
        records.append({
            "name": name,
            value_key: _round_money(value),
            "shareOfTotalRevenue": _round_number((value / total * 100) if total else 0, 2),
        })
    return records


def _period_breakdown(
    rows: List[Dict[str, object]],
    item_lookup: Dict[str, object],
    province_lookup: Dict[str, object],
    item_prices: Dict[str, float],
) -> Dict[str, object]:
    """
    Build all supporting charts for a selected forecast period.

    Item behavior:
    - item revenue is allocated from total forecast revenue
    - item totals reconcile to the selected period total
    - units are estimated from item revenue / median cleaned item price

    Province behavior:
    - Unknown Province is calculated but excluded from visible province bars
    - known province bars are not renormalized
    - therefore visible province revenue is intentionally less than total
      forecast revenue whenever Unknown Province has a share
    """
    total = _round_money(sum(float(row["forecastRevenue"]) for row in rows))
    days = len(rows)

    item_shares = _weighted_period_shares(rows, item_lookup)
    item_revenue_map = _allocate_revenue(total, item_shares, item_lookup["names"])
    item_revenue = _sorted_records(item_revenue_map, total)

    item_units = []
    for item in item_revenue:
        price = item_prices.get(item["name"], 1)
        units = float(item["revenue"]) / price if price else 0
        item_units.append({
            "name": item["name"],
            "units": int(round(units)),
            "revenue": item["revenue"],
        })

    province_shares = _weighted_period_shares(rows, province_lookup)
    province_revenue_map = _allocate_revenue(total, province_shares, province_lookup["names"])
    unknown_revenue = _round_money(province_revenue_map.get(UNKNOWN_PROVINCE, 0))
    known_province_map = {
        name: value
        for name, value in province_revenue_map.items()
        if name != UNKNOWN_PROVINCE
    }
    province_revenue = _sorted_records(known_province_map, total)
    known_total = _round_money(sum(known_province_map.values()))

    return {
        "totalRevenue": total,
        "days": days,
        "averageDailyRevenue": _round_money(total / days) if days else 0,
        "itemRevenue": item_revenue,
        "itemUnits": item_units,
        "provinceRevenue": province_revenue,
        "knownProvinceRevenue": known_total,
        "excludedProvince": {
            "name": UNKNOWN_PROVINCE,
            "revenue": unknown_revenue,
            "shareOfTotalRevenue": _round_number((unknown_revenue / total * 100) if total else 0, 2),
            "note": "Excluded from visible province chart and not reallocated to known provinces.",
        },
    }


def _summary(rows: List[Dict[str, object]], label: str) -> Dict[str, object]:
    """Create KPI-ready totals for a forecast window."""
    total = _round_money(sum(float(row["forecastRevenue"]) for row in rows))
    lower = _round_money(sum(float(row["lowerEstimate"]) for row in rows))
    upper = _round_money(sum(float(row["upperEstimate"]) for row in rows))
    days = len(rows)
    return {
        "label": label,
        "days": days,
        "startDate": rows[0]["date"],
        "endDate": rows[-1]["date"],
        "expectedRevenue": total,
        "lowerEstimate": lower,
        "upperEstimate": upper,
        "averageDailyRevenue": _round_money(total / days) if days else 0,
    }


def _historical_comparison(
    daily: pd.DataFrame,
    forecast_rows: List[Dict[str, object]],
    window_days: int,
    label: str,
) -> Dict[str, object]:
    """
    Compare forecast revenue against the same number of recent historical days.

    This gives non-technical users a quick anchor: is the forecast higher or
    lower than recent business performance, and by roughly how much?
    """
    history = daily.tail(window_days)
    forecast_window = forecast_rows[:window_days]
    historical_total = _round_money(history["revenue"].sum())
    forecast_total = _round_money(sum(float(row["forecastRevenue"]) for row in forecast_window))
    difference = _round_money(forecast_total - historical_total)
    return {
        "label": label,
        "historicalStartDate": history["date"].min().strftime("%Y-%m-%d"),
        "historicalEndDate": history["date"].max().strftime("%Y-%m-%d"),
        "historicalRevenue": historical_total,
        "forecastRevenue": forecast_total,
        "difference": difference,
        "percentChange": _round_number((difference / historical_total * 100) if historical_total else 0, 2),
        "historicalAverageDailyRevenue": _round_money(historical_total / window_days),
        "forecastAverageDailyRevenue": _round_money(forecast_total / window_days),
    }


def _build_monthly_forecast(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """
    Aggregate daily forecasts into month rows for the six-month dashboard view.

    The model itself stays daily. Monthly rows are derived from those daily
    outputs so daily and monthly views always agree. June is marked partial
    because the exact 180-day horizon ends on 2024-06-28.
    """
    frame = pd.DataFrame(rows)
    frame["date"] = pd.to_datetime(frame["date"])
    frame["month"] = frame["date"].dt.to_period("M")
    monthly = []

    for period, month_rows in frame.groupby("month"):
        start = month_rows["date"].min()
        end = month_rows["date"].max()
        days = len(month_rows)
        full_days = period.days_in_month
        monthly.append({
            "month": str(period),
            "label": _month_label(period),
            "startDate": start.strftime("%Y-%m-%d"),
            "endDate": end.strftime("%Y-%m-%d"),
            "days": int(days),
            "isPartial": bool(days < full_days),
            "forecastRevenue": _round_money(month_rows["forecastRevenue"].sum()),
            "lowerEstimate": _round_money(month_rows["lowerEstimate"].sum()),
            "upperEstimate": _round_money(month_rows["upperEstimate"].sum()),
            "planningNote": "Partial month" if days < full_days else "Full month",
        })

    return monthly


def generate_sales_forecast(df: pd.DataFrame) -> Dict[str, object]:
    """
    Create the complete static forecast payload consumed by the dashboard.

    This is the public entry point used by `generate_dashboard_data.py`. It
    returns only plain Python containers so `json.dump` can write the result
    without a custom serializer.
    """
    daily = _as_daily_revenue(df)
    selected, validation = _evaluate_candidates(daily)

    # Anchor the horizon to the data, not the machine's current date. This
    # makes the output reproducible for demos and tests.
    last_date = daily["date"].max()
    forecast_dates = pd.Series(pd.date_range(last_date + timedelta(days=1), periods=FORECAST_DAYS, freq="D"))
    point_forecast = selected.predictor(daily, forecast_dates)

    # The interval is a planning range based on validation residuals. It is
    # intentionally described as an estimate, not a formal confidence interval.
    residual_scale = max(float(validation["rmse"]), 1.0)
    interval_width = 1.28 * residual_scale

    daily_forecast = []
    for date, forecast in zip(forecast_dates, point_forecast):
        expected = _round_money(forecast)
        daily_forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "label": _date_label(date),
            "periodKey": date.strftime("%Y-%m-%d"),
            "dayType": _day_type(date),
            "forecastRevenue": expected,
            "lowerEstimate": _round_money(max(expected - interval_width, 0)),
            "upperEstimate": _round_money(expected + interval_width),
        })

    monthly_forecast = _build_monthly_forecast(daily_forecast)

    # Build breakdown mix lookups once, then reuse them for every selectable
    # day/month/window that the frontend needs.
    item_lookup = _build_share_lookup(df, "item")
    province_lookup = _build_share_lookup(df, "province")
    item_prices = (
        df[df["item"].notna()]
        .groupby("item")["price_per_unit"]
        .median()
        .to_dict()
    )

    first_30_rows = daily_forecast[:FIRST_WINDOW_DAYS]
    full_rows = daily_forecast
    month_rows = {
        month["month"]: [
            row for row in daily_forecast
            if row["date"] >= month["startDate"] and row["date"] <= month["endDate"]
        ]
        for month in monthly_forecast
    }

    breakdowns = {
        "windows": {
            "first30": _period_breakdown(first_30_rows, item_lookup, province_lookup, item_prices),
            "full180": _period_breakdown(full_rows, item_lookup, province_lookup, item_prices),
        },
        "days": {
            row["date"]: _period_breakdown([row], item_lookup, province_lookup, item_prices)
            for row in daily_forecast
        },
        "months": {
            month: _period_breakdown(rows, item_lookup, province_lookup, item_prices)
            for month, rows in month_rows.items()
        },
    }

    # Summary and comparison blocks are shaped for KPI cards, so the React page
    # does not need to recalculate business logic from raw forecast rows.
    summaries = {
        "first30Days": _summary(first_30_rows, "First 30 forecast days"),
        "full180Days": _summary(full_rows, "Full 180-day forecast"),
    }
    comparisons = {
        "recent30Days": _historical_comparison(daily, daily_forecast, 30, "Compared with latest 30 historical days"),
        "recent180Days": _historical_comparison(daily, daily_forecast, 180, "Compared with latest 180 historical days"),
    }

    total_forecast = summaries["full180Days"]["expectedRevenue"]

    return {
        "modelName": validation["selectedModel"],
        "modelType": "Offline explainable daily revenue forecast",
        "forecastPeriod": f"{daily_forecast[0]['date']} to {daily_forecast[-1]['date']}",
        "totalForecastRevenue": total_forecast,
        "horizon": {
            "startDate": daily_forecast[0]["date"],
            "endDate": daily_forecast[-1]["date"],
            "days": FORECAST_DAYS,
            "monthlyViewNote": "June 2024 is a partial forecast month because the horizon is exactly 180 days.",
        },
        "trainingData": {
            "startDate": daily["date"].min().strftime("%Y-%m-%d"),
            "endDate": daily["date"].max().strftime("%Y-%m-%d"),
            "dailyObservations": int(len(daily)),
            "datedRows": int(df["transaction_date"].notna().sum()),
            "missingDateRowsExcluded": int(df["transaction_date"].isna().sum()),
        },
        "validation": validation,
        "summaryMetrics": summaries,
        "comparisons": comparisons,
        "dailyForecast": daily_forecast,
        "monthlyForecast": monthly_forecast,
        "breakdowns": breakdowns,
        "assumptions": [
            "Only one complete historical year is available, so the model does not claim learned annual seasonality.",
            "Rows with missing transaction dates are excluded from time-series training but remain valid for non-time-based KPIs.",
            "The forecast is generated offline and saved as static JSON for the dashboard.",
            "Province charts exclude Unknown Province and do not reallocate that revenue to known provinces.",
        ],
        "limitations": [
            "The dataset does not include promotions, weather, footfall, store hours, inventory, customer IDs, or profit margins.",
            "Forecast intervals are planning ranges based on historical validation residuals, not guaranteed confidence intervals.",
            "Expected units are planning estimates derived from forecast item revenue and median cleaned item price.",
        ],
    }


def generate_legacy_six_month_forecast(forecast: Dict[str, object]) -> Dict[str, object]:
    """Compatibility payload for any stale references to the old file name."""
    return {
        "modelName": forecast["modelName"],
        "forecastPeriod": forecast["forecastPeriod"],
        "totalForecastRevenue": forecast["totalForecastRevenue"],
        "validation": forecast["validation"],
        "assumptions": forecast["assumptions"],
        "limitations": forecast["limitations"],
        "monthlyForecast": forecast["monthlyForecast"],
    }
