# CanAI Cafe Hackathon — Data Cleaning Project

This project cleans the **CanAI Cafe 2023 Sales Information** dataset for hackathon analysis, Power BI dashboarding, and six-month sales forecasting.

The project is designed to be simple, explainable, and GitHub-ready.

---

## Project Structure

```text
canai-cafe-hackathon/
├── data/
│   ├── raw/
│   │   └── CanAI Cafe 2023 Sales Information.xlsx
│   └── processed/
│       ├── clean_output.csv
│       ├── cleaning_summary.csv
│       ├── profile_report.txt
│       └── rejected_rows.csv
├── scripts/
│   ├── dataset_cleaner.py
│   ├── dataset_profiler.py
│   └── run_all.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Complete Pipeline

From the project root folder:

```bash
python scripts/run_all.py
```

This runs:

1. `dataset_cleaner.py`
2. `dataset_profiler.py`

---

## Run Individual Scripts

### Clean the dataset

```bash
python scripts/dataset_cleaner.py
```

### Profile raw and cleaned data

```bash
python scripts/dataset_profiler.py
```

---

## Output Files

| File | Purpose |
|---|---|
| `data/processed/clean_output.csv` | Final cleaned dataset for Power BI / analysis |
| `data/processed/cleaning_summary.csv` | Cleaning metrics and audit summary |
| `data/processed/profile_report.txt` | Raw and cleaned data profile report |
| `data/processed/rejected_rows.csv` | Rows rejected after numeric validation, if any |
<<<<<<< HEAD
| `canai-cafe-frontend-project/frontend/public/data/forecast_sales.json` | Static 180-day forecast payload for the React dashboard |
=======
>>>>>>> origin/feature/setup-frontend-dashboard

---

## Cleaning Decisions

### 1. Column names

Original column names are converted to snake_case.

Example:

```text
Transaction ID → transaction_id
Price Per Unit → price_per_unit
Total Spent → total_spent
```

---

### 2. Item standardization

Dirty product names are standardized.

Examples:

| Dirty Value | Clean Value |
|---|---|
| `cofee`, `coffe`, `c0ffee` | Coffee |
| `tee`, `TEA` | Tea |
| `donutt`, `doughnut` | Donut |
| `sandwhich` | Sandwich |
| `juic`, `juicee` | Juice |

Missing item values are inferred from `price_per_unit` because price uniquely identifies product in this dataset.

---

### 3. Numeric repair

The cleaner repairs numeric fields before filtering invalid rows.

This is important because missing quantity can be recovered using:

```text
quantity = total_spent / price_per_unit
```

The previous issue was that rows with missing quantity were removed before repair. This version fixes that.

---

### 4. Payment method cleaning

Valid payment methods are:

```text
Cash
Credit Card
Digital Wallet
```

Invalid or missing values are set to:

```text
Unknown Payment
```

This is better than hiding blanks or guessing the most common payment method.

---

### 5. Location cleaning

Valid locations are:

```text
In-store
Takeaway
```

Missing or invalid values are set to:

```text
Unknown Location
```

---

### 6. Province cleaning

Province values are standardized into:

```text
British Columbia
Manitoba
Newfoundland and Labrador
Ontario
Saskatchewan
Unknown Province
```

The script uses **Newfoundland and Labrador** as the final province name instead of only `Newfoundland`.

---

### 7. Date handling

Unknown or invalid dates remain missing.

For business analysis:

- Use all rows for total revenue, product, payment, province, and location analysis.
- Use only rows with valid `transaction_date` for monthly trend and forecasting.

The cleaner also creates:

```text
transaction_month
weekday_name
day_type
missing_date_flag
```

---

### 8. Duplicate transaction IDs

Duplicate transaction IDs are not blindly deleted.

Instead, the cleaner creates:

```text
duplicate_transaction_id_flag
```

Reason: duplicate IDs may not be exact duplicate rows. Deleting them blindly can cause revenue loss.

---

<<<<<<< HEAD
## Forecasting Methodology

The sales forecast is built ahead of time in Python and saved as static JSON:

```text
canai-cafe-frontend-project/frontend/public/data/forecast_sales.json
```

### What The Forecast Predicts

The model predicts expected cafe revenue for the next 180 calendar days after
the final transaction date in the cleaned dataset:

```text
2024-01-01 through 2024-06-28
```

The forecast is created one day at a time. The dashboard then groups those
daily forecasts into monthly totals for the 6-month view.

### How The Model Learns From The Data

The cleaned dataset has one year of dated sales history. That is enough to
learn simple daily patterns, but not enough to confidently learn annual
seasonality. Because of that, the model focuses on patterns that are easier to
defend:

- how much revenue the cafe has made recently
- whether a forecast date is a weekday or weekend
- whether daily sales have been drifting slightly up or down

The pipeline compares a few simple forecasting options:

- Use the recent average daily revenue.
- Use recent averages for each weekday.
- Use a small day-of-week regression model.
- Blend the regression model with recent weekday averages.

The selected model is the one that performs best during back-testing. The
current selected model is:

```text
Day-of-week regression blended with recent level
```

This means the forecast uses a stable weekday pattern from the full year, then
blends it with more recent sales behavior so the forecast is not stuck in the
past.

### How The Model Is Checked

The pipeline does not just create future numbers and hope they look right. It
tests the model against known historical data.

It does this by hiding three recent 30-day periods from the model, predicting
those periods, and comparing the predictions with what actually happened. This
is called back-testing.

The dashboard shows the result in plain business terms:

- In the 30-day daily view, `Typical Daily Error` shows the average daily miss
  during back-testing.
- In the 6-month monthly view, `Typical Monthly Error` shows the average
  30-day total-revenue miss during back-testing.

The monthly error is not calculated by multiplying daily error by 30. Instead,
it compares each hidden 30-day period's total predicted revenue against its
actual total revenue. This is more realistic because daily over-predictions and
under-predictions can cancel out across a month.

### How The Breakdowns Work

The model first forecasts total revenue. Then it creates supporting breakdowns
for the dashboard.

Item breakdowns:

- Forecast item revenue is allocated from the total revenue forecast using
  historical item sales mix.
- Item revenue adds back up to the selected forecast total.
- Expected item units are estimated from forecast item revenue and each item's
  median cleaned price.
- Units are rounded to whole numbers because they are planning estimates.

Province breakdowns:

- `Unknown Province` is excluded from the visible province chart.
- That unknown revenue is not redistributed to known provinces.
- Because of this, the visible province bars intentionally do not add up to the
  total forecast revenue.

### Important Limits

- Rows with missing transaction dates are excluded from time-based model
  training.
- The dataset has one year of history, so the model avoids strong annual
  seasonality claims.
- The dataset does not include promotions, weather, foot traffic, store hours,
  inventory, customer IDs, or profit margins.
- Lower and upper forecast estimates are planning ranges based on historical
  back-test error, not guaranteed confidence intervals.

The forecast should be read as a planning baseline: useful for understanding
expected direction, scale, and mix, but not a guarantee of future sales.

---

=======
>>>>>>> origin/feature/setup-frontend-dashboard
## Key Cleaning Results From Current Dataset

| Metric | Value |
|---|---:|
| Original rows | 10,000 |
| Cleaned rows | 10,000 |
| Rejected rows | 0 |
| Missing / invalid dates | 240 |
| Missing item inferred from price | 100 |
| Quantity repaired | 98 |
| Unknown payment rows | 555 |
| Unknown location rows | 878 |
| Unknown province rows | 417 |
| Duplicate transaction ID rows flagged | 88 |
| Revenue mismatch rows | 0 |
| Total cleaned revenue | 86,288.00 |

---

## Recommended Power BI Usage

Use `data/processed/clean_output.csv` as the main Power BI source.

Recommended dashboard pages:

1. Executive Overview
2. Data Quality Summary
3. Product Performance
4. Regional Performance
5. Payment and Location Analysis
6. Monthly Trend and Forecast

Important filters/slicers:

```text
item
province
payment_method
location
transaction_month
day_type
```

---

## GitHub Push Commands

From inside the project folder:

```bash
git init
git add .
git commit -m "Initial CanAI Cafe data cleaning project"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

Replace `<your-github-repo-url>` with your actual GitHub repository URL.

---

## Notes

This project intentionally keeps unknown values visible instead of silently removing them. That makes the final dashboard and presentation more honest and professional.
