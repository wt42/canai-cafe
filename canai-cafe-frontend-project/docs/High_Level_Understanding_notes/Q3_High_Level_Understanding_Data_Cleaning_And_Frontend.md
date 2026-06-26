# Q3 — High Level Understanding of Data-Cleaning and Frontend Code

## 1. Simple Big Picture

The whole project has two main parts:

```text
Data-Cleaning Project  →  Makes the data correct and trustworthy
Frontend React App     →  Shows the cleaned result in a business-friendly way
```

Think of it like this:

```text
Raw Excel file
   ↓
Python cleaning code
   ↓
Clean CSV / summary data
   ↓
Frontend JSON files
   ↓
React dashboard pages
   ↓
Judges understand the story
```

The Python side is the **factory**.
The React side is the **showroom**.

Python prepares the data.
React presents the data.

---

# Part A — High Level Understanding of Data-Cleaning Code

## 2. Why we wrote data-cleaning code

The hackathon dataset is not ready for direct dashboarding.

It has problems like:

```text
Missing values
Wrong spellings
Duplicate transaction IDs
Invalid payment values
Inconsistent province names
Unknown dates
Dirty item names
```

So, before analysis or dashboarding, we needed to clean and prepare the dataset.

The goal of data-cleaning code is:

```text
Convert messy raw data into trusted clean data.
```

---

## 3. Data-cleaning project flow

```text
Step 1: Read raw Excel file
Step 2: Standardize column names
Step 3: Clean province names
Step 4: Clean item names
Step 5: Clean payment method
Step 6: Clean location
Step 7: Clean transaction date
Step 8: Convert numeric columns
Step 9: Repair missing numeric values where possible
Step 10: Add quality flags
Step 11: Export clean CSV and cleaning summary
```

---

## 4. What `dataset_cleaner.py` does

This is the main cleaning file.

Its responsibility is:

```text
Take raw Excel input
Clean it
Repair recoverable values
Flag data-quality issues
Export final cleaned CSV
```

High-level work inside this file:

| Area | What it does |
|---|---|
| Column cleanup | Converts column names into clean format like `transaction_id`, `total_spent` |
| Province cleanup | Converts values like `BC`, `B.C.`, `BritishColumbia` into `British Columbia` |
| Item cleanup | Converts values like `cofee`, `c0ffee`, `sandwhich` into clean product names |
| Payment cleanup | Keeps valid payments and marks invalid/missing ones as `Unknown Payment` |
| Location cleanup | Keeps `In-store`, `Takeaway`, and marks blanks as `Unknown Location` |
| Date cleanup | Converts valid dates and marks invalid dates |
| Numeric repair | Repairs missing quantity using `total_spent / price_per_unit` |
| Quality flags | Adds flags like duplicate ID, missing date, unknown payment |
| Output | Creates `clean_output.csv`, `cleaning_summary.csv`, and rejected rows file |

---

## 5. Important mindset in cleaner code

The cleaner should not delete data blindly.

Bad approach:

```text
If row has missing value → delete row
```

Good approach:

```text
If value can be repaired safely → repair it
If value cannot be repaired → mark it as Unknown or flag it
Only reject truly invalid rows
```

Example:

```text
Quantity is missing
Price Per Unit is available
Total Spent is available

Quantity = Total Spent / Price Per Unit
```

So this row should be repaired, not deleted.

---

## 6. What `dataset_profiler.py` does

The profiler is not mainly for cleaning.

Its purpose is to **inspect** the data.

It helps us answer:

```text
What dirty values exist?
How many unique item names are there?
How many province spellings are there?
What payment methods exist?
What locations exist?
```

In simple words:

```text
Cleaner = fixes the data
Profiler = tells us what is wrong in the data
```

The profiler helps us prove our cleaning work during the hackathon.

---

## 7. Data-cleaning outputs

The data-cleaning project produces files like:

```text
data/processed/clean_output.csv
data/processed/cleaning_summary.csv
data/processed/profile_report.txt
data/processed/rejected_rows.csv
```

Meaning:

| File | Purpose |
|---|---|
| `clean_output.csv` | Final cleaned dataset |
| `cleaning_summary.csv` | Summary of what was cleaned |
| `profile_report.txt` | Human-readable data profile |
| `rejected_rows.csv` | Rows that could not be safely used, if any |

---

# Part B — High Level Understanding of Frontend Code

## 8. Why we wrote frontend code

The frontend is not doing heavy data cleaning.

The frontend is for presentation.

Its goal is:

```text
Show cleaned data, insights, forecast, and recommendations in a professional way.
```

The React app helps judges quickly understand:

```text
What was cleaned?
What did we find?
What is the forecast?
What should the business do next?
```

---

## 9. Frontend project flow

```text
Step 1: React app starts
Step 2: It loads JSON files from public/data
Step 3: Data service reads those files
Step 4: Pages receive the data
Step 5: Components display KPI cards, charts, tables, and recommendations
Step 6: User navigates between pages using sidebar
```

---

## 10. Frontend folder structure

