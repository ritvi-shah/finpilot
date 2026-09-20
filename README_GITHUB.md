# 💳 FinPilot - AI-Powered Personal Finance Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](#)

> **Transform scattered financial data into one clear, actionable picture of your spending, savings, and financial goals.**

![FinPilot Dashboard](https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=1200&auto=format&fit=crop)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Development](#-development)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Overview

**FinPilot** solves a fundamental financial problem: people have data everywhere (bank statements, card statements, bills, subscriptions, spreadsheets) but it's disconnected and unactionable.

FinPilot turns those records into **one explainable financial workspace** where you can:
- 📊 Visualize spending patterns across categories
- 💰 Track budgets vs actual spending
- 🎯 Set and monitor savings goals
- 📈 Analyze monthly cash flow trends
- 🤖 Get AI-powered financial insights
- 💬 Ask natural language questions about your finances

### Why FinPilot?

✅ **Zero-Trust Architecture** - All data processing happens locally. No cloud storage, no bank credentials required.  
✅ **Smart Categorization** - Automatic transaction categorization with customizable rules.  
✅ **Intuitive UI** - Premium glassmorphism design with smooth animations and responsive layouts.  
✅ **No Subscriptions** - Self-hosted, open-source solution you control completely.  
✅ **Fast & Lightweight** - Runs on any machine without heavy dependencies.  

---

## 🚀 Features

### 💻 Dashboard Analytics
- **Real-time Summary Cards** - Income, expenses, net balance, committed bills at a glance
- **Interactive Charts** - Category breakdown and cash flow trends
- **Smart Insights** - AI-generated observations about your spending patterns
- **Savings Rate Calculation** - Track what percentage of income you're saving

### 📝 Transaction Management
- **CSV/Excel Import** - Drag & drop bank statements in any format
- **Manual Entry** - Quickly add transactions with auto-categorization
- **Smart Normalization** - Handles multiple CSV formats automatically
- **Description Optional** - Auto-fills with "Unnamed Transaction" when skipped
- **Flexible Categorization** - 10 built-in categories with rule-based classification

### 🎯 Budget & Goals
- **Budget Tracking** - Set monthly limits per category
- **Over-Budget Alerts** - Visual indicators for spending limits exceeded
- **Recurring Transaction Detection** - Identify subscriptions and regular payments
- **Savings Goals** - Track progress toward financial objectives
- **Goal Timeline** - Calculate months to reach each goal

### 🤖 AI Assistant
- **Natural Language Queries** - Ask "How can I save money?" or "What's my biggest expense?"
- **Contextual Insights** - AI analyzes your data to provide actionable advice
- **Pattern Recognition** - Identifies unusual spending spikes
- **Multi-modal Responses** - Formatted with markdown for readability

### 🎨 User Experience
- **Premium UI** - Glassmorphism design with glowing gradients
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Real-time Updates** - Instant dashboard refresh after adding transactions
- **Smooth Animations** - Polished micro-interactions and transitions
- **Dark Mode** - Eye-friendly interface optimized for all lighting conditions

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic structure
- **CSS3** - Glassmorphism, gradients, animations, Grid/Flexbox
- **Vanilla JavaScript (ES6+)** - No frameworks, lightweight bundle
- **Chart.js** - Interactive data visualizations
- **Marked.js** - Markdown rendering for AI responses

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0+** - Lightweight web framework
- **Pandas 2.1+** - Data processing and analysis
- **NumPy 1.26+** - Numerical computations
- **Flask-CORS 4.0+** - Cross-origin request handling

### Data Storage
- **In-Memory State** (Prototype) - For hackathon/demo purposes
- **CSV/Excel Support** - Multiple import formats

### DevOps
- **Python HTTP Server** - Simple frontend hosting
- **Flask Development Server** - Backend API
- **CORS** - Secure cross-origin communication

---

## 📁 Project Structure

```
FinPilot/
├── README.md                 # This file
├── PITCH.md                  # 60-second elevator pitch
├── requirements.txt          # Python dependencies
│
├── Backend API
├── server.py                 # Flask API server (port 5000)
└── app.py                    # Core business logic
│
├── Frontend
├── index.html                # Main HTML template
├── app.js                    # JavaScript application logic
├── styles.css                # Custom CSS styling
│
├── Data Files (Examples)
├── demo_data.csv             # Sample transactions for testing
├── sample_transactions.csv   # Example bank statement
└── sample_bills.csv          # Example recurring bills

```

### Key Files Explained

| File | Purpose | Size |
|------|---------|------|
| `server.py` | Flask API with all endpoints | ~340 lines |
| `app.py` | Core logic (normalization, classification, calculations) | ~600 lines |
| `app.js` | Frontend application state and interactions | ~650 lines |
| `index.html` | Complete HTML structure with forms and sections | ~500 lines |
| `styles.css` | Premium CSS with animations and responsive design | ~800 lines |

---

## 💾 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Git** (for cloning the repository)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/FinPilot.git
cd FinPilot
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `flask>=3.0` - Web server
- `flask-cors>=4.0` - CORS handling
- `pandas>=2.1` - Data processing
- `numpy>=1.26` - Numerical computing
- `openpyxl>=3.1` - Excel file support
- `streamlit>=1.38,<2` - Optional (not currently used)

### Step 4: Verify Installation

```bash
# Check Flask
python -c "import flask; print(f'Flask {flask.__version__} installed')"

# Check Pandas
python -c "import pandas; print(f'Pandas {pandas.__version__} installed')"
```

---

## 🚀 Quick Start

### 1️⃣ Start Backend Server

```bash
python server.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**The backend is now listening on:** `http://localhost:5000/api`

### 2️⃣ Start Frontend Server (New Terminal)

```bash
# Navigate to project directory
cd path/to/FinPilot

# Start simple HTTP server on port 8000
python -m http.server 8000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**The frontend is now available at:** `http://localhost:8000`

### 3️⃣ Open in Browser

Navigate to: **http://localhost:8000**

### 4️⃣ Load Demo Data

1. Click the **Upload Statement** card
2. Drag & drop `demo_data.csv` or select it manually
3. Click **Upload & Analyse**
4. Dashboard will auto-populate with 25 sample transactions

### 5️⃣ Try the Features

- 📊 **Dashboard** - View summary and charts
- 💳 **Transactions** - Add more transactions or upload CSVs
- 🎯 **Budgets & Subs** - Set budgets and see recurring payments
- 🚀 **Goals** - Create savings goals
- 💬 **Ask FinPilot** - Chat with AI about your finances

---

## 📖 Usage Guide

### Adding Transactions Manually

1. Go to **💳 Transactions** tab
2. Click **➕ Add Manually**
3. Fill in:
   - **Date** - Transaction date (required)
   - **Amount** - Transaction amount in ₹ (required)
   - **Description** - Optional (auto-fills as "Unnamed Transaction" if empty)
   - **Type** - Income or Expense
   - **Category** - Pre-selected category or choose from dropdown
4. Click **Add Transaction**
5. Dashboard updates instantly

### Uploading Bank Statements

**Supported Formats:**
- CSV files (.csv)
- Excel files (.xlsx, .xls)

**Required Columns:**
- `Date` or `Transaction Date` or `Txn Date`
- `Amount` or `Transaction Amount` or `Value`

**Optional Columns:**
- `Description` or `Merchant` or `Payee` or `Narration`
- `Type` or `Transaction Type` or `Credit/Debit`
- `Category` or `Category Name`
- `Notes` or `Remarks`

**Example CSV Format:**
```
Date,Description,Amount,Type,Category
2024-01-15,Swiggy Food Order,450,Expense,Food
2024-01-14,Netflix Subscription,199,Expense,Subscriptions
2024-01-13,Monthly Salary,50000,Income,Salary
```

### Setting Budgets

1. Go to **🎯 Budgets & Subs**
2. Scroll to **🎯 Set a Budget**
3. Select category
4. Enter monthly limit in ₹
5. Click **Save Budget**
6. View budget tracking bars with color indicators:
   - 🟢 Green: < 70% of limit
   - 🟡 Yellow: 70-89% of limit
   - 🔴 Red: ≥ 90% of limit

### Creating Savings Goals

1. Go to **🚀 Goals**
2. Fill in goal details:
   - **Goal Name** - e.g., "Vacation Fund"
   - **Target Amount** - Total goal in ₹
   - **Already Saved** - Current amount saved
   - **Monthly Contribution** - How much to save per month
3. Click **Add Goal**
4. View progress bar and timeline to goal

### Using AI Assistant

1. Go to **💬 Ask FinPilot**
2. Type a question, e.g.:
   - "How much did I spend on food?"
   - "What's my biggest expense?"
   - "How can I save money?"
   - "Show me my savings rate"
   - "Which category am I over budget in?"
3. Press **Send**
4. AI analyzes your data and responds with insights

---

## 🔌 API Reference

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Upload Transactions
```http
POST /api/upload
Content-Type: multipart/form-data

file: <CSV or Excel file>
```

**Response:**
```json
{
  "success": true,
  "message": "X transactions imported",
  "count": 25
}
```

---

#### Add Single Transaction
```http
POST /api/add_transaction
Content-Type: application/json

{
  "date": "2024-01-15",
  "description": "Swiggy Order",
  "amount": 450,
  "type": "Expense",
  "category": "Food",
  "notes": ""
}
```

**Response:**
```json
{
  "success": true,
  "message": "Transaction added",
  "transaction_id": 1
}
```

---

#### Get Dashboard Data
```http
GET /api/dashboard
```

**Response:**
```json
{
  "empty": false,
  "income": 50000,
  "expenses": 7850,
  "net": 42150,
  "committed": 0,
  "category_totals": {
    "Food": 2500,
    "Shopping": 1500,
    "Bills": 1850,
    "Entertainment": 1000
  },
  "cash_flow": {
    "2024-01-01": 50000,
    "2024-01-15": 42150
  }
}
```

---

#### Get Transactions
```http
GET /api/transactions
```

**Response:**
```json
[
  {
    "date": "2024-01-15 14:30:00",
    "description": "Swiggy Order",
    "category": "Food",
    "type": "Expense",
    "amount": 450
  }
]
```

---

#### Get Budgets
```http
GET /api/budgets
```

**Response:**
```json
{
  "budgets": {
    "Food": 5000,
    "Shopping": 3000,
    "Entertainment": 2000
  },
  "actuals": {
    "Food": 2500,
    "Shopping": 1500,
    "Entertainment": 800
  }
}
```

---

#### Set Budget
```http
POST /api/budgets
Content-Type: application/json

{
  "category": "Food",
  "amount": 5000
}
```

---

#### Get Goals
```http
GET /api/goals
```

**Response:**
```json
[
  {
    "name": "Vacation Fund",
    "target": 100000,
    "current": 25000,
    "monthly": 5000
  }
]
```

---

#### Add Goal
```http
POST /api/goals
Content-Type: application/json

{
  "name": "Vacation Fund",
  "target": 100000,
  "current": 25000,
  "monthly": 5000
}
```

---

#### Ask AI
```http
POST /api/ask
Content-Type: application/json

{
  "query": "How much did I spend on food?"
}
```

**Response:**
```json
{
  "response": "You spent ₹2,500 on food this month, with 15 transactions including..."
}
```

---

#### Reset All Data
```http
POST /api/reset
```

**Response:**
```json
{
  "success": true,
  "message": "All data cleared"
}
```

---

#### Frequent Transactions
```http
GET /api/frequent_transactions
```

**Response:**
```json
[
  {
    "description": "Netflix Subscription",
    "category": "Subscriptions",
    "amount": 199,
    "count": 3,
    "total": 597
  }
]
```

---

## ⚙️ Configuration

### Backend Configuration

Edit `server.py` to customize:

#### Transaction Categories
```python
CATEGORIES = [
    "Housing", "Food", "Transport", "Shopping", "Bills", 
    "Health", "Education", "Entertainment", "Subscriptions", "Other"
]
```

#### Classification Rules
```python
rules = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe", "food", ...],
    "Transport": ["uber", "ola", "rapido", "metro", ...],
    # Add your own merchant keywords
}
```

#### Server Port
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change port here
```

### Frontend Configuration

Edit `app.js`:

#### API Base URL
```javascript
const API_BASE = 'http://localhost:5000/api';  // Change if backend port differs
```

#### Currency Format
```javascript
const formatMoney = (amount) =>
    new Intl.NumberFormat('en-IN', {  // Change 'en-IN' to your locale
        style: 'currency', 
        currency: 'INR',  // Change 'INR' to your currency
        maximumFractionDigits: 0
    }).format(Math.abs(amount));
```

---

## 🔧 Development

### Project Architecture

#### Frontend Flow
```
User Action
    ↓
Event Handler (app.js)
    ↓
Validation & Data Prep
    ↓
Fetch API Call → Backend
    ↓
Handle Response
    ↓
Update UI / Charts
    ↓
Show Toast Notification
```

#### Backend Flow
```
HTTP Request
    ↓
Route Handler (server.py)
    ↓
Data Validation
    ↓
Process Data (app.py)
    ↓
Calculate Metrics
    ↓
Return JSON Response
```

### Key Functions

#### Frontend (app.js)

| Function | Purpose |
|----------|---------|
| `loadDashboard()` | Fetch and render dashboard data |
| `loadTransactions()` | Display transaction history |
| `loadBudgets()` | Show budgets and subscriptions |
| `loadGoals()` | Display savings goals |
| `showToast()` | Display notifications |

#### Backend (app.py)

| Function | Purpose |
|----------|---------|
| `normalize()` | Clean and standardize CSV data |
| `classify()` | Auto-categorize transactions |
| `month_stats()` | Calculate monthly metrics |
| `frequent_tx()` | Detect recurring transactions |

### Adding New Features

**Example: Add a new category**

1. **Update backend** (server.py):
```python
CATEGORIES = [..., "NewCategory"]
rules = {
    ...,
    "NewCategory": ["keyword1", "keyword2"]
}
```

2. **Update frontend** (index.html):
```html
<select id="tx-cat">
    ...
    <option value="NewCategory">NewCategory</option>
</select>
```

3. **Update charts** (app.js):
```javascript
// Add color in chart configuration
backgroundColor: [..., '#your-color']
```

---

## 🐛 Troubleshooting

### "Failed to load dashboard" Error

**Problem:** Dashboard doesn't load after importing data

**Solutions:**
1. Verify backend is running: `python server.py` should show "Running on http://127.0.0.1:5000"
2. Check browser console (F12) for error messages
3. Verify CORS is enabled (check server.py has `CORS(app)`)
4. Check network tab (F12) to see if API calls are succeeding

---

### "Cannot reach the server" Error

**Problem:** Frontend can't connect to backend

**Solutions:**
1. Ensure backend is running on port 5000
2. Check firewall isn't blocking localhost:5000
3. Verify `API_BASE` in app.js points to correct URL
4. Try `http://127.0.0.1:5000` instead of `http://localhost:5000`

---

### CSV Upload Not Working

**Problem:** File upload returns error

**Solutions:**
1. Verify CSV has required columns: `Date` and `Amount`
2. Check date format is standard (YYYY-MM-DD or MM/DD/YYYY)
3. Check amounts are numeric (remove currency symbols from CSV before upload)
4. Try with `demo_data.csv` to verify setup works
5. Check server console for error messages

---

### Chart Not Displaying

**Problem:** Dashboard loads but charts are empty

**Solutions:**
1. Ensure data is uploaded successfully
2. Check if transactions exist: go to Transactions tab
3. Clear browser cache (Ctrl+Shift+Delete)
4. Refresh page
5. Verify Chart.js is loaded (check network tab in F12)

---

### Transaction Description Issues

**Problem:** Description field behavior

**Solutions:**
- Description is OPTIONAL - leave blank to auto-fill "Unnamed Transaction"
- For CSV imports, missing descriptions auto-fill as "Unlabeled Transaction"
- Both work identically in analytics and dashboards

---

### Port Already in Use

**Problem:** "Address already in use" error

**Solutions:**

**Find what's using the port:**

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

macOS/Linux:
```bash
lsof -i :5000
kill -9 <PID>
```

**Or use different ports:**

Backend:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed from 5000
```

Frontend (app.js):
```javascript
const API_BASE = 'http://localhost:5001/api';  // Updated to match
```

---

## 📝 Contributing

### How to Contribute

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/FinPilot.git
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
- Follow existing code style
- Add comments for complex logic
- Test thoroughly with demo data

4. **Commit changes**
```bash
git commit -m "Add: descriptive message of changes"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create Pull Request**
- Describe what you changed
- Reference any related issues
- Add screenshots if UI changes

### Code Style Guide

**Python:**
- Follow PEP 8
- Use snake_case for functions
- Add docstrings to functions

**JavaScript:**
- Use camelCase for variables
- Use const/let (no var)
- Add comments for complex logic

**CSS:**
- Use custom properties for colors
- Mobile-first design approach
- Use semantic selectors

### Reporting Bugs

Create an issue with:
- Clear title describing the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, browser)

