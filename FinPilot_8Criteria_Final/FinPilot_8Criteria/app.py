
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import calendar
import re

st.set_page_config(page_title="FinPilot", page_icon="💳", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp{background:#f7f8fc;color:#172033}
.block-container{max-width:1280px;padding-top:1.2rem}
[data-testid="stSidebar"]{background:#12172b}
[data-testid="stSidebar"] *{color:#eef0ff!important}
.hero{background:linear-gradient(135deg,#11172f,#414b91);padding:30px 34px;border-radius:24px;color:#fff;margin-bottom:18px}
.hero h1{font-size:42px;margin:0 0 7px;letter-spacing:-1.2px}.hero p{color:#e0e4ff;margin:0}
.card{background:#fff;border:1px solid #e7e9f0;border-radius:18px;padding:18px;margin-bottom:14px;box-shadow:0 5px 22px rgba(25,35,70,.055)}
.section{font-size:25px;font-weight:800;margin:18px 0 10px}.muted{color:#6c7488;font-size:13px}
.big{font-size:30px;font-weight:800}.good{color:#16865b;font-weight:700}.warn{color:#b87500;font-weight:700}.bad{color:#cc4d67;font-weight:700}
.insight{border-left:4px solid #5d5bd6;background:#f5f4ff;padding:12px 14px;border-radius:10px;margin:8px 0}
.agent{border:1px solid #dcdcff;background:#fafaff;border-radius:16px;padding:16px}
.tag{display:inline-block;padding:4px 9px;border-radius:999px;background:#eff0ff;color:#4c4db8;font-size:12px;margin:2px}
@media(max-width:800px){.hero h1{font-size:31px}.big{font-size:25px}}
</style>
""", unsafe_allow_html=True)

CATEGORIES=["Housing","Food","Transport","Shopping","Bills","Health","Education","Entertainment","Subscriptions","Other"]

def classify(desc):
    x=str(desc).lower()
    rules={
        "Housing":["rent","hostel","housing"],
        "Food":["swiggy","zomato","restaurant","cafe","food","bigbasket","blinkit","zepto","grocery"],
        "Transport":["uber","ola","rapido","metro","fuel","petrol","bus","train","transport"],
        "Subscriptions":["netflix","spotify","prime","hotstar","youtube premium","subscription"],
        "Bills":["electricity","water bill","internet","mobile","recharge","gas","utility"],
        "Shopping":["amazon","flipkart","myntra","shopping"],
        "Health":["pharmacy","hospital","doctor","medicine","health"],
        "Education":["college","tuition","course","coursera","fee"],
        "Entertainment":["movie","cinema","game","concert"]
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
    if not {"date","description","amount"}.issubset(df.columns):
        return None,"Minimum columns required: Date, Description, Amount."
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df["amount"]=df["amount"].astype(str).str.replace(",","",regex=False).str.replace("₹","",regex=False).str.replace("$","",regex=False).str.replace("INR","",regex=False).str.strip()
    df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
    df=df.dropna(subset=["date","description","amount"]).copy()
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



def money(x): return f"₹{abs(float(x)):,.0f}"

# ---------------- state ----------------
if "df" not in st.session_state: st.session_state.df=pd.DataFrame()
if "bills" not in st.session_state: st.session_state.bills=pd.DataFrame(columns=["name","amount","due_date","frequency","category"])
if "budgets" not in st.session_state: st.session_state.budgets={}
if "goals" not in st.session_state: st.session_state.goals=[]
if "page" not in st.session_state: st.session_state.page="Dashboard"
if "agent_log" not in st.session_state: st.session_state.agent_log=[]

# ---------------- sidebar ----------------
st.sidebar.markdown("## 💳 FinPilot")
st.sidebar.caption("AI-powered everyday finance decision support")
pages=["Dashboard","Transactions","Spending","Recurring & Subscriptions","Bills","Budgets","Goals","Monthly Compare","Agent Insights","Ask FinPilot","Monthly Report"]
for p in pages:
    if st.sidebar.button(p,use_container_width=True,type="primary" if st.session_state.page==p else "secondary"):
        st.session_state.page=p
st.sidebar.divider()
upload=st.sidebar.file_uploader("Upload transaction statement",type=["csv","xlsx","xls"])
if upload is not None and st.session_state.get("uploaded_name")!=upload.name:
    try:
        raw=pd.read_csv(upload) if upload.name.lower().endswith(".csv") else pd.read_excel(upload)
        d,err=normalize(raw)
        if err: st.sidebar.error(err)
        else:
            st.session_state.df=d; st.session_state.uploaded_name=upload.name
            st.sidebar.success(f"Loaded {len(d)} transactions")
    except Exception as e: st.sidebar.error(str(e))

if st.sidebar.button("Reset all",use_container_width=True):
    for k in ["df","bills","budgets","goals","agent_log"]:
        if k=="df": st.session_state[k]=pd.DataFrame()
        elif k=="bills": st.session_state[k]=pd.DataFrame(columns=["name","amount","due_date","frequency","category"])
        elif k=="budgets": st.session_state[k]={}
        elif k=="goals": st.session_state[k]=[]
        else: st.session_state[k]=[]
    st.rerun()
st.sidebar.caption("Local-first prototype • no bank login • no paid API required")

st.markdown("""
<div class="hero">
<h1>💳 FinPilot</h1>
<p>Your financial data is scattered. FinPilot turns it into one understandable, explainable picture of spending, commitments, cash flow and goals.</p>
</div>
""",unsafe_allow_html=True)

df=st.session_state.df
if df.empty:
    st.markdown("""
    <div class="card">
    <h2>Start with your financial data</h2>
    <p>Please upload a transaction statement or enter your first transaction manually below to begin. FinPilot requires your data to perform any analysis.</p>
    <div class="insight"><b>Privacy-first:</b> the prototype does not need bank credentials or a live banking connection. All data remains locally in your session.</div>
    </div>""",unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Upload CSV/Excel Statement")
        st.markdown("Minimum import format: `Date, Description, Amount`")
        main_upload = st.file_uploader("Upload your transaction statement", type=["csv","xlsx","xls"], key="main_upload")
        if main_upload is not None:
            try:
                raw=pd.read_csv(main_upload) if main_upload.name.lower().endswith(".csv") else pd.read_excel(main_upload)
                d,err=normalize(raw)
                if err: st.error(err)
                else:
                    st.session_state.df=d; st.session_state.uploaded_name=main_upload.name
                    st.success(f"Loaded {len(d)} transactions")
                    st.rerun()
            except Exception as e: st.error(str(e))
            
    with col2:
        st.markdown("### ✍️ Or Add Manually")
        with st.form("initial_tx"):
            d = st.date_input("Date", date.today())
            desc = st.text_input("Description")
            amt = st.number_input("Amount", min_value=0.0, step=100.0)
            typ2 = st.selectbox("Type", ["Expense","Income"])
            cat2 = st.selectbox("Category", CATEGORIES)
            note = st.text_input("Notes (Optional)")
            if st.form_submit_button("Add Transaction"):
                if desc and amt:
                    row = pd.DataFrame([[pd.Timestamp(d), desc, amt if typ2=="Income" else -amt, typ2, cat2, note]], columns=["date","description","amount","type","category","notes"])
                    st.session_state.df = row
                    st.rerun()
                else:
                    st.error("Please provide a description and amount.")
                    
    st.stop()

# ---------------- helpers ----------------
def months():
    return sorted(df.date.dt.to_period("M").astype(str).unique())
def month_stats(m):
    x=df[df.date.dt.to_period("M").astype(str)==m]
    inc=x[x.type=="Income"].amount.sum()
    exp=x[x.type=="Expense"].amount.abs().sum()
    return inc,exp,inc-exp
def current_month(): return months()[-1]
def category_total(m):
    return df[(df.date.dt.to_period("M").astype(str)==m)&(df.type=="Expense")].groupby("category").amount.sum().abs().sort_values(ascending=False)

# ---------------- Dashboard ----------------
if st.session_state.page=="Dashboard":
    m=current_month(); inc,exp,net=month_stats(m)
    st.markdown(f'<div class="section">Dashboard · {m}</div>',unsafe_allow_html=True)
    c=st.columns(5)
    c[0].metric("Income",money(inc)); c[1].metric("Expenses",money(exp)); c[2].metric("Net",money(net))
    c[3].metric("Committed",money(sum(b["amount"] for _,b in st.session_state.bills.iterrows())) if len(st.session_state.bills) else "₹0")
    c[4].metric("Goals",len(st.session_state.goals))
    if net<0: st.warning("Recorded expenses exceed income for the selected month.")
    else: st.success(f"Recorded cash flow is positive by {money(net)} this month.")
    a,b=st.columns([1.2,1])
    with a:
        st.markdown('<div class="card"><b>Where money went</b></div>',unsafe_allow_html=True)
        st.bar_chart(category_total(m).head(8))
    with b:
        st.markdown('<div class="card"><b>Agent snapshot</b></div>',unsafe_allow_html=True)
        cats=category_total(m)
        if len(cats):
            st.markdown(f"<div class='insight'><b>{cats.index[0]}</b> is your largest spending category at <b>{money(cats.iloc[0])}</b>.</div>",unsafe_allow_html=True)
        st.markdown("<div class='card'><b>Next:</b> Review recurring payments, then check Budget vs Actual and Monthly Compare.</div>",unsafe_allow_html=True)
    st.markdown('<div class="section">Cash flow</div>',unsafe_allow_html=True)
    st.line_chart(df.groupby("date").amount.sum())

# ---------------- Transactions ----------------
elif st.session_state.page=="Transactions":
    st.markdown('<div class="section">Transactions</div>',unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    typ=f1.multiselect("Type",sorted(df.type.unique()),default=sorted(df.type.unique()))
    cat=f2.multiselect("Category",sorted(df.category.unique()),default=sorted(df.category.unique()))
    q=f3.text_input("Search")
    view=df[df.type.isin(typ)&df.category.isin(cat)]
    if q: view=view[view.description.str.contains(q,case=False,na=False)]
    st.dataframe(view.sort_values("date",ascending=False),use_container_width=True,hide_index=True)
    st.download_button("Export filtered CSV",view.to_csv(index=False).encode(),"finpilot_filtered.csv","text/csv")
    st.markdown("### Add transaction")
    with st.form("tx"):
        a,b,c=st.columns(3); d=a.date_input("Date",date.today()); desc=b.text_input("Description"); amt=c.number_input("Amount",min_value=0.0,step=100.0)
        d1,d2,d3=st.columns(3); typ2=d1.selectbox("Type",["Expense","Income"]); cat2=d2.selectbox("Category",CATEGORIES); note=d3.text_input("Notes")
        if st.form_submit_button("Add"):
            if desc and amt:
                row=pd.DataFrame([[pd.Timestamp(d),desc,amt if typ2=="Income" else -amt,typ2,cat2,note]],columns=df.columns)
                st.session_state.df=pd.concat([df,row],ignore_index=True); st.rerun()

# ---------------- Spending ----------------
elif st.session_state.page=="Spending":
    m=st.selectbox("Month",months(),index=len(months())-1)
    st.markdown(f'<div class="section">Spending · {m}</div>',unsafe_allow_html=True)
    x=category_total(m)
    if len(x):
        st.bar_chart(x)
        total=x.sum()
        tbl=pd.DataFrame({"Amount":x.map(money),"Share":(x/total*100).round(1).astype(str)+"%"})
        st.dataframe(tbl,use_container_width=True)
        st.markdown("### Largest transactions")
        st.dataframe(df[(df.type=="Expense")&(df.date.dt.to_period("M").astype(str)==m)].assign(Amount=lambda z:z.amount.abs()).sort_values("Amount",ascending=False).head(10),use_container_width=True,hide_index=True)

# ---------------- Recurring ----------------
elif st.session_state.page=="Recurring & Subscriptions":
    st.markdown('<div class="section">Recurring payments & subscriptions</div>',unsafe_allow_html=True)
    exp=df[df.type=="Expense"].copy()
    groups=exp.groupby("description").agg(occurrences=("description","size"),avg_amount=("amount",lambda s:s.abs().mean()),last_seen=("date","max"))
    rec=groups[groups.occurrences>=2].sort_values(["occurrences","avg_amount"],ascending=False)
    if len(rec):
        st.markdown("### Detected recurring patterns")
        st.dataframe(rec.assign(avg_amount=rec.avg_amount.map(money)),use_container_width=True)
        st.caption("A recurring signal means the same description appears at least twice. It is a detection signal, not a guarantee of subscription status.")
    else: st.info("More transaction history is needed to detect recurring patterns.")
    st.markdown("### Add a subscription manually")
    with st.form("sub"):
        a,b,c=st.columns(3); name=a.text_input("Name"); amount=b.number_input("Amount",min_value=0.0,step=50.0); freq=c.selectbox("Frequency",["Monthly","Yearly","Weekly"])
        if st.form_submit_button("Add subscription") and name and amount:
            new=pd.DataFrame([[name,amount,"",freq,"Subscriptions"]],columns=st.session_state.bills.columns)
            st.session_state.bills=pd.concat([st.session_state.bills,new],ignore_index=True)
            st.success("Added.")

# ---------------- Bills ----------------
elif st.session_state.page=="Bills":
    st.markdown('<div class="section">Bills & upcoming obligations</div>',unsafe_allow_html=True)
    st.write("Upload a bill/expense CSV separately or add known obligations. Bills are kept separate from transactions so the agent can distinguish paid history from upcoming commitments.")
    bill_upload=st.file_uploader("Upload bills CSV/XLSX",type=["csv","xlsx","xls"],key="bills_upload")
    if bill_upload:
        try:
            raw=pd.read_csv(bill_upload) if bill_upload.name.endswith(".csv") else pd.read_excel(bill_upload)
            cols={str(c).lower().strip():c for c in raw.columns}
            required=[k for k in ["name","amount"] if k not in cols]
            if required: st.error("Bills file needs at least Name and Amount columns.")
            else:
                out=pd.DataFrame({
                    "name":raw[cols["name"]].astype(str),
                    "amount":pd.to_numeric(raw[cols["amount"]],errors="coerce").abs(),
                    "due_date":raw[cols["due date"]] if "due date" in cols else "",
                    "frequency":raw[cols["frequency"]] if "frequency" in cols else "Monthly",
                    "category":raw[cols["category"]] if "category" in cols else "Bills"
                }).dropna(subset=["amount"])
                st.session_state.bills=out
                st.success(f"Loaded {len(out)} obligations.")
        except Exception as e: st.error(str(e))
    with st.form("bill_add"):
        a,b,c,d=st.columns(4); name=a.text_input("Bill"); amount=b.number_input("Amount",min_value=0.0,step=100.0); due=c.text_input("Due date/day"); freq=d.selectbox("Frequency",["Monthly","Yearly","One-time"])
        if st.form_submit_button("Add bill") and name and amount:
            row=pd.DataFrame([[name,amount,due,freq,"Bills"]],columns=st.session_state.bills.columns)
            st.session_state.bills=pd.concat([st.session_state.bills,row],ignore_index=True)
    if len(st.session_state.bills):
        st.dataframe(st.session_state.bills,use_container_width=True,hide_index=True)
        committed=st.session_state.bills.amount.sum()
        st.markdown(f"<div class='card'><div class='big'>{money(committed)}</div><div class='muted'>Total tracked obligation amount</div></div>",unsafe_allow_html=True)
    else: st.info("No upcoming obligations added yet.")

# ---------------- Budgets ----------------
elif st.session_state.page=="Budgets":
    m=st.selectbox("Month",months(),index=len(months())-1)
    actual=category_total(m)
    st.markdown('<div class="section">Budget vs actual</div>',unsafe_allow_html=True)
    for cat in sorted(set(CATEGORIES)|set(actual.index)):
        a,b,c=st.columns([1.2,1,1])
        a.write(cat)
        old=float(st.session_state.budgets.get(cat,0))
        val=b.number_input("Budget",min_value=0.0,value=old,step=500.0,key=f"bud_{cat}")
        st.session_state.budgets[cat]=val
        act=float(actual.get(cat,0))
        if val:
            pct=act/val*100
            cls="bad" if pct>100 else ("warn" if pct>=80 else "good")
            c.markdown(f"<span class='{cls}'>{pct:.0f}% used</span><br><span class='muted'>{money(act)} / {money(val)}</span>",unsafe_allow_html=True)
    st.info("Budget indicators describe your recorded spending against limits you set; they are not financial advice.")

# ---------------- Goals ----------------
elif st.session_state.page=="Goals":
    st.markdown('<div class="section">Goals & spending impact</div>',unsafe_allow_html=True)
    with st.form("goal"):
        a,b,c,d=st.columns(4); name=a.text_input("Goal"); target=b.number_input("Target",min_value=0.0,step=1000.0); current=c.number_input("Saved",min_value=0.0,step=1000.0); monthly=d.number_input("Planned monthly contribution",min_value=0.0,step=500.0)
        if st.form_submit_button("Create goal") and name and target:
            st.session_state.goals.append({"name":name,"target":target,"current":current,"monthly":monthly})
    for g in st.session_state.goals:
        remaining=max(0,g["target"]-g["current"])
        months_needed=(remaining/g["monthly"]) if g["monthly"] else None
        exp=month_stats(current_month())[1]
        st.markdown(f"<div class='card'><h3>🎯 {g['name']}</h3><p>{money(g['current'])} saved of {money(g['target'])}</p></div>",unsafe_allow_html=True)
        st.progress(min(1,g["current"]/g["target"]) if g["target"] else 0)
        if months_needed is not None:
            st.markdown(f"<div class='insight'>At the planned contribution of <b>{money(g['monthly'])}/month</b>, the remaining amount is approximately <b>{months_needed:.1f} months</b> of contributions.</div>",unsafe_allow_html=True)
        st.caption("This is a simple arithmetic scenario based on the amount you entered; it does not predict returns or recommend financial products.")
    if not st.session_state.goals: st.info("Create a goal to see how current spending and planned contributions relate to it.")

# ---------------- Monthly Compare ----------------
elif st.session_state.page=="Monthly Compare":
    ms=months()
    st.markdown('<div class="section">Month-over-month comparison</div>',unsafe_allow_html=True)
    if len(ms)<2:
        st.info("Upload at least two months of transactions to compare changes.")
    else:
        m2=st.selectbox("Current month",ms,index=len(ms)-1)
        idx=ms.index(m2); m1=ms[idx-1]
        i1,e1,n1=month_stats(m1); i2,e2,n2=month_stats(m2)
        c=st.columns(4); c[0].metric("Income change",money(i2-i1),delta=f"{(i2-i1):,.0f}"); c[1].metric("Expense change",money(e2-e1),delta=f"{e2-e1:,.0f}"); c[2].metric("Net change",money(n2-n1)); c[3].metric("Expense % change",f"{((e2/e1-1)*100 if e1 else 0):.1f}%")
        a=category_total(m1); b=category_total(m2)
        comp=pd.concat([a.rename(m1),b.rename(m2)],axis=1).fillna(0)
        comp["Change"]=comp[m2]-comp[m1]
        comp["Change %"]=np.where(comp[m1]!=0,comp["Change"]/comp[m1]*100,np.nan)
        comp=comp.sort_values("Change",ascending=False)
        st.markdown("### What increased?")
        st.dataframe(comp.style.format({m1:"₹{:,.0f}",m2:"₹{:,.0f}","Change":"₹{:,.0f}","Change %":"{:.1f}%"}),use_container_width=True)
        top=comp.iloc[0]
        if top["Change"]>0: st.warning(f"{comp.index[0]} increased the most, by {money(top['Change'])}.")
        else: st.success("No spending category increased in the comparison.")

# ---------------- Agent Insights ----------------
elif st.session_state.page=="Agent Insights":
    st.markdown('<div class="section">🤖 FinPilot Agent</div>',unsafe_allow_html=True)
    m=current_month(); inc,exp,net=month_stats(m); cats=category_total(m)
    st.markdown("""
    <div class="agent">
    <b>Agent role:</b> observe your records → detect patterns → explain evidence → surface upcoming commitments → connect spending with goals → suggest what to review next.
    </div>""",unsafe_allow_html=True)
    if len(cats):
        st.markdown(f"<div class='card'><h3>Priority 1 · Spending concentration</h3><p>{cats.index[0]} is your largest category at <b>{money(cats.iloc[0])}</b>.</p><span class='muted'>Evidence: current-month transaction totals.</span></div>",unsafe_allow_html=True)
    expdf=df[df.type=="Expense"]
    if len(expdf)>=5:
        mean=expdf.amount.abs().mean(); sd=expdf.amount.abs().std()
        unusual=expdf[expdf.amount.abs()>mean+2*sd]
        st.markdown(f"<div class='card'><h3>Priority 2 · Unusual spending</h3><p>{len(unusual)} transaction(s) exceed the dataset's local statistical threshold.</p><span class='muted'>Rule: amount > mean + 2×standard deviation. This is a review signal, not a fraud claim.</span></div>",unsafe_allow_html=True)
    if len(st.session_state.bills):
        committed=st.session_state.bills.amount.sum()
        st.markdown(f"<div class='card'><h3>Priority 3 · Upcoming commitments</h3><p><b>{money(committed)}</b> is currently tracked as upcoming/recurring obligations.</p></div>",unsafe_allow_html=True)
    st.markdown("### Agent action queue")
    actions=[]
    if len(cats): actions.append(f"Review {cats.index[0]} spending because it is the largest current category.")
    if len(months())>=2: actions.append("Open Monthly Compare to inspect categories that changed versus the previous month.")
    if len(st.session_state.budgets): actions.append("Review categories approaching their user-defined limits.")
    if len(st.session_state.goals): actions.append("Open Goals to see the simple contribution scenario for your goal.")
    actions.append("Review recurring payments and confirm that repeated merchants are expected.")
    for a in actions: st.markdown(f"• {a}")

# ---------------- Ask ----------------
elif st.session_state.page=="Ask FinPilot":
    st.markdown('<div class="section">💬 Ask FinPilot</div>',unsafe_allow_html=True)
    st.caption("Answers are calculated from the transaction/bill data loaded into this session.")
    q=st.text_input("Question",placeholder="Where did I spend the most this month?")
    if q:
        x=q.lower(); m=current_month(); cats=category_total(m); exp=df[df.type=="Expense"]
        if "most" in x and ("spend" in x or "spent" in x):
            st.markdown(f"<div class='card'>You spent the most on <b>{cats.index[0]}</b> this month: <b>{money(cats.iloc[0])}</b>.</div>",unsafe_allow_html=True)
        elif "subscription" in x:
            sub=exp[exp.category=="Subscriptions"].groupby("description").amount.sum().abs().sort_values(ascending=False)
            if len(sub): st.dataframe(sub.rename("Amount").map(money),use_container_width=True)
            else: st.info("No subscription transactions were detected.")
        elif "increased" in x or "compared" in x:
            ms=months()
            if len(ms)<2: st.info("Need at least two months.")
            else:
                prev=ms[-2]; a=category_total(prev); b=cats
                comp=(b-a).fillna(b).sort_values(ascending=False)
                st.write("Largest increases:",comp.head(5).map(money))
        elif "budget" in x or "committed" in x:
            budget=sum(st.session_state.budgets.values()); used=cats.sum()
            committed=st.session_state.bills.amount.sum() if len(st.session_state.bills) else 0
            st.markdown(f"<div class='card'><b>Recorded expenses:</b> {money(used)}<br><b>Tracked upcoming/recurring obligations:</b> {money(committed)}<br><b>Total budget limits entered:</b> {money(budget)}</div>",unsafe_allow_html=True)
        else:
            st.info("Try: “Where did I spend the most this month?”, “Which subscriptions am I paying for?”, “What expenses increased compared with last month?”, or “How much of my budget is already committed?”")

# ---------------- Monthly Report ----------------
elif st.session_state.page=="Monthly Report":
    m=current_month(); inc,exp,net=month_stats(m); cats=category_total(m)
    st.markdown(f'<div class="section">Monthly financial summary · {m}</div>',unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
    <h2>FinPilot monthly summary</h2>
    <p><b>Income:</b> {money(inc)} &nbsp; <b>Expenses:</b> {money(exp)} &nbsp; <b>Net:</b> {money(net)}</p>
    </div>""",unsafe_allow_html=True)
    st.markdown("### Key observations")
    obs=[]
    if len(cats): obs.append(f"{cats.index[0]} was the largest category at {money(cats.iloc[0])}.")
    if net<0: obs.append("Recorded expenses were higher than recorded income.")
    else: obs.append(f"Recorded cash flow remained positive by {money(net)}.")
    if len(months())>=2:
        prev=months()[-2]; pc=category_total(prev)
        common=(cats-pc).dropna().sort_values(ascending=False)
        if len(common) and common.iloc[0]>0: obs.append(f"{common.index[0]} increased versus the previous month by {money(common.iloc[0])}.")
    for o in obs: st.markdown(f"• {o}")
    st.markdown("### Action items")
    actions=["Review recurring payments and confirm each is still needed.","Check Budget vs Actual for categories near their limits.","Review the largest spending category and inspect the underlying transactions."]
    if len(st.session_state.goals): actions.append("Review your goal contribution scenario after considering this month's actual spending.")
    for a in actions: st.markdown(f"• {a}")
    st.caption("This report describes the data and produces review prompts. It does not provide investment, tax, credit, insurance or other professional financial advice.")

st.divider()
st.caption("FinPilot • Personal finance understanding & decision support • Not investment or financial advice")