```text
frontend/
├── public/
│   └── data/
│       └── JSON files
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── package.json
└── vite.config.js
```

---

## 11. Meaning of important frontend folders

| Folder | Meaning |
|---|---|
| `public/data` | Stores prepared JSON data for the frontend |
| `src/pages` | Full screens like Executive Overview, Forecast, Data Quality |
| `src/components` | Reusable UI parts like cards, charts, sidebar |
| `src/services` | Code that loads data from JSON files |
| `src/utils` | Formatting helpers for currency, numbers, percentages |
| `src/index.css` | Styling for the full app |

---

## 12. What `main.jsx` does

This is the starting point of the React app.

Simple meaning:

```text
main.jsx starts React and attaches App.jsx to the browser page.
```

It connects React to:

```html
<div id="root"></div>
```

---

## 13. What `App.jsx` does

`App.jsx` controls page routing.

It says:

```text
/overview          → Executive Overview page
/data-quality      → Data Quality page
/sales             → Sales Performance page
/products          → Product Intelligence page
/regions           → Regional Intelligence page
/forecast          → Forecast Center page
/recommendations   → Recommendations page
/methodology       → Methodology page
/powerbi           → Power BI page
```

Simple meaning:

```text
App.jsx decides which page should open for which URL.
```

---

## 14. What layout components do

Layout components create the common app structure.

Example:

```text
Sidebar
Topbar
Main page area
```

This means every page has the same professional look.

The user does not feel like every page is separate.

---

## 15. What card components do

Cards are reusable small UI blocks.

Examples:

```text
KPI Card
Insight Card
Recommendation Card
Methodology Card
```

Instead of writing the same design again and again, we create one component and reuse it.

Example:

```text
Total Revenue card
Transactions card
Top Product card
Forecast card
```

All can use the same `KpiCard` component.

---

## 16. What chart components do

Chart components show the numbers visually.

Examples:

```text
Monthly Sales Chart
Product Revenue Chart
Province Revenue Chart
Forecast Chart
Data Quality Chart
Weekday vs Weekend Chart
```

Simple meaning:

```text
Charts convert table data into visual understanding.
```

This is important because judges can understand charts faster than raw CSV rows.

---

## 17. What `dataService.js` does

This file loads data from JSON files.

Example:

```text
Load kpi_summary.json
Load monthly_sales.json
Load forecast_6_months.json
```

Simple meaning:

```text
dataService.js is the bridge between JSON data and React pages.
```

React pages should not know too much about file loading logic.

They should simply ask:

```text
Give me the data
```

---

## 18. What utility files do

Utility files help format values.

Examples:

```text
86288 → $86,288.00
10000 → 10,000
78.63 → 78.63%
```

Without utility files, formatting code gets repeated everywhere.

---

# Part C — How Data-Cleaning and Frontend Work Together

## 19. Full connection

```text
Raw Excel file
   ↓
dataset_cleaner.py
   ↓
clean_output.csv
   ↓
summary / forecast / business JSON
   ↓
React frontend
   ↓
Dashboard pages
   ↓
Hackathon demo
```

---

## 20. Who owns what?

| Area | Owner |
|---|---|
| Raw Excel reading | Python |
| Cleaning dirty data | Python |
| Repairing missing quantity/item | Python |
| Creating clean CSV | Python |
| Creating business summary | Python / data team |
| Showing KPI cards | React |
| Showing charts | React |
| Showing recommendations | React |
| Explaining methodology | React |
| Final demo story | Team |

---

## 21. Why frontend should not clean raw Excel

React should not clean the Excel file directly because:

```text
It makes frontend complicated
It creates performance issues
It mixes business logic with UI code
It becomes hard to test
It becomes hard to explain
```

Better approach:

```text
Python cleans data
React displays data
```

This is clean separation of responsibility.

---

## 22. Simple analogy

Imagine a restaurant.

```text
Kitchen = Python data-cleaning code
Dining area = React frontend
Customer = Judge / Business user
```

The kitchen prepares the food properly.
The dining area presents it nicely.
The customer should not see the messy preparation work.

But if the customer asks, we can explain how the food was prepared.

That is exactly what our project does.

---

# Part D — What to Say in Presentation

## 23. Simple explanation for judges

You can say:

```text
We separated the project into two layers.

The Python layer cleans and prepares the raw café transaction data. It fixes spelling issues, repairs recoverable numeric fields, standardizes categories, flags duplicate IDs, and creates clean output files.

The React frontend is the executive reporting layer. It reads prepared JSON files and displays KPIs, charts, forecast results, cleaning decisions, and business recommendations in a clean dashboard format.

This separation keeps the solution reliable, explainable, and demo-friendly.
```

---

# 24. Final Simple Summary

```text
Data-cleaning code answers:
Can we trust the data?

Frontend code answers:
Can business users understand the result?
```

So the high-level project understanding is:

```text
Python makes the data correct.
React makes the data understandable.
Power BI can support deeper dashboarding.
Presentation explains the business value.
```

That is the full solution story.