### Feature Requests

Create an issue with:
- Clear title describing the feature
- Why you need it
- How it would work
- Example use cases

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

✅ **You can:**
- Use commercially
- Modify the code
- Distribute copies
- Use privately

⚠️ **You must:**
- Include the license and copyright notice
- State significant changes

❌ **You cannot:**
- Hold liable the authors

---

## 🙌 Acknowledgments

- **Pandas** - Data processing powerhouse
- **Flask** - Lightweight Python framework
- **Chart.js** - Beautiful data visualizations
- **Community** - Feedback and contributions

---

## 📞 Support

### Getting Help

1. **Check FAQ** - See Troubleshooting section above
2. **Review Issues** - Search existing GitHub issues
3. **Read Documentation** - Check README and code comments
4. **Create Issue** - If problem persists, open a GitHub issue

### Contact

- **Email:** your-email@example.com
- **GitHub Issues:** [Project Issues](https://github.com/yourusername/FinPilot/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/FinPilot/discussions)

---

## 🗺️ Roadmap

### v1.1 (Planned)
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication & multi-user support
- [ ] Transaction editing & deletion
- [ ] Custom category creation
- [ ] Export reports as PDF
- [ ] Mobile app (React Native)

### v1.2 (Planned)
- [ ] Investment tracking
- [ ] Multi-currency support
- [ ] Budget alerts & notifications
- [ ] Advanced analytics (forecasting)
- [ ] API for third-party integrations

### v2.0 (Future)
- [ ] Machine learning for anomaly detection
- [ ] Real-time bank API integration
- [ ] Advanced financial advice engine
- [ ] Social features (expense splitting)
- [ ] Voice commands

---

## 📊 Project Statistics

- **Lines of Code:** ~2,300+
- **Files:** 11 (Frontend: 3, Backend: 2, Data: 6)
- **Dependencies:** 6 core packages
- **Features:** 50+
- **API Endpoints:** 10+

---

## 🎓 Learning Resources

### Understanding the Code

1. **Start with:** `README.md` (this file)
2. **Frontend:** Read `app.js` top-to-bottom
3. **Backend:** Read `server.py` to understand routes
4. **Data Processing:** Check `app.py` for business logic

### Topics Covered

- ✅ REST API design (Flask)
- ✅ Frontend-backend communication (Fetch API)
- ✅ Data processing (Pandas)
- ✅ CSV/Excel handling
- ✅ Data visualization (Chart.js)
- ✅ CSS animations & design
- ✅ JavaScript ES6+ patterns
- ✅ CORS & security basics

---

**Made with ❤️ for financial transparency and personal empowerment.**

Last Updated: January 2024  
Version: 1.0.0  
Status: Active Development
