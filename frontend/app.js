const API_BASE = 'http://localhost:5000/api';

// Navigation
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view');

navItems.forEach(item => {
    item.addEventListener('click', () => {
        // Update active nav
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');

        // Show target view
        const targetId = item.getAttribute('data-target');
        views.forEach(view => {
            view.classList.remove('active');
            if (view.id === targetId) {
                view.classList.add('active');
            }
        });

        // Load data if needed
        if (targetId === 'transactions') {
            loadTransactions();
        }
    });
});

// Format currency
const formatMoney = (amount) => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(Math.abs(amount));
};

let categoryChartInstance = null;
let flowChartInstance = null;

// Load Dashboard Data
async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/dashboard`);
        const data = await res.json();

        if (data.empty) {
            document.getElementById('agent-insights').innerHTML = '<p class="muted">No data loaded. Please load the demo data.</p>';
            return;
        }

        // Update metrics
        document.getElementById('metric-income').textContent = formatMoney(data.income);
        document.getElementById('metric-expenses').textContent = formatMoney(data.expenses);
        
        const netEl = document.getElementById('metric-net');
        netEl.textContent = formatMoney(data.net);
        if (data.net < 0) {
            netEl.className = 'value bad';
        } else {
            netEl.className = 'value good';
        }

        document.getElementById('metric-committed').textContent = formatMoney(data.committed);

        // Update Agent Insights
        const insightsContainer = document.getElementById('agent-insights');
        let insightsHtml = '';
        const cats = Object.keys(data.category_totals);
        if (cats.length > 0) {
            insightsHtml += `
                <div class="insight-box">
                    <p><b>Priority 1: Spending Concentration</b></p>
                    <p><b>${cats[0]}</b> is your largest category at <b>${formatMoney(data.category_totals[cats[0]])}</b>.</p>
                </div>
            `;
        }
        
        insightsHtml += `
            <div class="insight-box">
                <p><b>Agent Action:</b></p>
                <p>Review ${cats[0] || 'your'} spending and check for unusual recurring payments.</p>
            </div>
        `;
        insightsContainer.innerHTML = insightsHtml;

        // Render Category Chart
        const ctxCat = document.getElementById('categoryChart').getContext('2d');
        if (categoryChartInstance) categoryChartInstance.destroy();
        
        const catLabels = Object.keys(data.category_totals).slice(0, 8);
        const catData = Object.values(data.category_totals).slice(0, 8);

        categoryChartInstance = new Chart(ctxCat, {
            type: 'bar',
            data: {
                labels: catLabels,
                datasets: [{
                    label: 'Amount spent',
                    data: catData,
                    backgroundColor: 'rgba(99, 102, 241, 0.8)',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Render Flow Chart
        const ctxFlow = document.getElementById('flowChart').getContext('2d');
        if (flowChartInstance) flowChartInstance.destroy();

        const dates = Object.keys(data.cash_flow);
        const flowData = Object.values(data.cash_flow);

        flowChartInstance = new Chart(ctxFlow, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Cash Flow',
                    data: flowData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

    } catch (err) {
        console.error('Error fetching dashboard data:', err);
    }
}

// Load Transactions
async function loadTransactions() {
    try {
        const res = await fetch(`${API_BASE}/transactions`);
        const data = await res.json();
        
        const tbody = document.getElementById('transactions-body');
        
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No transactions found.</td></tr>';
            return;
        }

        tbody.innerHTML = data.map(tx => `
            <tr>
                <td>${tx.date.split(' ')[0]}</td>
                <td>${tx.description}</td>
                <td>${tx.category}</td>
                <td><span class="badge ${tx.type.toLowerCase()}">${tx.type}</span></td>
                <td style="font-weight: 600;">${formatMoney(tx.amount)}</td>
            </tr>
        `).join('');

    } catch (err) {
        console.error('Error fetching transactions:', err);
    }
}

// Load Demo Data Action
document.getElementById('load-demo-btn').addEventListener('click', async () => {
    const btn = document.getElementById('load-demo-btn');
    btn.textContent = 'Loading...';
    btn.disabled = true;

    try {
        await fetch(`${API_BASE}/load_demo`, { method: 'POST' });
        await loadDashboard();
        if (document.getElementById('transactions').classList.contains('active')) {
            await loadTransactions();
        }
    } catch (err) {
        alert('Failed to load demo data');
    } finally {
        btn.textContent = '▶ Load 3-Month Demo';
        btn.disabled = false;
    }
});

// Initial load
loadDashboard();
