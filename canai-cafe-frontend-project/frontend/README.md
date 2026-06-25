# CanAI Café Intelligence Portal

React + Vite frontend for the CanAI Café June 2026 Hackathon.

This app is an executive reporting portal that presents cleaned sales KPIs, data quality decisions, product insights, regional insights, a six-month forecast, recommendations, methodology, and a Power BI connection page.

## Tech stack

- React
- Vite
- React Router
- Recharts
- Plain CSS
- Static JSON data from `public/data`

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown by Vite, usually:

```text
http://localhost:5173
```

## Build

```bash
npm run build
npm run preview
```

## Data files

The frontend reads JSON files from:

```text
frontend/public/data
```

Important files:

- `kpi_summary.json`
- `data_quality_summary.json`
- `monthly_sales.json`
- `product_performance.json`
- `province_performance.json`
- `forecast_6_months.json`
- `recommendations.json`
- `methodology.json`

## Power BI link

Optional:

1. Copy `.env.example` to `.env`
2. Set:

```text
VITE_POWERBI_REPORT_URL=https://your-powerbi-report-link
```

Then restart Vite.

## Demo flow

1. Executive Overview
2. Data Quality
3. Sales Performance
4. Products
5. Regions
6. Forecast
7. Recommendations
8. Methodology
9. Power BI
