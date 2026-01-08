import React, { useState } from 'react'
import axios from 'axios'
import './AIInsights.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function AIInsights({ summary, isAuthenticated, onLoginClick }) {
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [customQuery, setCustomQuery] = useState('')

  const getInsights = async (query = null) => {
    if (!isAuthenticated) {
      onLoginClick()
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_BASE}/api/insights`, {
        query: query || undefined
      })
      setInsights(response.data)
    } catch (err) {
      if (err.response?.status === 403) {
        setError('Please log in to access AI insights')
        onLoginClick()
      } else {
        setError(err.response?.data?.detail || 'Failed to get AI insights. Make sure ANTHROPIC_API_KEY is set.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleCustomQuery = (e) => {
    e.preventDefault()
    if (customQuery.trim()) {
      getInsights(customQuery)
    }
  }

  const quickQuestions = [
    "What are my top spending categories and how can I reduce them?",
    "Analyze my restaurant spending habits",
    "How can I optimize my monthly expenses?",
    "What percentage of my income should I save?",
    "Find unusual or irregular spending patterns"
  ]

  return (
    <div className="ai-insights">
      <div className="insights-header">
        <h2>AI-Powered Financial Insights</h2>
        <p>Get personalized advice based on your spending patterns</p>
        {!isAuthenticated && (
          <div className="auth-required-notice">
            🔒 Login required to access AI insights with your real data
          </div>
        )}
      </div>

      <div className="query-section">
        <div className="quick-questions">
          <h3>Quick Questions</h3>
          <div className="question-buttons">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => getInsights(question)}
                disabled={loading}
                className="question-btn"
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        <div className="custom-query">
          <h3>Ask Your Own Question</h3>
          <form onSubmit={handleCustomQuery}>
            <input
              type="text"
              placeholder="e.g., How much do I spend on skiing compared to other sports?"
              value={customQuery}
              onChange={(e) => setCustomQuery(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !customQuery.trim()}>
              {loading ? 'Analyzing...' : 'Get Insights'}
            </button>
          </form>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <h3>AI Insights Not Available</h3>
          <p>{error}</p>
          {error.includes('ANTHROPIC_API_KEY') && (
            <div className="setup-instructions">
              <h4>To enable AI insights:</h4>
              <ol>
                <li>Get your API key from <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer">console.anthropic.com</a></li>
                <li>Edit <code>backend/.env</code> file</li>
                <li>Add: <code>ANTHROPIC_API_KEY=your_api_key_here</code></li>
                <li>Restart the backend server</li>
              </ol>
              <div className="cost-estimate">
                <strong>💰 Cost Estimate:</strong> AI insights cost approximately $0.001-0.005 per query.
                Typical monthly usage for personal finance: <strong>$0.50-2.00/month</strong>
              </div>
            </div>
          )}
        </div>
      )}

      {loading && (
        <div className="loading-insights">
          <div className="spinner"></div>
          <p>Analyzing your spending patterns with AI...</p>
        </div>
      )}

      {insights && !loading && (
        <div className="insights-result">
          <h3>AI Analysis</h3>
          <div className="query-display">
            <strong>Question:</strong> {insights.query}
          </div>
          <div className="insights-content">
            {insights.insights.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>
      )}

      {!insights && !loading && !error && (
        <div className="placeholder">
          <p>Click on a quick question or ask your own to get AI-powered insights about your spending.</p>
        </div>
      )}
    </div>
  )
}

export default AIInsights
