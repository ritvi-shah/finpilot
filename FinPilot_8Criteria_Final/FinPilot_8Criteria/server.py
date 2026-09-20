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
    df=raw.copy()
    aliases={}
    for c in df.columns:
        key=str(c).strip().lower().replace("_"," ").replace("-"," ")
        if key in ["date","transaction date","txn date"]: aliases[c]="date"
        elif key in ["description","merchant","payee","narration","transaction description"]: aliases[c]="description"
        elif key in ["amount","transaction amount","value"]: aliases[c]="amount"
        elif key in ["type","transaction type","debit credit","credit debit"]: aliases[c]="type"
        elif key in ["category","category name"]: aliases[c]="category"
        elif key in ["notes","note","remarks"]: aliases[c]="notes"
    df=df.rename(columns=aliases)
    if not {"date","amount"}.issubset(df.columns):
        return None,"Minimum columns required: Date and Amount."
    # Description is optional — fill blanks
    if "description" not in df.columns:
        df["description"] = "Unlabeled Transaction"
    df["description"] = df["description"].fillna("").astype(str).str.strip()
    df["description"] = df["description"].replace("", "Unlabeled Transaction")
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df["amount"]=df["amount"].astype(str).str.replace(",","",regex=False).str.replace("₹","",regex=False).str.replace("$","",regex=False).str.replace("INR","",regex=False).str.strip()
    df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
    df=df.dropna(subset=["date","amount"]).copy()
    if "type" not in df.columns:
        df["type"]=np.where(df["amount"]>=0,"Income","Expense")
    else:
        t=df["type"].astype(str).str.lower()
        df["type"]=np.where(t.str.contains("credit|income|deposit"),"Income","Expense")
    if "category" not in df.columns: df["category"]=df["description"].map(classify)
    df["category"]=df["category"].fillna("Other").replace("", "Other").astype(str)
    if "notes" not in df.columns: df["notes"]=""
    df.loc[df.type=="Income","amount"]=df.loc[df.type=="Income","amount"].abs()
    df.loc[df.type=="Expense","amount"]=-df.loc[df.type=="Expense","amount"].abs()
    return df[["date","description","amount","type","category","notes"]].sort_values("date"),None

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

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    try:
        if file.filename.endswith('.csv'):
            raw = pd.read_csv(file)
        else:
            raw = pd.read_excel(file)
        
        d, err = normalize(raw)
        if err:
            return jsonify({"success": False, "message": err}), 400
        
        state["df"] = d
        return jsonify({"success": True, "message": f"Loaded {len(d)} transactions"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    try:
        d = data.get('date', str(date.today()))
        desc = data.get('description', '')
        amt = float(data.get('amount', 0))
        typ2 = data.get('type', 'Expense')
        cat2 = data.get('category', 'Other')
        note = data.get('notes', '')
        
        # Description is optional; amount is the only hard requirement
        if not amt:
            return jsonify({"success": False, "message": "Amount is required"}), 400
        if not desc:
            desc = "Unlabeled Transaction"
            
        row = pd.DataFrame([[pd.Timestamp(d), desc, amt if typ2=="Income" else -abs(amt), typ2, cat2, note]], 
                           columns=["date","description","amount","type","category","notes"])
        
        if state["df"].empty:
            state["df"] = row
        else:
            state["df"] = pd.concat([state["df"], row], ignore_index=True)
            
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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

@app.route('/api/frequent_transactions', methods=['GET'])
def frequent_transactions():
    """Return descriptions that appear more than once — these are frequent/recurring."""
    if state["df"].empty:
        return jsonify([])
    df = state["df"]
    counts = df[df.type == "Expense"].groupby("description").agg(
        count=("amount", "count"),
        total=("amount", lambda x: x.abs().sum()),
        category=("category", "first")
    ).reset_index()
    freq = counts[counts["count"] > 1].sort_values("count", ascending=False)
    result = [
        {"description": row["description"],
         "count": int(row["count"]),
         "total": float(row["total"]),
         "category": row["category"]}
        for _, row in freq.iterrows()
    ]
    return jsonify(result)

@app.route('/api/budgets', methods=['GET', 'POST'])
def handle_budgets():
    if request.method == 'POST':
        data = request.json
        state["budgets"][data["category"]] = float(data["amount"])
        return jsonify({"success": True})
    
    # GET
    if state["df"].empty: return jsonify({"budgets": state["budgets"], "actuals": {}})
    m = get_months()[-1]
    df = state["df"]
    exp_df = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Expense")]
    actuals = exp_df.groupby("category").amount.sum().abs().to_dict()
    return jsonify({"budgets": state["budgets"], "actuals": actuals, "month": m})

@app.route('/api/goals', methods=['GET', 'POST'])
def handle_goals():
    if request.method == 'POST':
        data = request.json
        state["goals"].append({
            "name": data["name"],
            "target": float(data["target"]),
            "current": float(data["current"]),
            "monthly": float(data["monthly"])
        })
        return jsonify({"success": True})
    return jsonify(state["goals"])

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    if state["df"].empty: return jsonify([])
    df = state["df"]
    exp = df[df.type == "Expense"]
    groups = exp.groupby("description").agg(occurrences=("description", "size"), avg_amount=("amount", lambda s: s.abs().mean()), last_seen=("date", "max"))
    rec = groups[groups.occurrences >= 2].sort_values(["occurrences", "avg_amount"], ascending=False).reset_index()
    rec["last_seen"] = rec["last_seen"].astype(str)
    return jsonify(rec.to_dict(orient="records"))

@app.route('/api/ask', methods=['POST'])
def ask_finpilot():
    if state["df"].empty:
        return jsonify({"response": "Please load your data first."})
    
    q = request.json.get("query", "").lower()
    m = get_months()[-1]
    df = state["df"]
    exp = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Expense")]
    cats = exp.groupby("category").amount.sum().abs().sort_values(ascending=False)
    
    # Keyword sets for intent detection
    intent_highest = any(w in q for w in ["most", "highest", "biggest", "top", "max", "worst"])
    intent_spending = any(w in q for w in ["spend", "spent", "spending", "expense", "expenses", "cost"])
    intent_income = any(w in q for w in ["income", "earn", "earned", "salary", "revenue", "money in", "receive"])
    intent_total = any(w in q for w in ["total", "overall", "all", "sum", "how much"])
    intent_save = any(w in q for w in ["save", "saved", "saving", "net", "left", "remaining", "balance"])
    intent_subs = any(w in q for w in ["sub", "subscription", "recurring", "netflix", "spotify"])
    intent_compare = any(w in q for w in ["increase", "compare", "last month", "change", "difference", "trend"])
    intent_budget = any(w in q for w in ["budget", "commit", "obligation", "limit"])
    intent_advice = any(w in q for w in ["how can", "what should", "advice", "recommend", "help me", "improve"])

    if intent_highest and intent_spending:
        if len(cats) > 0:
            return jsonify({"response": f"Your largest expense category this month is **{cats.index[0]}** at ₹{cats.iloc[0]:,.0f}."})
        return jsonify({"response": "I don't see any expenses this month."})
        
    elif intent_income:
        inc = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Income")].amount.sum()
        return jsonify({"response": f"Your total recorded income for this month is **₹{inc:,.0f}**."})
        
    elif intent_save:
        inc = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Income")].amount.sum()
        tot = cats.sum()
        net = inc - tot
        if net > 0:
            return jsonify({"response": f"You have saved **₹{net:,.0f}** this month! That's {(net/inc*100):.1f}% of your income."})
        else:
            return jsonify({"response": f"Your net cash flow is **₹{net:,.0f}**. You spent more than you earned this month."})
            
    elif intent_total and intent_spending:
        tot = cats.sum()
        return jsonify({"response": f"Your total expenses for this month sum up to **₹{tot:,.0f}**."})
        
    elif intent_subs:
        sub = df[(df.type == "Expense") & (df.category == "Subscriptions")].groupby("description").amount.sum().abs()
        if len(sub):
            res = "Here are the subscriptions detected this month:\n" + "\n".join([f"- **{k}**: ₹{v:,.0f}" for k, v in sub.items()])
            return jsonify({"response": res})
        return jsonify({"response": "No subscription transactions were detected."})
        
    elif intent_compare:
        ms = get_months()
        if len(ms) < 2: return jsonify({"response": "I need at least two months of data to make a comparison."})
        prev_exp = df[(df.date.dt.to_period("M").astype(str) == ms[-2]) & (df.type == "Expense")]
        prev_cats = prev_exp.groupby("category").amount.sum().abs()
        comp = (cats - prev_cats).dropna().sort_values(ascending=False)
        if len(comp) > 0 and comp.iloc[0] > 0:
            return jsonify({"response": f"Your **{comp.index[0]}** expenses saw the biggest jump compared to last month (up by ₹{comp.iloc[0]:,.0f})."})
        return jsonify({"response": "Your spending has generally decreased or stayed the same compared to last month."})
        
    elif intent_budget:
        budget = sum(state["budgets"].values())
        used = cats.sum()
        committed = sum(b["amount"] for _, b in state["bills"].iterrows()) if len(state["bills"]) else 0
        return jsonify({"response": f"**Total budgets set:** ₹{budget:,.0f}\n**Recorded expenses:** ₹{used:,.0f}\n**Tracked upcoming obligations:** ₹{committed:,.0f}"})
        
    elif intent_advice:
        if len(cats) == 0:
            return jsonify({"response": "I need some expense data before I can give you advice!"})
        
        advice = []
        top_cat = cats.index[0]
        top_amt = cats.iloc[0]
        
        inc = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Income")].amount.sum()
        if inc > 0 and (top_amt / inc) > 0.4:
            advice.append(f"**Reduce {top_cat}**: You're spending over 40% of your income on {top_cat} (₹{top_amt:,.0f}). Consider setting a strict budget here.")
        else:
            advice.append(f"**Watch your top category**: Your biggest expense is {top_cat} (₹{top_amt:,.0f}). Look for areas to cut back here first.")
            
        sub = df[(df.type == "Expense") & (df.category == "Subscriptions")].groupby("description").amount.sum().abs()
        if len(sub) > 0:
            advice.append(f"**Audit Subscriptions**: You have {len(sub)} active subscriptions. Cancel any you haven't used in the last 30 days to easily save cash.")
            
        advice.append("**Automate Savings**: Set up an automatic transfer to your savings account right after payday so you don't accidentally spend it.")
        
        res = "Here is my personalized advice for you based on this month's data:\n\n" + "\n\n".join([f"- {a}" for a in advice])
        return jsonify({"response": res})
        
    else:
        # Check for specific categories dynamically
        for cat in CATEGORIES:
            if cat.lower() in q:
                spent = cats.get(cat, 0)
                if spent > 0:
                    return jsonify({"response": f"You have spent **₹{spent:,.0f}** on {cat} this month."})
                else:
                    return jsonify({"response": f"You haven't spent anything on {cat} this month."})
                    
        # Ultimate fallback - just give a general summary instead of "I'm not sure"
        inc = df[(df.date.dt.to_period("M").astype(str) == m) & (df.type == "Income")].amount.sum()
        tot = cats.sum()
        top_cat = cats.index[0] if len(cats) > 0 else "None"
        return jsonify({"response": f"Based on your data for {m}, you earned **₹{inc:,.0f}**, spent **₹{tot:,.0f}**, and your biggest expense was **{top_cat}**. Is there a specific category you want to know about?"})


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
