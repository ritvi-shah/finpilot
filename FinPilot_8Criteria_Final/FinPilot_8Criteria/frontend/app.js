const API_BASE = '/api';
// ─── State ──────────────────────────────────────────────────────────────────
let hasData = false;
let categoryChartInstance = null;
let flowChartInstance     = null;

// ─── Helpers ─────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
const formatMoney = (amount) =>
    new Intl.NumberFormat('en-IN', {
        style: 'currency', currency: 'INR', maximumFractionDigits: 0
    }).format(Math.abs(amount));

function showToast(msg, type = 'success') {
    const t = document.createElement('div');
    t.className = `toast toast-${type}`;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.classList.add('show'), 10);
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 3500);
}

// ─── View Management ─────────────────────────────────────────────────────────
function showAppView(targetId) {
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
        v.classList.add('hidden');
    });
    const target = $(targetId);
    if (target) {
        target.classList.remove('hidden');
        target.classList.add('active');
    }
}

function switchToApp() {
    hasData = true;
    // Hide onboarding, show nav-accessible views
    $('empty-state').classList.add('hidden');
    $('empty-state').classList.remove('active');
    showAppView('dashboard');
    // Mark dashboard nav as active
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector('[data-target="dashboard"]').classList.add('active');
    loadDashboard();
}

// ─── Navigation ──────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        if (!hasData) {
            showToast('Please upload your data or add a transaction first.', 'warn');
            return;
        }
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');

        const targetId = item.getAttribute('data-target');
        showAppView(targetId);

        if (targetId === 'transactions') loadTransactions();
        if (targetId === 'budgets')      loadBudgets();
    });
});

// ─── File Upload ─────────────────────────────────────────────────────────────
$('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = $('file-upload').files[0];
    if (!file) return;

    const btn = $('upload-btn');
    btn.textContent = 'Uploading…';
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res  = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
        const data = await res.json();
        if (data.success) {
            showToast(`✅ ${data.message}`);
            switchToApp();
        } else {
            showToast(`❌ ${data.message}`, 'error');
        }
    } catch (err) {
        showToast('❌ Could not reach the server. Is it running?', 'error');
    } finally {
        btn.textContent = 'Upload Transactions';
        btn.disabled = false;
    }
});

// ─── Manual Transaction Entry ─────────────────────────────────────────────────
// Set today's date as default
$('tx-date').valueAsDate = new Date();

$('manual-tx-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        date:        $('tx-date').value,
        description: $('tx-desc').value.trim() || 'Unnamed Transaction',
        amount:      parseFloat($('tx-amt').value),
        type:        $('tx-type').value,
        category:    $('tx-cat').value,
        notes:       ''
    };

   if (!payload.amount) {
    showToast('Please fill in the Amount.', 'warn');
    return;
}

    const btn = $('add-tx-btn');
    btn.textContent = 'Adding…';
    btn.disabled = true;

    try {
        const res  = await fetch(`${API_BASE}/add_transaction`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            showToast('✅ Transaction added!');
            $('manual-tx-form').reset();
            $('tx-date').valueAsDate = new Date();
            if (!hasData) {
                switchToApp();
            } else {
                loadDashboard();
            }
        } else {
            showToast(`❌ ${data.message}`, 'error');
        }
    } catch (err) {
        showToast('❌ Could not reach the server.', 'error');
    } finally {
        btn.textContent = 'Add Transaction';
        btn.disabled = false;
    }
});

// ─── Add Transaction form inside Transactions view ──────────────────────────
// (also available from sidebar Add-Tx button)
const addTxViewForm = $('add-tx-view-form');
if (addTxViewForm) {
    $('tx2-date').valueAsDate = new Date();
    addTxViewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            date:        $('tx2-date').value,
            description: $('tx2-desc').value.trim() || 'Unnamed Transaction',
            amount:      parseFloat($('tx2-amt').value),
            type:        $('tx2-type').value,
            category:    $('tx2-cat').value,
            notes:       ''
        };
        const btn = $('add-tx2-btn');
        btn.textContent = 'Adding…';
        btn.disabled = true;
if (!payload.amount) {
    showToast('Please fill in the Amount.', 'warn');
    return;
}
        try {
            const res  = await fetch(`${API_BASE}/add_transaction`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.success) {
                showToast('✅ Transaction added!');
                addTxViewForm.reset();
                $('tx2-date').valueAsDate = new Date();
                loadTransactions();
                loadDashboard();
            } else {
                showToast(`❌ ${data.message}`, 'error');
            }
        } catch (err) {
            showToast('❌ Could not reach the server.', 'error');
        } finally {
            btn.textContent = 'Add Transaction';
            btn.disabled = false;
        }
    });
}

