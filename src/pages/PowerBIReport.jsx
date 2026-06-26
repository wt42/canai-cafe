import { useEffect, useState } from 'react';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import { getManyJson } from '../services/dataService.js';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const COLORS = ['#5b341f', '#c7923e', '#407a52', '#b42318', '#2c1810', '#744EC2', '#D9B300', '#E66C37'];

const PRODUCT_ICONS = {
  'Sandwich': '🥪',
  'Coffee': '☕',
  'Salad': '🥗',
  'Tea': '🍵',
  'Refresher': '🧃',
  'Juice': '🍊',
  'Cookie': '🍪',
  'Donut': '🍩'
};

export default function PowerBIReport() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getManyJson([
      'kpi_summary.json',
      'monthly_sales.json',
      'product_performance.json',
      'province_performance.json',
      'payment_performance.json',
      'weekday_detail.json'
    ]).then(setData).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!data) return <LoadingState />;

  const kpi = data['kpi_summary.json'];
  const monthly = data['monthly_sales.json'];
  const products = data['product_performance.json'];
  const provinces = data['province_performance.json'];
  const payments = data['payment_performance.json'];
  const weekday = data['weekday_detail.json'];

  const formatCurrency = (val) => `$${Number(val).toLocaleString()}`;

  const productsWithIcons = products.map(p => ({
    ...p,
    label: `${PRODUCT_ICONS[p.name] || ''} ${p.name}`
  }));

  return (
    <div className="pbi-dashboard">
      <style>{`
        .pbi-dashboard {
          padding: 0;
        }
        .pbi-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }
        .pbi-header h1 {
          margin: 0;
          font-size: 20px;
          font-weight: 700;
          color: var(--coffee-dark);
        }
        .pbi-header p {
          margin: 4px 0 0;
          color: var(--muted);
          font-size: 13px;
        }
        .pbi-badge {
          background: var(--coffee-dark);
          color: #fff;
          padding: 12px 24px;
          border-radius: 999px;
          font-size: 15px;
          font-weight: 700;
          letter-spacing: 0.06em;
        }
        .pbi-kpis {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          margin-bottom: 22px;
        }
        .pbi-kpi {
          background: var(--panel);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 18px 20px;
          border-top: 3px solid var(--gold);
          box-shadow: var(--shadow);
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .pbi-kpi:hover {
          transform: translateY(-3px);
          box-shadow: 0 12px 30px rgba(44, 24, 16, 0.15);
        }
        .pbi-kpi-icon {
          font-size: 28px;
          margin-bottom: 6px;
        }
        .pbi-kpi p {
          margin: 0;
          color: var(--muted);
          font-size: 11px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.06em;
        }
        .pbi-kpi h2 {
          margin: 6px 0 0;
          font-size: 26px;
          font-weight: 800;
          color: var(--coffee-dark);
        }
        .pbi-row {
          display: grid;
          gap: 16px;
          margin-bottom: 16px;
        }
        .pbi-row-2 { grid-template-columns: 1.4fr 1fr; }
        .pbi-row-3 { grid-template-columns: 1fr 1fr 1fr; }
        .pbi-card {
          background: var(--panel);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 20px;
          box-shadow: var(--shadow);
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .pbi-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 14px 35px rgba(44, 24, 16, 0.12);
        }
        .pbi-card h3 {
          margin: 0 0 14px;
          font-size: 14px;
          font-weight: 700;
          color: var(--coffee-dark);
        }
        .pbi-footer {
          margin-top: 16px;
          padding: 12px 18px;
          background: var(--panel-soft);
          border: 1px solid var(--border);
          border-radius: 12px;
          display: flex;
          justify-content: space-between;
          font-size: 12px;
          color: var(--muted);
        }
        .pbi-legend {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-top: 8px;
        }
        .pbi-legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 11px;
          color: var(--text);
        }
        .pbi-legend-dot {
          width: 10px;
          height: 10px;
          border-radius: 50%;
        }
      `}</style>

      {/* Header */}
      <div className="pbi-header">
        <div>
          <h1>☕ CanAI Café — 2023 Sales Intelligence</h1>
          <p>Interactive Power BI Dashboard • Data source: Cleaned transactions</p>
        </div>
        <span className="pbi-badge">⚡ POWER BI</span>
      </div>

      {/* KPI Cards */}
      <div className="pbi-kpis">
        {[
          { label: 'Total Revenue', value: formatCurrency(kpi.totalRevenue), icon: '💰' },
          { label: 'Transactions', value: kpi.totalTransactions.toLocaleString(), icon: '🧾' },
          { label: 'Avg Transaction', value: formatCurrency(kpi.averageTransactionValue), icon: '📊' },
          { label: 'Units Sold', value: kpi.totalUnitsSold.toLocaleString(), icon: '📦' }
        ].map(card => (
          <div key={card.label} className="pbi-kpi">
            <div className="pbi-kpi-icon">{card.icon}</div>
            <p>{card.label}</p>
            <h2>{card.value}</h2>
          </div>
        ))}
      </div>

      {/* Row 1: Line + Bar */}
      <div className="pbi-row pbi-row-2">
        <div className="pbi-card">
          <h3>📈 Monthly Revenue Trend</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={monthly}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" tick={{ fill: '#667085', fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
              <YAxis tick={{ fill: '#667085', fontSize: 11 }} tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(v)} />
              <Line type="monotone" dataKey="revenue" stroke="#c7923e" strokeWidth={2.5} dot={{ fill: '#5b341f', r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="pbi-card">
          <h3>🍩 Revenue by Product</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={productsWithIcons} layout="vertical" margin={{ left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis type="number" tick={{ fill: '#667085', fontSize: 11 }} tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <YAxis type="category" dataKey="label" tick={{ fill: '#667085', fontSize: 12 }} width={100} />
              <Tooltip formatter={(v) => formatCurrency(v)} />
              <Bar dataKey="revenue" radius={[0, 6, 6, 0]}>
                {productsWithIcons.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 2: Donut + Donut + Column */}
      <div className="pbi-row pbi-row-3">
        <div className="pbi-card">
          <h3>💳 Payment Methods</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={payments} dataKey="revenue" nameKey="name" cx="50%" cy="50%" innerRadius={40} outerRadius={65}>
                {payments.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(v) => formatCurrency(v)} />
            </PieChart>
          </ResponsiveContainer>
          <div className="pbi-legend">
            {payments.map((p, i) => (
              <span key={p.name} className="pbi-legend-item">
                <span className="pbi-legend-dot" style={{ background: COLORS[i % COLORS.length] }}></span>
                {p.name} ({p.revenueShare}%)
              </span>
            ))}
          </div>
        </div>

        <div className="pbi-card">
          <h3>🗺️ Revenue by Province</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={provinces} dataKey="revenue" nameKey="name" cx="50%" cy="50%" innerRadius={40} outerRadius={65}>
                {provinces.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(v) => formatCurrency(v)} />
            </PieChart>
          </ResponsiveContainer>
          <div className="pbi-legend">
            {provinces.map((p, i) => (
              <span key={p.name} className="pbi-legend-item">
                <span className="pbi-legend-dot" style={{ background: COLORS[i % COLORS.length] }}></span>
                {p.name.split(' ')[0]} ({p.revenueShare}%)
              </span>
            ))}
          </div>
        </div>

        <div className="pbi-card">
          <h3>📅 Revenue by Day</h3>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={weekday} margin={{ bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="name" tick={{ fill: '#667085', fontSize: 10 }} tickFormatter={(v) => v.slice(0,3)} />
              <YAxis tick={{ fill: '#667085', fontSize: 10 }} tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(v)} />
              <Bar dataKey="totalRevenue" radius={[4, 4, 0, 0]}>
                {weekday.map((_, i) => <Cell key={i} fill={i < 5 ? '#5b341f' : '#c7923e'} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="pbi-legend">
            <span className="pbi-legend-item"><span className="pbi-legend-dot" style={{ background: '#5b341f' }}></span>Weekday</span>
            <span className="pbi-legend-item"><span className="pbi-legend-dot" style={{ background: '#c7923e' }}></span>Weekend</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="pbi-footer">
        <span>Data source: CanAI Café 2023 Sales (cleaned) • 10,000 transactions</span>
      </div>
    </div>
  );
}
