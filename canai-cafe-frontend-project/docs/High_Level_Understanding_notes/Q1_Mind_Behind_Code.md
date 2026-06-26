# Q1 — What Was the Mind Behind Writing This Code?

## 1. Simple Answer

The main thought behind the code was:

> First make the data trustworthy, then make the frontend easy to understand for judges and business users.

This project is not just about writing Python or React code. The hackathon problem is a business problem:

- The café has sales data.
- The data is dirty.
- The business wants to understand past sales.
- The business also wants a six-month forecast.
- The final solution should help decision-making.

So the code was written with this mindset:

```text
Raw dirty data
        ↓
Clean and reliable data
        ↓
Business summaries
        ↓
Frontend dashboard
        ↓
Clear recommendations for judges
```

---

## 2. Mind Behind the Data-Cleaning Code

The data-cleaning code was written first because bad data gives bad dashboard results.

If we directly create charts from dirty data, then the dashboard may look good but the insights will be wrong.

So the data-cleaning code focuses on these things:

```text
1. Standardize column names
2. Clean product names
3. Clean province names
4. Handle missing values
5. Repair values that can be recovered
6. Keep unknown values visible
7. Flag duplicate transaction IDs
8. Export a clean CSV for analysis and frontend
```

---

## 3. Why We Standardized Column Names

Raw Excel columns may have spaces and capital letters.

Example:

```text
Transaction ID
Price Per Unit
Total Spent
```

For coding, these are converted into:

```text
transaction_id
price_per_unit
total_spent
```

Why?

Because this style is easier and safer in Python.

Instead of writing confusing column names repeatedly, we get clean names for development.

---

## 4. Why We Cleaned Product Names

The product column had spelling and formatting issues.

Example:

```text
cofee
coffe
c0ffee
tee
sandwhich
donutt
```

These should not appear as separate products in the dashboard.

So the mind was:

> One real product should have one clean name.

Example:

```text
cofee, coffe, c0ffee → Coffee
tee → Tea
sandwhich → Sandwich
donutt → Donut
```

Without this cleaning, the Product Performance page would show fake products.

---

## 5. Why We Cleaned Province Names

Province values also had issues.

Example:

```text
BC
B.C.
BritishColumbia
British Columba
MB
Manitba
SK
Sasktchewan
NL
NFLD
```

The mind was:

> A province should be shown once, not in multiple wrong spellings.

So we mapped dirty values to clean province names.

This makes regional analysis meaningful.

---

## 6. Why We Did Not Blindly Delete Dirty Rows

In beginner projects, people often delete rows with missing values.

But in this project, that would be risky.

Example:

If quantity is missing, but total spent and price per unit are available, then quantity can be recovered:

```text
quantity = total_spent / price_per_unit
```

So the mindset was:

> Do not delete a row if it can be logically repaired.

This protects revenue and avoids losing useful data.

---

## 7. Why We Used Unknown Values

For some fields, we cannot safely guess the value.

Example:

```text
Missing payment method
Missing location
Missing province
```

We should not randomly replace missing payment with `Credit Card` just because Credit Card is common.

That would create fake insight.

So the better approach is:

```text
Missing payment method → Unknown Payment
Missing location → Unknown Location
Missing province → Unknown Province
```

This keeps the dashboard honest.

---

## 8. Why We Added Flags

Flags are simple true/false columns that explain what happened to each row.

Example:

```text
quantity_repaired_flag
item_imputed_flag
duplicate_transaction_id_flag
missing_date_flag
unknown_payment_flag
unknown_location_flag
unknown_province_flag
```

The reason is simple:

> We should be able to prove what we cleaned.

This helps in the presentation because judges may ask:

```text
How many rows did you repair?
How many values were missing?
Did you delete duplicate records?
How did you handle unknown values?
```

With flags, we can answer confidently.

---

## 9. Mind Behind the Frontend Code

The frontend code was written with a different purpose.

The frontend is not responsible for cleaning data.

The frontend is responsible for showing the story clearly.

The frontend mind was:

```text
Do not make a complex app.
Make a clean executive portal.
Use prepared data.
Show insights clearly.
Support the final presentation.
```

---

## 10. Why We Built Multiple Pages

The frontend has multiple pages because each page answers one business question.

| Page | Business Question |
|---|---|
| Executive Overview | What is the full business summary? |
| Data Quality | What was wrong and what did we clean? |
| Sales Performance | How did sales perform in 2023? |
| Product Intelligence | Which products matter most? |
| Regional Intelligence | Which provinces performed best? |
| Forecast Center | What may happen in the next six months? |
| Recommendations | What should the business do next? |
| Methodology | How did we build the solution? |
| Power BI | Where can detailed BI report be connected? |

The goal is to help judges move through the story step by step.

---

## 11. Why React Reads Prepared JSON

The frontend reads prepared JSON files because React should not do heavy data-cleaning logic.

The correct responsibility split is:

```text
Python → Clean data and prepare output
React → Display clean output beautifully
Power BI → Detailed dashboard/reporting
Presentation → Explain business value
```

This makes the frontend stable and easy to demo.

---

## 12. Why We Avoided Backend, Login, Database, and AI

For this hackathon, time is limited.

Adding too many things can create bugs and confusion.

So we avoided:

```text
Backend API
Login system
Database
AI assistant
Live CSV upload
Admin panel
Complex state management
```

The mind was:

> Build what helps us win, not what makes the project unnecessarily heavy.

---

## 13. Final Simple Understanding

The code was written with this thinking:

```text
1. Fix the data first.
2. Do not hide data quality issues.
3. Keep business logic in Python.
4. Keep frontend simple and presentation-ready.
5. Show facts, not guesses.
6. Make the final solution easy for judges to understand.
```

In short:

> The data-cleaning code builds trust.  
> The frontend code builds clarity.  
> Together, they help the team tell a strong hackathon story.

---

## 14. One-Line Interview Explanation

If someone asks why we wrote the code this way, say:

> We separated data preparation from presentation: Python cleans and validates the café sales data, while React presents the cleaned insights, forecast, and recommendations in a simple executive portal.