// ─── CSV Upload inside Transactions view ──────────────────────────────────────
const uploadViewForm = $('upload-view-form');
if (uploadViewForm) {
    uploadViewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = $('file-upload-2').files[0];
        if (!file) return;

        const btn = $('upload-btn-2');
        btn.textContent = 'Uploading…';
        btn.disabled = true;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res  = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
            const data = await res.json();
            if (data.success) {
                showToast(`✅ ${data.message}`);
                $('file-upload-2').value = '';
                if ($('file-name-display-2')) $('file-name-display-2').textContent = '';
                loadTransactions();
                loadDashboard();
            } else {
                showToast(`❌ ${data.message}`, 'error');
            }
        } catch (err) {
            showToast('❌ Could not reach the server. Is it running?', 'error');
        } finally {
            btn.textContent = 'Upload & Merge';
            btn.disabled = false;
        }
    });

    // Handle file selection display for the second drop zone
    $('file-upload-2')?.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file && $('file-name-display-2')) {
            $('file-name-display-2').textContent = file.name;
        }
    });
}

// ─── Reset ────────────────────────────────────────────────────────────────────
$('reset-btn').addEventListener('click', async () => {
    if (!confirm('Reset all data? This cannot be undone.')) return;
    try {
        await fetch(`${API_BASE}/reset`, { method: 'POST' });
    } catch (_) {}
    hasData = false;
    if (categoryChartInstance) { categoryChartInstance.destroy(); categoryChartInstance = null; }
    if (flowChartInstance)     { flowChartInstance.destroy();     flowChartInstance = null; }
    // Reset metrics
    $('metric-income').textContent    = '₹0';
    $('metric-expenses').textContent  = '₹0';
    $('metric-net').textContent       = '₹0';
    $('metric-committed').textContent = '₹0';
    $('agent-insights').innerHTML     = '<p class="muted">Load data to see insights.</p>';
    $('transactions-body').innerHTML  = '<tr><td colspan="5" class="empty-state">No transactions found.</td></tr>';
    // Show onboarding
    document.querySelectorAll('.view').forEach(v => { v.classList.remove('active'); v.classList.add('hidden'); });
    $('empty-state').classList.remove('hidden');
    $('empty-state').classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    $('file-upload').value = '';
    $('manual-tx-form').reset();
    $('tx-date').valueAsDate = new Date();
    showToast('Data reset.', 'warn');
});

// ─── Dashboard ────────────────────────────────────────────────────────────────
async function loadDashboard() {
    try {
        const res  = await fetch(`${API_BASE}/dashboard`);
        const data = await res.json();

        if (data.empty) {
            $('agent-insights').innerHTML = '<p class="muted">Add or upload transactions to see insights.</p>';
            return;
        }

        $('metric-income').textContent   = formatMoney(data.income);
        $('metric-expenses').textContent = formatMoney(data.expenses);

        const netEl = $('metric-net');
        netEl.textContent = (data.net < 0 ? '-' : '+') + formatMoney(data.net);
        netEl.className   = data.net < 0 ? 'value bad' : 'value good';

        $('metric-committed').textContent = formatMoney(data.committed);

        // Agent Insights
const categoryEntries = Object.entries(data.category_totals)
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));

let insightsHtml = '';

if (categoryEntries.length > 0) {
    const [topCategory, topAmount] = categoryEntries[0];

    const savingsRate = data.income > 0
        ? ((data.income - data.expenses) / data.income * 100).toFixed(1)
        : '0.0';

    insightsHtml += `
        <div class="insight-box">
            <p><b>🏆 Top Spend: ${topCategory}</b></p>
            <p>You spent <b>${formatMoney(topAmount)}</b> on ${topCategory} this month.</p>
        </div>

        <div class="insight-box">
            <p><b>💰 Savings Rate</b></p>
            <p>You saved <b>${savingsRate}%</b> of your income this month.</p>
        </div>`;
}

if (data.committed > 0) {
    insightsHtml += `<div class="insight-box">
        <p><b>📌 Committed Bills</b></p>
        <p><b>${formatMoney(data.committed)}</b> is tracked as upcoming obligations.</p>
    </div>`;
}

if (!insightsHtml) {
    insightsHtml = '<p class="muted">Add more transactions to generate insights.</p>';
}

