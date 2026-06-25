# CanAI Café Frontend Setup and Development Guide

## 1. Objective

This frontend is not a random React dashboard. It is the executive reporting layer for the CanAI Café Hackathon solution.

The app should help judges understand:

1. What was wrong with the dataset
2. What the team cleaned
3. What happened in 2023 sales
4. Which products and regions performed best
5. What the next six months may look like
6. What business actions CanAI Café should take
7. What limitations exist in the analysis

## 2. Recommended folder placement

Your current project already has:

```text
CafeAIHackthonSolution/
├── data/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
```

Extract the provided frontend folder into the same root:

```text
CafeAIHackthonSolution/
├── data/
├── scripts/
├── frontend/
├── .gitignore
├── README.md
└── requirements.txt
```

## 3. Frontend structure

```text
frontend/
├── public/
│   └── data/
│       ├── kpi_summary.json
│       ├── data_quality_summary.json
│       ├── monthly_sales.json
│       ├── product_performance.json
│       ├── province_performance.json
│       ├── payment_performance.json
│       ├── location_performance.json
│       ├── weekday_weekend.json
│       ├── weekday_detail.json
│       ├── forecast_6_months.json
│       ├── recommendations.json
│       ├── methodology.json
│       └── powerbi_report.json
│
├── src/
│   ├── components/
│   │   ├── layout/
│   │   ├── cards/
│   │   ├── charts/
│   │   └── common/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── package.json
├── vite.config.js
├── README.md
├── .env.example
└── .gitignore
```

## 4. Installation steps

Open VS Code terminal from your project root.

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the app:

```bash
npm run dev
```

Vite will show a local URL, usually:

```text
http://localhost:5173
```

Open that URL in the browser.

## 5. Required Node.js version

Use Node.js 18 or above.

Check your version:

```bash
node -v
npm -v
```

If Node is missing or old, install the latest LTS version from the official Node.js website.

## 6. Pages included

### 6.1 Executive Overview

Purpose: Give judges the complete business story quickly.

Includes:

- Total Revenue
- Total Transactions
- Units Sold
- Average Ticket
- Top Product
- Top Province
- Six-Month Forecast
- Data Quality Score
- Monthly Sales Trend
- Product Revenue Chart
- Province Revenue Chart
- Forecast Chart

### 6.2 Data Quality

Purpose: Prove that the team did real data cleaning.

Includes:

- Original rows
- Cleaned rows
- Rejected rows
- Quantity repaired
- Item inferred
- Unknown payment rows
- Unknown location rows
- Unknown province rows
- Duplicate ID rows flagged
- Missing date rows
- Cleaning decisions

### 6.3 Sales Performance

Purpose: Explain 2023 historical sales.

Includes:

- Best month
- Weakest month
- Monthly sales trend
- Weekday vs weekend revenue
- Average daily revenue by weekday

### 6.4 Product Intelligence

Purpose: Show product-level performance and opportunity.

Includes:

- Product revenue chart
- Product transaction chart
- Product ranking table
- Coffee + Sandwich bundle insight

### 6.5 Regional Intelligence

Purpose: Show province-level performance.

Includes:

- Revenue by province
- Province ranking table
- Unknown Province impact
- Honest interpretation for low-volume Ontario data

### 6.6 Forecast Center

Purpose: Present the six-month forecast clearly.

Includes:

- Model name
- Forecast period
- Total forecast revenue
- Validation metrics
- Forecast chart
- Forecast table
- Assumptions
- Limitations

### 6.7 Recommendations

Purpose: Convert analysis into action.

Includes recommendations for:

- Coffee + Sandwich bundle
- Weekend sales improvement
- High-value product availability
- Data capture quality
- Better future forecasting data

### 6.8 Methodology

Purpose: Help answer technical judging questions.

Explains:

- Raw dataset
- Cleaning rules
- Analysis metrics
- Forecast method
- Frontend approach
- Known limitations

### 6.9 Power BI

Purpose: Connect the React portal with the Power BI dashboard.

The page can:

- Show a Power BI link
- Embed a report if a public/secure link is available
- Act as a screenshot backup page

## 7. Updating frontend data

The app reads static JSON from:

```text
frontend/public/data
```

To update dashboard numbers, update the JSON files. No React code change is needed if the JSON shape stays the same.

Example KPI file:

```json
{
  "totalRevenue": 86288,
  "totalTransactions": 10000,
  "totalUnitsSold": 19853,
  "averageTransactionValue": 8.63,
  "topProduct": "Sandwich",
  "topProvince": "British Columbia",
  "sixMonthForecast": 43094.97,
  "dataQualityScore": 78.63
}
```

## 8. Power BI configuration

Create a `.env` file inside the `frontend` folder:

```text
VITE_POWERBI_REPORT_URL=https://your-powerbi-report-link
```

Restart the frontend:

```bash
npm run dev
```

If the Power BI link is not ready, the app still works. This is intentional for demo safety.

## 9. GitHub push instructions

From the project root:

```bash
git status
git add .
git commit -m "Add CanAI Cafe React intelligence portal"
git push
```

Do not commit:

- `frontend/node_modules`
- `frontend/dist`
- `.env`

The included `.gitignore` handles these.

## 10. Demo script

Use this flow during judging:

```text
We built the CanAI Café Intelligence Portal as the frontend reporting layer for business users.

First, the Executive Overview shows the main KPIs, product leaders, regional performance, and six-month forecast.

Second, the Data Quality page proves that we did not hide dirty data. We repaired recoverable values, labeled unknowns transparently, and flagged duplicate transaction IDs.

Third, the Sales, Product, and Regional pages explain what happened in 2023.

Fourth, the Forecast Center shows the Jan-Jun 2024 planning forecast with assumptions and limitations.

Finally, the Recommendation Board converts the analysis into business actions such as Coffee + Sandwich bundles, weekend sales improvement, and better data capture.
```

## 11. Senior developer notes

Keep the frontend stable.

Do not add unnecessary features before the demo:

- No login
- No database
- No live CSV editing
- No backend dependency
- No AI dependency
- No complex state library

This frontend is meant to be reliable, clean, and presentation-ready.
