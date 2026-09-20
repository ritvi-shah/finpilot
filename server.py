from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import date
import io

app = Flask(__name__)
CORS(app)

CATEGORIES = ["Housing", "Food", "Transport", "Shopping", "Bills", "Health", "Education", "Entertainment", "Subscriptions", "Other"]

def classify(desc):
    x = str(desc).lower()
    rules = {
        "Housing": ["rent", "hostel", "housing"],
        "Food": ["swiggy", "zomato", "restaurant", "cafe", "food", "bigbasket", "blinkit", "zepto", "grocery"],
        "Transport": ["uber", "ola", "rapido", "metro", "fuel", "petrol", "bus", "train", "transport"],
        "Subscriptions": ["netflix", "spotify", "prime", "hotstar", "youtube premium", "subscription"],
        "Bills": ["electricity", "water bill", "internet", "mobile", "recharge", "gas", "utility"],
        "Shopping": ["amazon", "flipkart", "myntra", "shopping"],
        "Health": ["pharmacy", "hospital", "doctor", "medicine", "health"],
        "Education": ["college", "tuition", "course", "coursera", "fee"],
        "Entertainment": ["movie", "cinema", "game", "concert"]
    }
    for cat, words in rules.items():
        if any(w in x for w in words): return cat
    return "Other"

def normalize(raw):
    df = raw.copy()
    aliases = {}
    for c in df.columns:
        key = str(c).strip().lower().replace("_", " ").replace("-", " ")
        if key in ["date", "transaction date", "txn date"]: aliases[c] = "date"
        elif key in ["description", "merchant", "payee", "narration", "transaction description"]: aliases[c] = "description"
        elif key in ["amount", "transaction amount", "value"]: aliases[c] = "amount"
        elif key in ["type", "transaction type", "debit credit", "credit debit"]: aliases[c] = "type"
        elif key in ["category", "category name"]: aliases[c] = "category"
        elif key in ["notes", "note", "remarks"]: aliases[c] = "notes"
    df = df.rename(columns=aliases)
    if not {"date", "description", "amount"}.issubset(df.columns):
        return None, "Minimum columns required: Date, Description, Amount."
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = df["amount"].astype(str).str.replace(",", "", regex=False).str.replace("₹", "", regex=False).str.replace("$", "", regex=False).str.replace("INR", "", regex=False).str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "description", "amount"]).copy()
    if "type" not in df.columns:
        df["type"] = np.where(df["amount"] >= 0, "Income", "Expense")
    else:
        t = df["type"].astype(str).str.lower()
        df["type"] = np.where(t.str.contains("credit|income|deposit"), "Income", "Expense")
    if "category" not in df.columns: df["category"] = df["description"].map(classify)
    df["category"] = df["category"].fillna("Other").replace("", "Other").astype(str)
    if "notes" not in df.columns: df["notes"] = ""
    df.loc[df.type == "Income", "amount"] = df.loc[df.type == "Income", "amount"].abs()
    df.loc[df.type == "Expense", "amount"] = -df.loc[df.type == "Expense", "amount"].abs()
    return df[["date", "description", "amount", "type", "category", "notes"]].sort_values("date"), None