$('agent-insights').innerHTML = insightsHtml;
        if (data.committed > 0) {
            insightsHtml += `<div class="insight-box">
                <p><b>📌 Committed Bills</b></p>
                <p><b>${formatMoney(data.committed)}</b> is tracked as upcoming obligations.</p>
            </div>`;
        }
        if (!insightsHtml) insightsHtml = '<p class="muted">Add more transactions to generate insights.</p>';
        $('agent-insights').innerHTML = insightsHtml;

        // Category Chart
        const ctxCat = $('categoryChart').getContext('2d');
        if (categoryChartInstance) categoryChartInstance.destroy();
        const catLabels = Object.keys(data.category_totals).slice(0, 8);
        const catData   = Object.values(data.category_totals).slice(0, 8);
        categoryChartInstance = new Chart(ctxCat, {
            type: 'bar',
            data: {
                labels: catLabels,
                datasets: [{
                    label: 'Amount spent',
                    data: catData,
                    backgroundColor: [
                        'rgba(99,102,241,0.85)','rgba(16,185,129,0.85)','rgba(245,158,11,0.85)',
                        'rgba(244,63,94,0.85)','rgba(139,92,246,0.85)','rgba(6,182,212,0.85)',
                        'rgba(251,146,60,0.85)','rgba(52,211,153,0.85)'
                    ],
                    borderRadius: 8,
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', callback: v => '₹' + v.toLocaleString('en-IN') } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Cash Flow Chart
        const ctxFlow = $('flowChart').getContext('2d');
        if (flowChartInstance) flowChartInstance.destroy();
        const dates    = Object.keys(data.cash_flow);
        const flowData = Object.values(data.cash_flow);
        flowChartInstance = new Chart(ctxFlow, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Cash Flow',
                    data: flowData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16,185,129,0.1)',
                    tension: 0.4, fill: true, pointRadius: 3,
                    pointBackgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', callback: v => '₹' + v.toLocaleString('en-IN') } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8', maxTicksLimit: 10 } }
                }
            }
        });

    } catch (err) {
        console.error('Dashboard error:', err);
    }
}

// ─── Transactions ─────────────────────────────────────────────────────────────
async function loadTransactions() {
    try {
        const res  = await fetch(`${API_BASE}/transactions`);
        const data = await res.json();
        const tbody = $('transactions-body');

        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No transactions yet.</td></tr>';
            return;
        }

        tbody.innerHTML = [...data].reverse().map(tx => `
            <tr>
                <td>${tx.date.split(' ')[0]}</td>
                <td>${tx.description}</td>
                <td><span class="category-tag">${tx.category}</span></td>
                <td><span class="badge ${tx.type.toLowerCase()}">${tx.type}</span></td>
                <td style="font-weight:700;color:${tx.type==='Income'?'#10b981':'#f43f5e'}">
                    ${tx.type === 'Income' ? '+' : '-'}${formatMoney(tx.amount)}
                </td>
            </tr>
        `).join('');
    } catch (err) {
        console.error('Transactions error:', err);
    }
}

// ─── Budgets ──────────────────────────────────────────────────────────────────
async function loadBudgets() {
    try {
        const res  = await fetch(`${API_BASE}/budgets`);
        const data = await res.json();
        const { budgets, actuals = {} } = data;

        const list = $('budget-list');
        if (!Object.keys(budgets).length) {
            list.innerHTML = '<p class="muted">No budgets set yet.</p>';
        } else {
            list.innerHTML = Object.entries(budgets).map(([cat, limit]) => {
                const spent = actuals[cat] || 0;
                const pct   = Math.min(100, (spent / limit) * 100).toFixed(0);
                const color = pct >= 90 ? '#f43f5e' : pct >= 70 ? '#f59e0b' : '#10b981';
                return `
                <div class="budget-bar-wrap">
                    <div class="budget-bar-header">
                        <span><b>${cat}</b></span>
                        <span style="color:${color}">${formatMoney(spent)} / ${formatMoney(limit)}</span>
                    </div>
                    <div class="budget-track">
                        <div class="budget-fill" style="width:${pct}%;background:${color}"></div>
                    </div>
                </div>`;
            }).join('');
        }

        // Frequent Transactions
        const subsRes  = await fetch(`${API_BASE}/frequent_transactions`);
        const subsData = await subsRes.json();
        const subsList = $('subs-list');
        if (!subsData.length) {
            subsList.innerHTML = '<p class="muted">No repeated transactions detected yet.</p>';
        } else {
            subsList.innerHTML = subsData.slice(0, 10).map(s => `
                <div class="sub-item" style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                    <div>
                        <div style="font-weight:600;font-size:14px">${s.description}</div>
                        <div style="font-size:12px;color:var(--text-secondary)">${s.category} &bull; ${s.count}x this period</div>
                    </div>
                    <span class="badge expense">${formatMoney(s.total)} total</span>
                </div>`
            ).join('');
        }
    } catch (err) {
        console.error('Budgets error:', err);
    }
}

