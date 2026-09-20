# FinPilot

**An explainable financial workspace for personal financial records.**

FinPilot consolidates transaction statements, bills, subscriptions and spreadsheets into a single, coherent view of spending, commitments, cash flow and savings goals. All processing is performed locally. The system requires no bank credentials, no paid APIs and no live financial data feeds.

> **Disclaimer:** FinPilot is a decision-support tool. It does not provide investment, tax, credit, insurance or any other form of professional financial advice. It describes the data supplied by the user and identifies items that may warrant review.

---

## Table of Contents

1. [Background](#background)
2. [Features](#features)
3. [System Overview](#system-overview)
4. [Interfaces](#interfaces)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Sample Data](#sample-data)
8. [Input Data Format](#input-data-format)
9. [Project Structure](#project-structure)
10. [API Reference](#api-reference)
11. [Privacy and Design Principles](#privacy-and-design-principles)
12. [Limitations](#limitations)
13. [Future Work](#future-work)
14. [Contributing](#contributing)
15. [License](#license)

---

## Background

Individuals typically hold financial information across many sources, including bank statements, card statements, bills, subscriptions and personal spreadsheets. The difficulty is not a lack of data but its fragmentation, which makes it hard to understand where money is spent and what obligations lie ahead.

FinPilot addresses this by combining these records into one workspace and presenting the results with the supporting evidence, so that users can understand their finances and make their own informed decisions.

## Features

Given a transaction statement, FinPilot performs the following functions:

- **Categorization:** Assigns each transaction to one of ten categories, with keyword rules suited to Indian merchants and amounts in rupees (INR).
- **Recurring payment detection:** Identifies repeated payments and probable subscriptions.
- **Unusual spending detection:** Flags expenses that exceed a transparent statistical threshold.
- **Cash flow summary:** Reports monthly income, expenses and net position.
- **Bill tracking:** Records upcoming obligations separately from paid transaction history.
- **Budget comparison:** Compares user-defined budgets with actual spending by category.
- **Goal tracking:** Relates savings goals to planned monthly contributions.
- **Month-over-month comparison:** Shows the absolute and percentage change in spending by category.
- **Natural-language queries:** Answers common questions about the loaded data.
- **Action queue:** Presents a prioritized list of items to review, each with supporting evidence.

For example, rather than reporting only that a category has increased, FinPilot presents the amount and percentage change and identifies the category concerned, so that the change can be reviewed.

## System Overview

The analytical workflow proceeds in four stages:

1. **Observe:** The user's records are imported from CSV or Excel files, or entered manually, and normalized to a common schema.
2. **Detect:** Patterns are identified, including recurring payments, unusual transactions and month-over-month trends.
3. **Explain:** Each finding is presented together with its underlying amounts and the rule that produced it.
4. **Prioritize:** Findings are assembled into an action queue that indicates what the user should review first.

All calculations are performed locally using pandas. No external language model is used. Each output can be traced to the user's data and to a stated rule.

| Signal | Rule |
|---|---|
| Recurring payment | The same description appears two or more times among expenses |
| Unusual spending | Expense amount exceeds the mean plus two standard deviations (requires at least five expenses) |
| Budget status | Under 80% of budget used: within budget; 80% to 100%: approaching limit; over 100%: exceeded |
| Goal timeline | (Target - Amount saved) divided by planned monthly contribution |
| Largest increase | The category with the greatest expense increase relative to the previous month |

## Interfaces

The repository provides two interfaces built on the same core logic.

| | Streamlit application | Web dashboard |
|---|---|---|
| Entry point | `app.py` | `server.py` and `frontend/` |
| Technology | Streamlit, pandas | Flask REST API, HTML, CSS, JavaScript, Chart.js |
| Scope | Full feature set | Dashboard, Transactions, Budgets and Subscriptions, Goals, Ask FinPilot |
| Command | `streamlit run app.py` | `python server.py` plus a static file server |

The Streamlit application includes the following pages: Dashboard, Transactions, Spending, Recurring and Subscriptions, Bills, Budgets, Goals, Monthly Compare, Agent Insights, Ask FinPilot and Monthly Report.

## Installation

**Prerequisites:** Python 3.9 or later.

```bash
# Clone the repository
git clone https://github.com/your-username/FinPilot.git
cd FinPilot

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option A: Streamlit application

```bash
streamlit run app.py
```

The application is served at `http://localhost:8501`.

### Option B: Web dashboard

The backend and frontend must run concurrently in separate terminals.

Terminal 1: start the Flask API on port 5000.

```bash
python server.py
```

Terminal 2: serve the frontend on port 8000.

```bash
cd frontend
python -m http.server 8000
```

Open `http://localhost:8000` in a browser. The frontend communicates with the API at `http://localhost:5000/api`, which is set by the `API_BASE` constant at the top of `frontend/app.js`.

### Natural-language queries

The Ask FinPilot feature supports queries such as:

- Where did I spend the most this month?
- How much did I save this month?
- What is my total income?
- Which subscriptions am I paying for?
- What expenses increased compared with last month?
- How much of my budget is already committed?
- How much did I spend on Food?
- How can I save money?

Query handling is based on keyword intent detection. Where a query is not recognized, the system returns a brief summary of the most recent month.

## Sample Data

The `sample_data/` directory contains files for evaluation.

| File | Contents | Intended use |
|---|---|---|
| `demo_data.csv` | 25 transactions, September 2026 | Initial review of the dashboard |
| `sample_transactions.csv` | 27 transactions, July to September 2026 | Month-over-month comparison and trend analysis |
| `sample_bills.csv` | 4 bills: Internet, Electricity, Netflix, College Fee | Bills page (Streamlit application) |

Suggested evaluation sequence:

1. Upload `sample_transactions.csv` through the file uploader.
2. Review the dashboard, followed by the Monthly Compare page in the Streamlit application.
3. Upload `sample_bills.csv` on the Bills page to view committed obligations.
4. Define several budgets and create a savings goal.
5. Use Ask FinPilot to submit queries against the loaded data.

## Input Data Format

FinPilot accepts CSV, XLSX and XLS files. Column headers are matched flexibly and without regard to case; for example, `Txn Date`, `Narration`, `Payee` and `Debit/Credit` are recognized.

### Transactions

| Column | Requirement | Notes |
|---|---|---|
| `Date` | Required | Any format parsable by pandas |
| `Amount` | Required | The symbols and text `₹`, `$`, `INR` and thousands separators are removed automatically |
| `Description` | Required in the Streamlit application; optional in the web dashboard | Blank values are recorded as "Unlabeled Transaction" in the web dashboard |
| `Type` | Optional | If absent, positive amounts are treated as Income and negative amounts as Expense. Values containing "credit", "income" or "deposit" are treated as Income |
| `Category` | Optional | If absent, a category is assigned from the description |
| `Notes` | Optional | Free text |

Example:

```csv
Date,Description,Amount,Type,Category,Notes
2026-07-01,Salary,65000,Income,Other,Monthly salary
2026-07-02,Rent,18000,Expense,Housing,
2026-07-03,BigBasket,2100,Expense,Food,
```

### Bills (Streamlit application)

| Column | Requirement |
|---|---|
| `Name` | Required |
| `Amount` | Required |
| `Due Date` | Optional |
| `Frequency` | Optional |
| `Category` | Optional |

### Categories

Housing, Food, Transport, Shopping, Bills, Health, Education, Entertainment, Subscriptions and Other.

Automatic categorization uses merchant keywords (for example Swiggy, Zomato, BigBasket, Uber, Ola, Rapido, Netflix, Spotify, Amazon and Flipkart). The rules may be extended by editing the `rules` dictionary in the `classify()` function.

## Project Structure

```
FinPilot/
├── app.py                  # Streamlit application (full feature set)
├── server.py               # Flask REST API for the web dashboard
├── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── sample_data/
│   ├── demo_data.csv
│   ├── sample_transactions.csv
│   └── sample_bills.csv
├── PITCH.md                # Project pitch
└── README.md
```

## API Reference

Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Uploads a CSV or Excel statement (multipart form, field `file`) |
| POST | `/add_transaction` | Adds a single transaction (JSON body) |
| GET | `/dashboard` | Returns income, expenses, net position, category totals and cash flow for the most recent month |
| GET | `/transactions` | Returns all normalized transactions |
| GET | `/frequent_transactions` | Returns repeated expense descriptions with count and total |
| GET | `/subscriptions` | Returns recurring expenses with average amount and last date seen |
| GET, POST | `/budgets` | Returns budgets and actual spending; sets a category budget |
| GET, POST | `/goals` | Lists savings goals; creates a savings goal |
| POST | `/ask` | Answers a natural-language query (JSON body: `{"query": "..."}`) |

## Privacy and Design Principles

- **Local-first:** User data remains on the user's machine. No bank credentials, cloud storage or paid APIs are required.
- **Explainable:** Every insight is accompanied by the rule and evidence from which it was derived.
- **Reliable:** Core calculations do not depend on network access or third-party services.
- **Non-advisory:** The system describes and compares recorded data. It does not recommend investments or financial products.

## Limitations

- **Prototype state management:** Data is held in memory, in server variables (Flask) or session state (Streamlit). It is not retained after a restart, and the Flask backend supports a single user.
- **Most recent month:** Dashboard figures and query responses are based on the latest month present in the data.
- **Recurring detection:** Matching relies on identical descriptions; variations in a merchant's name are treated as distinct payees.
- **Rule-based assistant:** The query engine recognizes a fixed set of intents and does not interpret free-form language.
- **Network dependency in the frontend:** The web dashboard loads Chart.js, `marked` and web fonts from external content delivery networks.
- **Currency:** Amounts are displayed in Indian rupees (INR).

## Future Work

- Persistent storage (for example SQLite)
- Fuzzy merchant matching for recurring payment detection
- Statement parsers for specific banks
- Optional, opt-in language-model explanations
- Multi-currency support and PDF report export

## Contributing

Contributions are welcome. For substantial changes, please open an issue to discuss the proposed modification before submitting a pull request.

## License

This project is released under the [MIT License](LICENSE).