def demo_transactions():
    rows=[
    ["2026-07-01","Salary",65000,"Income","Other",""],
    ["2026-07-02","Rent",18000,"Expense","Housing",""],
    ["2026-07-03","BigBasket",2100,"Expense","Food",""],
    ["2026-07-04","Uber",420,"Expense","Transport",""],
    ["2026-07-05","Netflix",649,"Expense","Subscriptions",""],
    ["2026-07-06","Amazon",2100,"Expense","Shopping",""],
    ["2026-07-08","Electricity Bill",1200,"Expense","Bills",""],
    ["2026-07-10","Swiggy",850,"Expense","Food",""],
    ["2026-07-12","Pharmacy",780,"Expense","Health",""],
    ["2026-07-15","Uber",480,"Expense","Transport",""],
    ["2026-07-18","Amazon",1900,"Expense","Shopping",""],
    ["2026-07-21","Spotify",119,"Expense","Subscriptions",""],
    ["2026-07-25","Swiggy",760,"Expense","Food",""],
    ["2026-07-27","College Fee",7500,"Expense","Education",""],
    ["2026-08-01","Salary",65000,"Income","Other",""],
    ["2026-08-02","Rent",18000,"Expense","Housing",""],
    ["2026-08-03","BigBasket",2550,"Expense","Food",""],
    ["2026-08-04","Uber",610,"Expense","Transport",""],
    ["2026-08-05","Netflix",649,"Expense","Subscriptions",""],
    ["2026-08-06","Amazon",4200,"Expense","Shopping",""],
    ["2026-08-08","Electricity Bill",1450,"Expense","Bills",""],
    ["2026-08-10","Swiggy",1120,"Expense","Food",""],
    ["2026-08-12","Pharmacy",650,"Expense","Health",""],
    ["2026-08-15","Uber",520,"Expense","Transport",""],
    ["2026-08-18","Amazon",4600,"Expense","Shopping",""],
    ["2026-08-21","Spotify",119,"Expense","Subscriptions",""],
    ["2026-08-25","Swiggy",980,"Expense","Food",""],
    ["2026-08-27","College Fee",7500,"Expense","Education",""],
    ["2026-09-01","Salary",65000,"Income","Other",""],
    ["2026-09-02","Rent",18000,"Expense","Housing",""],
    ["2026-09-03","BigBasket",1850,"Expense","Food",""],
    ["2026-09-04","Uber",420,"Expense","Transport",""],
    ["2026-09-05","Netflix",649,"Expense","Subscriptions",""],
    ["2026-09-06","Amazon",2890,"Expense","Shopping",""],
    ["2026-09-08","Electricity Bill",1450,"Expense","Bills",""],
    ["2026-09-10","Swiggy",1620,"Expense","Food",""],
    ["2026-09-12","Pharmacy",780,"Expense","Health",""],
    ["2026-09-15","Uber",510,"Expense","Transport",""],
    ["2026-09-18","Amazon",4250,"Expense","Shopping",""],
    ["2026-09-19","Spotify",119,"Expense","Subscriptions",""],
    ["2026-09-20","Swiggy",1710,"Expense","Food",""],
    ["2026-09-22","College Fee",9000,"Expense","Education",""],
    ]
    return pd.DataFrame(rows,columns=["date","description","amount","type","category","notes"]).assign(date=lambda x:pd.to_datetime(x.date))

# Global state for prototype
state = {
    "df": pd.DataFrame(),
    "bills": pd.DataFrame(columns=["name", "amount", "due_date", "frequency", "category"]),
    "budgets": {},
    "goals": []
}

def get_months():
    if state["df"].empty: return []
    return sorted(state["df"].date.dt.to_period("M").astype(str).unique())

def month_stats(m):
    df = state["df"]
    x = df[df.date.dt.to_period("M").astype(str) == m]
    inc = float(x[x.type == "Income"].amount.sum())
    exp = float(x[x.type == "Expense"].amount.abs().sum())
    return inc, exp, inc - exp

@app.route('/api/load_demo', methods=['POST'])
def load_demo():
    state["df"] = demo_transactions()
    return jsonify({"success": True, "message": "Demo data loaded"})

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    if state["df"].empty:
        return jsonify({"empty": True})
    
    months = get_months()
    m = months[-1]
    inc, exp, net = month_stats(m)
    
    df = state["df"]
    exp_df = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Expense")]
    cat_totals = exp_df.groupby("category").amount.sum().abs().sort_values(ascending=False).to_dict()
    
    committed = sum(b["amount"] for _, b in state["bills"].iterrows()) if len(state["bills"]) else 0
    
    # cash flow series
    cf = df.groupby(df.date.astype(str)).amount.sum().to_dict()

    return jsonify({
        "empty": False,
        "month": m,
        "income": inc,
        "expenses": exp,
        "net": net,
        "committed": float(committed),
        "goals_count": len(state["goals"]),
        "category_totals": cat_totals,
        "cash_flow": cf
    })

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    if state["df"].empty: return jsonify([])
    df = state["df"].copy()
    df["date"] = df["date"].astype(str)
    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
