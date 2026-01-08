import React from 'react'
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, LineChart, Line, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts'
import { format, parseISO } from 'date-fns'
import './Dashboard.css'

// Modern gradient colors for dark mode
const COLORS = [
  '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b',
  '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3'
]

const GRADIENT_COLORS = [
  { start: '#667eea', end: '#764ba2' },
  { start: '#f093fb', end: '#f5576c' },
  { start: '#4facfe', end: '#00f2fe' },
  { start: '#43e97b', end: '#38f9d7' },
  { start: '#fa709a', end: '#fee140' }
]

// Custom tooltip with dark mode styling
const CustomTooltip = ({ active, payload, label, currency }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }}>
            {entry.name}: {entry.value.toFixed(2)} {currency}
          </p>
        ))}
      </div>
    )
  }
  return null
}

function Dashboard({ summary }) {
  if (!summary || !summary.category_breakdown || !summary.top_tags || !summary.monthly_summary) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading your financial insights...</p>
      </div>
    )
  }

  // Prepare category data for pie chart
  const categoryData = Object.entries(summary.category_breakdown)
    .slice(0, 8)
    .map(([name, value]) => ({
      name,
      value: parseFloat(value)
    }))

  // Prepare tag data
  const tagData = Object.entries(summary.top_tags)
    .slice(0, 10)
    .map(([name, value]) => ({
      name,
      value: parseFloat(value)
    }))

  // Prepare monthly trend data (last 12 months)
  const monthlyData = Object.entries(summary.monthly_summary)
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-12)
    .map(([month, data]) => ({
      month: month, // Keep full YYYY-MM format for display
      expenses: parseFloat(data.expenses || 0),
      income: parseFloat(data.income || 0),
      net: parseFloat(data.net || 0)
    }))

  // Prepare yearly data
  const yearlyData = Object.entries(summary.yearly_summary || {})
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([year, data]) => ({
      year,
      expenses: parseFloat(data.expenses || 0),
      income: parseFloat(data.income || 0),
      net: parseFloat(data.net || 0)
    }))

  // Prepare radar chart data for top categories
  const radarData = Object.entries(summary.category_breakdown)
    .slice(0, 6)
    .map(([category, value]) => ({
      category: category.length > 15 ? category.substring(0, 12) + '...' : category,
      value: parseFloat(value)
    }))

  return (
    <div className="dashboard dark-mode">
      {/* Hero Stats Cards */}
      <div className="hero-stats">
        <div className="stat-card expenses-card">
          <div className="stat-icon">💸</div>
          <div className="stat-content">
            <h3>Total Expenses</h3>
            <p className="stat-amount">{summary.total_expenses.toFixed(2)}</p>
            <span className="stat-currency">{summary.currency}</span>
          </div>
          <div className="stat-trend">
            <span className="date-range">
              {summary.date_range.start && format(parseISO(summary.date_range.start), 'MMM yyyy')} -
              {summary.date_range.end && format(parseISO(summary.date_range.end), 'MMM yyyy')}
            </span>
          </div>
        </div>

        <div className="stat-card income-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Total Income</h3>
            <p className="stat-amount">{summary.total_income.toFixed(2)}</p>
            <span className="stat-currency">{summary.currency}</span>
          </div>
          <div className="stat-badge positive">+{summary.income_count || 0} entries</div>
        </div>

        <div className={`stat-card balance-card ${summary.net >= 0 ? 'positive' : 'negative'}`}>
          <div className="stat-icon">{summary.net >= 0 ? '📈' : '📉'}</div>
          <div className="stat-content">
            <h3>Net Balance</h3>
            <p className="stat-amount">{Math.abs(summary.net).toFixed(2)}</p>
            <span className="stat-currency">{summary.currency}</span>
          </div>
          <div className={`stat-badge ${summary.net >= 0 ? 'positive' : 'negative'}`}>
            {summary.net >= 0 ? '+' : '-'} {((Math.abs(summary.net) / summary.total_expenses) * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Main Charts Grid */}
      <div className="charts-container">
        {/* Monthly Trend - Area Chart */}
        <div className="chart-card trend-chart">
          <div className="chart-header">
            <h3>📊 Monthly Cash Flow</h3>
            <span className="chart-subtitle">Last 12 months</span>
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={monthlyData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#43e97b" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#43e97b" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f093fb" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#f093fb" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
              <XAxis dataKey="month" stroke="#8b8b9a" />
              <YAxis stroke="#8b8b9a" />
              <Tooltip content={<CustomTooltip currency={summary.currency} />} />
              <Legend />
              <Area
                type="monotone"
                dataKey="income"
                stroke="#43e97b"
                fillOpacity={1}
                fill="url(#colorIncome)"
                strokeWidth={3}
                name="Income"
                animationDuration={1500}
                dot={{ fill: '#43e97b', r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Area
                type="monotone"
                dataKey="expenses"
                stroke="#f093fb"
                fillOpacity={1}
                fill="url(#colorExpenses)"
                strokeWidth={3}
                name="Expenses"
                animationDuration={1500}
                dot={{ fill: '#f093fb', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Category Distribution - Donut Chart */}
        <div className="chart-card donut-chart">
          <div className="chart-header">
            <h3>🎯 Spending Distribution</h3>
            <span className="chart-subtitle">Top categories</span>
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                animationDuration={1000}
                animationBegin={0}
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip currency={summary.currency} />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Chart for Categories */}
        <div className="chart-card radar-chart">
          <div className="chart-header">
            <h3>🎪 Category Analysis</h3>
            <span className="chart-subtitle">Spending patterns</span>
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#2a2a3e" />
              <PolarAngleAxis dataKey="category" stroke="#8b8b9a" />
              <PolarRadiusAxis stroke="#8b8b9a" />
              <Radar
                name="Spending"
                dataKey="value"
                stroke="#667eea"
                fill="#667eea"
                fillOpacity={0.6}
                animationDuration={1000}
              />
              <Tooltip content={<CustomTooltip currency={summary.currency} />} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Tags - Horizontal Bar Chart */}
        <div className="chart-card tags-chart">
          <div className="chart-header">
            <h3>🏷️ Top Spending Tags</h3>
            <span className="chart-subtitle">Most frequent expenses</span>
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={tagData} layout="vertical" margin={{ left: 100 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
              <XAxis type="number" stroke="#8b8b9a" />
              <YAxis type="category" dataKey="name" stroke="#8b8b9a" />
              <Tooltip content={<CustomTooltip currency={summary.currency} />} />
              <Bar dataKey="value" fill="#667eea" radius={[0, 8, 8, 0]} animationDuration={1000}>
                {tagData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Yearly Overview */}
        {yearlyData.length > 1 && (
          <div className="chart-card yearly-chart full-width">
            <div className="chart-header">
              <h3>📅 Yearly Overview</h3>
              <span className="chart-subtitle">Annual comparison</span>
            </div>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={yearlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
                <XAxis dataKey="year" stroke="#8b8b9a" />
                <YAxis stroke="#8b8b9a" />
                <Tooltip content={<CustomTooltip currency={summary.currency} />} />
                <Legend />
                <Bar dataKey="income" fill="#43e97b" name="Income" radius={[8, 8, 0, 0]} animationDuration={1000} />
                <Bar dataKey="expenses" fill="#f093fb" name="Expenses" radius={[8, 8, 0, 0]} animationDuration={1000} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Category Details Table */}
      <div className="category-details">
        <div className="chart-header">
          <h3>📋 Category Breakdown</h3>
          <span className="chart-subtitle">Categories over 50 {summary.currency}</span>
        </div>
        <div className="category-grid">
          {Object.entries(summary.category_breakdown)
            .filter(([_, amount]) => parseFloat(amount) >= 50)
            .map(([category, amount], index) => (
              <div key={category} className="category-item" style={{ animationDelay: `${index * 50}ms` }}>
                <div className="category-info">
                  <span className="category-icon" style={{ backgroundColor: COLORS[index % COLORS.length] }}>
                    {index + 1}
                  </span>
                  <span className="category-name">{category}</span>
                </div>
                <div className="category-value">
                  <span className="category-amount">{parseFloat(amount).toFixed(2)}</span>
                  <span className="category-currency">{summary.currency}</span>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
