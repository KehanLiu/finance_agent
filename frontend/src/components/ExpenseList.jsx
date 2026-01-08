import React, { useState, useMemo } from 'react'
import { format, parseISO, subMonths } from 'date-fns'
import './ExpenseList.css'

function ExpenseList({ expenses, loading, isIncome = false }) {
  // Temporary filter states (user is still selecting)
  const [tempSortOrder, setTempSortOrder] = useState('date-desc')
  const [tempFilterCategory, setTempFilterCategory] = useState('All')
  const [tempSearchTerm, setTempSearchTerm] = useState('')
  const [tempDateRange, setTempDateRange] = useState('3months')

  // Applied filter states (after clicking Update Table)
  const [sortOrder, setSortOrder] = useState('date-desc')
  const [filterCategory, setFilterCategory] = useState('All')
  const [searchTerm, setSearchTerm] = useState('')
  const [dateRange, setDateRange] = useState('3months')

  const applyFilters = () => {
    setSortOrder(tempSortOrder)
    setFilterCategory(tempFilterCategory)
    setSearchTerm(tempSearchTerm)
    setDateRange(tempDateRange)
  }

  if (loading) {
    return <div className="loading">Loading {isIncome ? 'income' : 'expenses'}...</div>
  }

  if (!expenses || expenses.length === 0) {
    return <div className="no-data">No {isIncome ? 'income' : 'expenses'} found</div>
  }

  // Get unique categories
  const categories = useMemo(() => {
    const cats = new Set(expenses.map(e => e.Category).filter(Boolean))
    return ['All', ...Array.from(cats).sort()]
  }, [expenses])

  // Calculate most recent date
  const mostRecentDate = useMemo(() => {
    if (expenses.length === 0) return new Date()
    return new Date(Math.max(...expenses.map(e => new Date(e.Date))))
  }, [expenses])

  // Filter and sort expenses
  const filteredExpenses = useMemo(() => {
    let filtered = [...expenses]

    // Filter out income from expenses table (and vice versa)
    if (!isIncome) {
      filtered = filtered.filter(e => e['Expense amount'] > 0)
    } else {
      filtered = filtered.filter(e => e['Income amount'] > 0)
    }

    // Date filtering - default last 3 months
    if (dateRange !== 'all') {
      let monthsToSubtract = 3
      if (dateRange === '6months') monthsToSubtract = 6
      if (dateRange === '1year') monthsToSubtract = 12

      const cutoffDate = subMonths(mostRecentDate, monthsToSubtract)
      filtered = filtered.filter(e => new Date(e.Date) >= cutoffDate)
    }

    // Category filtering
    if (filterCategory && filterCategory !== 'All') {
      filtered = filtered.filter(e => e.Category === filterCategory)
    }

    // Search filtering
    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(e =>
        (e.Category && e.Category.toLowerCase().includes(term)) ||
        (e.Tags && e.Tags.toLowerCase().includes(term)) ||
        (e.Description && e.Description.toLowerCase().includes(term))
      )
    }

    // Sorting - use converted EUR amounts for accurate comparison
    filtered.sort((a, b) => {
      if (sortOrder === 'date-desc') {
        return new Date(b.Date) - new Date(a.Date)
      } else if (sortOrder === 'date-asc') {
        return new Date(a.Date) - new Date(b.Date)
      } else if (sortOrder === 'amount-desc') {
        const amountA = a['In main currency'] || 0
        const amountB = b['In main currency'] || 0
        return amountB - amountA
      } else if (sortOrder === 'amount-asc') {
        const amountA = a['In main currency'] || 0
        const amountB = b['In main currency'] || 0
        return amountA - amountB
      }
      return 0
    })

    return filtered
  }, [expenses, dateRange, filterCategory, searchTerm, sortOrder, isIncome, mostRecentDate])

  return (
    <div className="expense-list">
      <div className="expense-list-header">
        <h2>{isIncome ? 'Income Entries' : 'Expenses'}</h2>
        <div className="expense-filters">
          <div className="filter-group">
            <label>Date Range:</label>
            <select value={tempDateRange} onChange={(e) => setTempDateRange(e.target.value)}>
              <option value="3months">Last 3 Months</option>
              <option value="6months">Last 6 Months</option>
              <option value="1year">Last Year</option>
              <option value="all">All Time</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Category:</label>
            <select value={tempFilterCategory} onChange={(e) => setTempFilterCategory(e.target.value)}>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Search:</label>
            <input
              type="text"
              placeholder="Filter by keyword..."
              value={tempSearchTerm}
              onChange={(e) => setTempSearchTerm(e.target.value)}
            />
          </div>

          <div className="filter-group">
            <label>Sort:</label>
            <select value={tempSortOrder} onChange={(e) => setTempSortOrder(e.target.value)}>
              <option value="date-desc">Date (Newest)</option>
              <option value="date-asc">Date (Oldest)</option>
              <option value="amount-desc">Amount (High to Low)</option>
              <option value="amount-asc">Amount (Low to High)</option>
            </select>
          </div>

          <div className="filter-group">
            <label>&nbsp;</label>
            <button
              className="update-button"
              onClick={applyFilters}
            >
              Update Table
            </button>
          </div>
        </div>
        <div className="results-count">
          Showing {filteredExpenses.length} of {expenses.length} entries
        </div>
      </div>
      <div className="expense-table">
        <div className="table-header">
          <div>Date</div>
          <div>Category</div>
          <div>Tags</div>
          <div>Description</div>
          <div>Amount</div>
        </div>
        {filteredExpenses.map((expense, index) => (
          <div key={index} className="table-row">
            <div className="date">
              {expense.Date ? format(parseISO(expense.Date), 'MMM dd, yyyy') : '-'}
            </div>
            <div className="category">
              <span className="category-badge">{expense.Category || '-'}</span>
            </div>
            <div className="tags">
              {expense.Tags && (
                <div className="tag-list">
                  {expense.Tags.split(',').map((tag, i) => (
                    <span key={i} className="tag">{tag.trim()}</span>
                  ))}
                </div>
              )}
            </div>
            <div className="description">{expense.Description || '-'}</div>
            <div className="amount">
              {expense['In main currency'] ? expense['In main currency'].toFixed(2) : '0.00'} {expense['Main currency'] || 'EUR'}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ExpenseList
