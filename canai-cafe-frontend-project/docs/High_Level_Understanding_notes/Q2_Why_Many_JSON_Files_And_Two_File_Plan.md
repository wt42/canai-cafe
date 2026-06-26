# Q2 — Why So Many JSON Files? Can We Keep Only Two Files?

## 1. Simple Answer

Yes, we can keep only **two JSON files** for the frontend.

The many JSON files were not mandatory. I used many files because each page had its own clean data source.

For example:

```text
kpi_summary.json              → Executive Overview
monthly_sales.json            → Sales Performance
product_performance.json      → Product Page
province_performance.json     → Regional Page
forecast_6_months.json        → Forecast Page
recommendations.json          → Recommendation Page
methodology.json              → Methodology Page
```

This structure is easy for development because each page reads only the data it needs.

But for your project, since you want it simple like the data-cleaning project, we can reduce it to only two files.

---

## 2. Why I Created Many JSON Files First

My thought was:

```text
One page = one focused data file
```

This makes frontend development easier because:

1. Each page is simple to understand.
2. If one page has a problem, we check only one data file.
3. Charts load smaller data.
4. It is easy to replace one section later.
5. It looks organized for a larger dashboard.

Example:

```text
Forecast page needs only forecast_6_months.json
Product page needs only product_performance.json
Data Quality page needs only data_quality_summary.json
```

So the frontend code becomes clear page by page.

---

## 3. But Why This Can Feel Too Much

You are right to question it.

For a hackathon, too many JSON files can feel like extra complexity.

A beginner or teammate may ask:

```text
Which JSON file should I update?
Where is the main data?
Why are there so many files?
```

That confusion is not good when time is short.

So for your current level and team situation, two JSON files are better.

---

## 4. Recommended Two-File Structure

Use only these two files:

```text
frontend/public/data/business_data.json
frontend/public/data/app_content.json
```

---

# File 1 — business_data.json

This file should contain all numeric and chart data.

It will include:

```text
KPI summary
Data quality summary
Monthly sales
Product performance
Province performance
Payment performance
Location performance
Weekday vs weekend data
Forecast data
```

Simple meaning:

```text
business_data.json = all numbers, charts, and analysis data
```

---

# File 2 — app_content.json

This file should contain all text-based content.

It will include:

```text
Recommendations
Methodology explanation
Power BI notes
Demo script text
Limitations
Business explanation messages
```

Simple meaning:

```text
app_content.json = all explanation, recommendation, and page text
```

---

## 5. Final Two-File Data Folder

Instead of this:

```text
frontend/public/data/
├── kpi_summary.json
├── data_quality_summary.json
├── monthly_sales.json
├── product_performance.json
├── province_performance.json
├── payment_performance.json
├── location_performance.json
├── weekday_weekend.json
├── weekday_detail.json
├── forecast_6_months.json
├── recommendations.json
├── methodology.json
└── powerbi_report.json
```

We will use this:

```text
frontend/public/data/
├── business_data.json
└── app_content.json
```

This is cleaner for your project.

---

## 6. How business_data.json Should Look

Example structure:

```json
{
  "kpiSummary": {
    "totalRevenue": 86288,
    "totalTransactions": 10000,
    "totalUnitsSold": 19853,
    "averageTransactionValue": 8.63,
    "topProduct": "Sandwich",
    "topProvince": "British Columbia",
    "sixMonthForecast": 43094.97,
    "dataQualityScore": 78.63
  },
  "dataQuality": {
    "summaryCards": [],
    "issueBreakdown": [],
    "categoryCleanup": []
  },
  "sales": {
    "monthlySales": [],
    "weekdayWeekend": [],
    "weekdayDetail": []
  },
  "products": [],
  "provinces": [],
  "payments": [],
  "locations": [],
  "forecast": {
    "modelName": "Weekday-adjusted baseline forecast",
    "forecastPeriod": "January 2024 to June 2024",
    "totalForecastRevenue": 43094.97,
    "monthlyForecast": []
  }
}
```

---

## 7. How app_content.json Should Look

Example structure:

```json
{
  "recommendations": [],
  "methodology": {
    "sections": []
  },
  "powerBi": {
    "title": "Power BI Dashboard",
    "status": "Optional integration point",
    "reportUrl": ""
  },
  "demoScript": {
    "opening": "We built the CanAI Cafe Intelligence Portal...",
    "flow": []
  }
}
```

---

## 8. What Will Change in React Code?

Currently pages may load files like this:

```javascript
getJson('kpi_summary.json')
getJson('monthly_sales.json')
getJson('forecast_6_months.json')
```

After two-file structure, pages will load:

```javascript
getJson('business_data.json')
getJson('app_content.json')
```

Then each page will pick its section.

Example:

```javascript
const businessData = await getJson('business_data.json');
const kpi = businessData.kpiSummary;
const monthlySales = businessData.sales.monthlySales;
const forecast = businessData.forecast;
```

---

## 9. Which Approach Is Better?

## Many JSON Files

Good when:

```text
Project is large
Many developers are working
Each page has separate ownership
Data is updated independently
```

Problem:

```text
Too many files for a small hackathon frontend
May confuse beginners
More fetch calls
```

---

## Two JSON Files

Good when:

```text
Project must stay simple
One frontend developer owns the app
Hackathon time is short
Team wants easy explanation
```

Problem:

```text
The file becomes larger
One mistake can affect multiple pages
```

But for our case, two files are better.

---

## 10. Final Decision

For this hackathon frontend, we should use:

```text
business_data.json
app_content.json
```

Reason:

```text
Simple to explain
Simple to maintain
Easy for your team
Matches the data-cleaning project style
Still professional enough for the demo
```

---

## 11. My Final Thought

The first version with many JSON files was written like a larger dashboard project.

But your project needs to be:

```text
clean
simple
understandable
demo-ready
```

So yes, we should reduce the frontend data folder to two files.

Final frontend data folder:

```text
frontend/public/data/
├── business_data.json
└── app_content.json
```

That is the best structure for your current hackathon solution.
