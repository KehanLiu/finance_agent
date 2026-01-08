import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './components/Dashboard'
import ExpenseList from './components/ExpenseList'
import AIInsights from './components/AIInsights'
import Login from './components/Login'
import './App.css'

// In production (Railway), API is served from same origin
// In development, use VITE_API_URL or default to localhost
const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://localhost:8000')

// Create axios instance with interceptor
const api = axios.create({
  baseURL: API_BASE
})

// Add request interceptor to include credentials (cookies)
api.interceptors.request.use(
  (config) => {
    // Cookies are sent automatically with withCredentials
    config.withCredentials = true
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

function App() {
  const [summary, setSummary] = useState(null)
  const [expenses, setExpenses] = useState([])
  const [income, setIncome] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [authStatus, setAuthStatus] = useState(null)
  const [showLogin, setShowLogin] = useState(false)

  useEffect(() => {
    // Check auth status and fetch data on mount
    checkAuthStatus()
    fetchSummary()
    fetchExpenses()
    fetchIncome()
  }, [])

  const checkAuthStatus = async () => {
    try {
      console.log('Checking auth status at:', `/api/auth/status`)
      const response = await api.get(`/api/auth/status`)
      console.log('Auth response:', response.data)
      setAuthStatus(response.data)
      return response.data
    } catch (error) {
      console.error('Error checking auth status:', error)
      setAuthStatus({ authenticated: false, mode: 'guest' })
      return { authenticated: false, mode: 'guest' }
    }
  }

  const fetchSummary = async () => {
    try {
      const response = await api.get(`/api/summary`)
      setSummary(response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching summary:', error)
      // Don't throw during initial load or logout
      return null
    }
  }

  const fetchExpenses = async (filters = {}) => {
    try {
      setLoading(true)
      const params = new URLSearchParams(filters)
      const response = await api.get(`/api/expenses?${params}`)
      setExpenses(response.data.expenses)
      return response.data
    } catch (error) {
      console.error('Error fetching expenses:', error)
      setExpenses([])
      return null
    } finally {
      setLoading(false)
    }
  }

  const fetchIncome = async () => {
    try {
      const response = await api.get(`/api/income`)
      setIncome(response.data.income)
      return response.data
    } catch (error) {
      console.error('Error fetching income:', error)
      setIncome([])
      return null
    }
  }

  const handleLogin = async (token) => {
    console.log('Login attempt with token:', token.substring(0, 10) + '...')

    try {
      // Call login endpoint to set httpOnly cookie
      const loginResponse = await api.post('/api/auth/login', { token })
      console.log('Login response:', loginResponse.data)

      // Check if authentication actually succeeded
      if (!loginResponse.data.authenticated) {
        throw new Error('Invalid token. Please check your token and try again.')
      }

      // Refresh auth status and data
      await checkAuthStatus()
      await fetchSummary()
      await fetchExpenses()
      await fetchIncome()

      console.log('Login successful! Session expires after 30 minutes.')
      setShowLogin(false) // Only close on success
    } catch (error) {
      console.error('Login error:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed'
      throw new Error(errorMessage)
    }
  }

  const handleLogout = async () => {
    try {
      // Call logout endpoint to clear httpOnly cookie
      await api.post('/api/auth/logout')
      console.log('Logout successful')
    } catch (error) {
      console.error('Logout error:', error)
      // Continue with logout even if API call fails
    }

    setAuthStatus({ authenticated: false, mode: 'guest' })

    // Refetch all data to get anonymized/normalized versions
    try {
      await Promise.all([
        fetchSummary().catch(err => console.error('Error refetching summary:', err)),
        fetchExpenses().catch(err => console.error('Error refetching expenses:', err)),
        fetchIncome().catch(err => console.error('Error refetching income:', err))
      ])
      console.log('Data refreshed with guest mode')
    } catch (error) {
      console.error('Error during logout data refresh:', error)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div>
            <h1>Finance Analysis Dashboard</h1>
            <p>Track and optimize your spending</p>
          </div>
          <div className="auth-status">
            {authStatus && (
              <>
                {authStatus.authenticated ? (
                  <div className="auth-badge trusted">
                    <span className="badge-icon">🔐</span>
                    <span>Trusted Mode</span>
                    <button onClick={handleLogout} className="logout-btn">Logout</button>
                  </div>
                ) : (
                  <div className="auth-badge guest">
                    <span className="badge-icon">👁️</span>
                    <span>Guest Mode (Normalized Data)</span>
                    <button onClick={() => setShowLogin(true)} className="login-btn">Login</button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={activeTab === 'expenses' ? 'active' : ''}
          onClick={() => setActiveTab('expenses')}
        >
          All Expenses
        </button>
        <button
          className={activeTab === 'income' ? 'active' : ''}
          onClick={() => setActiveTab('income')}
        >
          Income
          {!authStatus?.authenticated && <span className="privacy-icon"> 🔒</span>}
        </button>
        <button
          className={activeTab === 'insights' ? 'active' : ''}
          onClick={() => setActiveTab('insights')}
        >
          AI Insights
          {!authStatus?.authenticated && <span className="lock-icon"> 🔒</span>}
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' && summary && (
          <Dashboard summary={summary} />
        )}

        {activeTab === 'expenses' && (
          <ExpenseList expenses={expenses} loading={loading} />
        )}

        {activeTab === 'income' && (
          <ExpenseList
            expenses={income}
            loading={loading}
            isIncome={true}
          />
        )}

        {activeTab === 'insights' && (
          <AIInsights
            summary={summary}
            isAuthenticated={authStatus?.authenticated}
            onLoginClick={() => setShowLogin(true)}
          />
        )}
      </main>

      {showLogin && (
        <Login onLogin={handleLogin} onClose={() => setShowLogin(false)} />
      )}
    </div>
  )
}

export default App
