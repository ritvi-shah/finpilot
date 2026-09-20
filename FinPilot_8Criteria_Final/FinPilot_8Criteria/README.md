# ✨ FinPilot

**FinPilot** is a premium, AI-powered personal finance dashboard that turns your raw financial data into a clear, actionable, and visually stunning picture of your spending, commitments, cash flow, and goals. 

With a beautiful, state-of-the-art glassmorphism UI and a smart built-in Chatbot, managing your money has never felt this futuristic.

![FinPilot Demo Background](https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=1200&auto=format&fit=crop)

---

## 🚀 Features

- **Beautiful Analytics Dashboard:** Visualize your cash flow and categorized expenses through interactive, dynamic charts.
- **Smart AI Chatbot Engine:** Don't just look at data, *talk* to it. Ask the built-in AI for personalized financial advice, how much you saved, or what your largest expenses are.
- **Seamless Data Import:** Easily drag & drop your bank statement CSVs, or manually add transactions on the fly.
- **Goal Tracking:** Set and track custom financial goals (like a Vacation Fund or Emergency Savings).
- **Premium Aesthetics:** Fully custom CSS featuring glowing mesh gradients, frosted glass sidebars, animated SVGs, and ultra-smooth micro-animations.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Pandas (for lightning-fast CSV normalization and data crunching)
- **Frontend:** Vanilla HTML, CSS, and JavaScript
- **Visuals:** Chart.js for data visualization, custom SVG, and advanced CSS Grid/Flexbox layouts.

---

## ⚙️ Local Setup & Installation

To run FinPilot locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/FinPilot.git
   cd FinPilot/FinPilot_8Criteria
   ```

2. **Install Python Dependencies:**
   Make sure you have Python installed, then install the required backend packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure `flask` and `pandas` are installed)*

3. **Start the Backend Server:**
   The Python server handles the AI logic and data processing.
   ```bash
   python server.py
   ```
   *The Flask server will start on port 5000.*

4. **Start the Frontend Server:**
   Open a new terminal window/tab, navigate to the `frontend` folder, and start a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```

5. **Open the App:**
   Open your browser and navigate to `http://localhost:8000`

---

## 📊 Demo Mode

Want to test the app without using your real bank data? We've included a sample dataset for you!

1. Locate the `demo_data.csv` file in the root directory.
2. Open the app in your browser.
3. Drag and drop `demo_data.csv` into the upload zone to instantly populate the dashboard with 25 realistic transactions!
4. Head over to the **Ask FinPilot** tab and try asking: *"How can I save money?"*

---

## 📝 License

This project is open-source and available under the MIT License.