$('budget-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = { category: $('budget-category').value, amount: $('budget-amount').value };
    try {
        await fetch(`${API_BASE}/budgets`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        showToast('✅ Budget saved!');
        $('budget-amount').value = '';
        loadBudgets();
    } catch (err) {
        showToast('❌ Could not save budget.', 'error');
    }
});

// ─── Goals ────────────────────────────────────────────────────────────────────
async function loadGoals() {
    try {
        const res  = await fetch(`${API_BASE}/goals`);
        const data = await res.json();
        const list = $('goals-list');
        if (!data.length) {
            list.innerHTML = '<p class="muted" style="padding:16px">No goals yet. Add one above.</p>';
            return;
        }
        list.innerHTML = data.map(g => {
            const pct      = Math.min(100, (g.current / g.target) * 100).toFixed(0);
            const months   = g.monthly > 0 ? Math.ceil((g.target - g.current) / g.monthly) : '∞';
            return `
            <div class="glass goal-card">
                <h4>${g.name}</h4>
                <div class="goal-meta">
                    <span>${formatMoney(g.current)} saved</span>
                    <span>Target: ${formatMoney(g.target)}</span>
                </div>
                <div class="budget-track" style="margin:12px 0">
                    <div class="budget-fill" style="width:${pct}%;background:var(--accent)"></div>
                </div>
                <p class="muted">${pct}% achieved · ~${months} months to goal</p>
            </div>`;
        }).join('');
    } catch (err) {
        console.error('Goals error:', err);
    }
}

$('goal-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name:    $('goal-name').value.trim(),
        target:  parseFloat($('goal-target').value),
        current: parseFloat($('goal-current').value),
        monthly: parseFloat($('goal-monthly').value)
    };
    try {
        await fetch(`${API_BASE}/goals`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        showToast('✅ Goal added!');
        $('goal-form').reset();
        loadGoals();
    } catch (err) {
        showToast('❌ Could not save goal.', 'error');
    }
});

// Load goals when switching to goals view
document.querySelector('[data-target="goals"]')?.addEventListener('click', () => {
    if (hasData) loadGoals();
});

// ─── Ask FinPilot ──────────────────────────────────────────────────────────────
$('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!hasData) { showToast('Please load your data first.', 'warn'); return; }
    const input    = $('chat-input');
    const query    = input.value.trim();
    if (!query) return;

    const history  = $('chat-history');
    history.innerHTML += `
        <div class="chat-msg user-msg">
            <div class="msg-avatar">👤</div>
            <div class="bubble">${query}</div>
        </div>`;
    input.value = '';
    history.scrollTop = history.scrollHeight;

    try {
        const res  = await fetch(`${API_BASE}/ask`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await res.json();
        const parsedData = marked.parse ? marked.parse(data.response) : data.response;
        history.innerHTML += `
            <div class="chat-msg agent-msg">
                <div class="msg-avatar">✨</div>
                <div class="bubble">${parsedData}</div>
            </div>`;
    } catch (_) {
        history.innerHTML += `
            <div class="chat-msg agent-msg">
                <div class="msg-avatar">✨</div>
                <div class="bubble">❌ Could not reach the server.</div>
            </div>`;
    }
    history.scrollTop = history.scrollHeight;
});

// ─── Initial State ────────────────────────────────────────────────────────────
(async function init() {
    // Check if server already has data (e.g. after page refresh without server restart)
    try {
        const res  = await fetch(`${API_BASE}/dashboard`);
        const data = await res.json();
        if (!data.empty) {
            switchToApp();
            return;
        }
    } catch (_) {}

    // Show onboarding
    document.querySelectorAll('.view').forEach(v => { v.classList.remove('active'); v.classList.add('hidden'); });
    $('empty-state').classList.remove('hidden');
    $('empty-state').classList.add('active');
    $('tx-date').valueAsDate = new Date();
})();
