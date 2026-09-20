
# FinPilot — AI-Powered Personal Finance Decision-Support Agent

## Problem
Financial information is spread across statements, bills, subscriptions, emails and spreadsheets. People can see transactions but often cannot easily connect spending, upcoming obligations, budgets and goals.

## What this prototype does
FinPilot provides one workflow:

**Import → Understand → Detect → Compare → Plan → Ask → Summarize**

It supports:
- Transaction statement CSV/XLSX upload
- Bill/obligation CSV/XLSX upload
- Automatic transaction categorization
- Recurring payment/subscription detection
- Unusual-spending signals
- Monthly income/expense summaries
- Upcoming obligations
- User-defined budgets and budget-vs-actual
- Financial goals
- Simple goal-impact scenarios
- Personalized, explainable spending insights
- Natural-language questions
- Monthly financial summary + action items
- Month-over-month comparison

## Important reliability design
The core demo does NOT depend on:
- live bank APIs
- bank credentials
- paid LLM APIs
- external finance feeds

All core calculations are local and deterministic. This makes the hackathon demonstration stable.

The term "AI-powered agent" is represented through an agent workflow that observes data, detects patterns, explains evidence and generates a prioritized action queue. An LLM can later be connected for richer language generation, but it is not required for the core functionality.

## How to run on Windows
```cmd
cd FinPilot_8Criteria
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Recommended jury demo
1. Click **Load 3-month demo**.
2. Dashboard shows income, expenses, cash flow and largest spending category.
3. Open **Transactions** to demonstrate real transaction records.
4. Open **Recurring & Subscriptions** to show Netflix/Spotify/repeated merchants.
5. Add/upload a bill in **Bills**.
6. Set limits in **Budgets**.
7. Create an emergency-fund/purchase goal in **Goals**.
8. Open **Monthly Compare** to show what increased from August to September.
9. Open **Agent Insights** to show the agent's evidence and action queue.
10. Ask: **"Where did I spend the most this month?"**
11. Open **Monthly Report** to finish with observations + action items.

## Eight judging criteria

### 1. Clear real-world problem
The product directly addresses fragmented personal financial information and difficulty understanding everyday cash flow.

### 2. Innovative solution
The differentiator is not a generic expense chart. FinPilot connects transaction history, upcoming obligations, budgets, goals and month-over-month changes into an explainable agent action queue.

### 3. Functional working prototype
The user can load data and move through multiple connected sections. Calculations are generated from the loaded dataset.

### 4. Clean, modern, user-friendly UI
SaaS-style dashboard, focused navigation, cards, metrics, tables and charts.

### 5. Responsive design
Streamlit responsive layout + mobile-conscious CSS. Sections use adaptive columns rather than fixed-width panels.

### 6. Meaningful user flow
The user progresses from raw data to understanding, then monitoring, planning and action:
Import → Verify → Analyze → Detect commitments → Compare → Set budgets/goals → Ask → Monthly report.

### 7. Proper use of technology
Python + Streamlit + Pandas + statistical anomaly detection + categorization + stateful agent workflow + file parsing.

### 8. Real-world impact
The app is designed for everyday financial understanding without claiming to replace a financial professional or provide regulated advice.

## Data format

Transactions minimum:
```csv
Date,Description,Amount
2026-09-01,Salary,65000
2026-09-02,Rent,-18000
```

Optional:
```csv
Type,Category,Notes
Expense,Housing,Monthly rent
```

Bills minimum:
```csv
Name,Amount
Internet,999
Electricity,1450
```

Optional bills columns:
`Due Date, Frequency, Category`

## Safety / positioning
Do not pitch FinPilot as an investment adviser, bank, fraud detector, tax adviser or credit adviser. It is a personal finance understanding and everyday decision-support prototype.
