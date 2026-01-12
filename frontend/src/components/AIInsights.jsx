import React, { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import './AIInsights.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function AIInsights({ summary, isAuthenticated, onLoginClick }) {
  const [chatHistory, setChatHistory] = useState([])
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

    // Add user message to chat
    const userMessage = { role: 'user', content: query || 'Analyze my spending' }
    setChatHistory(prev => [...prev, userMessage])

    try {
      const response = await axios.post(`${API_BASE}/api/insights`, {
        query: query || undefined
      }, {
        withCredentials: true  // Send cookies with request
      })

      // Add AI response to chat
      const aiMessage = { role: 'assistant', content: response.data.insights }
      setChatHistory(prev => [...prev, aiMessage])
      setCustomQuery('') // Clear input after successful query
    } catch (err) {
      // Remove user message if request failed
      setChatHistory(prev => prev.slice(0, -1))

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

  const clearChat = () => {
    setChatHistory([])
    setError(null)
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
        <h2>💬 AI Financial Advisor</h2>
        <p>Get personalized advice based on your spending patterns</p>
        {!isAuthenticated && (
          <div className="auth-required-notice">
            🔒 Login required to access AI insights with your real data
          </div>
        )}
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

      {/* Chat Window */}
      <div className="chat-container">
        <div className="chat-header">
          <span>💬 Conversation</span>
          {chatHistory.length > 0 && (
            <button onClick={clearChat} className="clear-chat-btn">Clear Chat</button>
          )}
        </div>

        <div className="chat-messages">
          {chatHistory.length === 0 && !loading && (
            <div className="chat-placeholder">
              <p>👋 Hello! I'm your AI financial advisor.</p>
              <p>Ask me anything about your spending, income, or financial habits.</p>
            </div>
          )}

          {chatHistory.map((message, index) => (
            <div key={index} className={`chat-message ${message.role}`}>
              <div className="message-avatar">
                {message.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                {message.role === 'user' ? (
                  <p>{message.content}</p>
                ) : (
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <p className="analyzing-text">Analyzing your financial data...</p>
              </div>
            </div>
          )}
        </div>

        {/* Input Section */}
        <div className="chat-input-section">
          <div className="quick-questions">
            <h4>💡 Quick Questions:</h4>
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

          <form onSubmit={handleCustomQuery} className="chat-input-form">
            <input
              type="text"
              placeholder="Ask me anything about your finances..."
              value={customQuery}
              onChange={(e) => setCustomQuery(e.target.value)}
              disabled={loading}
              className="chat-input"
            />
            <button type="submit" disabled={loading || !customQuery.trim()} className="send-btn">
              {loading ? '⏳' : '📤'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default AIInsights
