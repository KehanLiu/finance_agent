import React, { useState } from 'react'
import './Login.css'

function Login({ onLogin, onClose }) {
  const [token, setToken] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!token.trim()) {
      setError('Please enter your access token')
      return
    }
    setLoading(true)
    setError('')
    try {
      await onLogin(token)
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-overlay" onClick={onClose}>
      <div className="login-modal" onClick={(e) => e.stopPropagation()}>
        <div className="login-header">
          <h2>🔐 Login</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="login-content">
          <p className="login-description">
            Enter your secure access token to view real financial data and access AI insights.
          </p>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="token">Access Token</label>
              <input
                type="password"
                id="token"
                value={token}
                onChange={(e) => {
                  setToken(e.target.value)
                  setError('')
                }}
                placeholder="Enter your secure token"
                autoFocus
              />
              {error && <span className="error-message">{error}</span>}
            </div>

            <button type="submit" className="login-submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className="login-info">
            <h3>How to get your token:</h3>
            <ol>
              <li>Check your <code>backend/.env</code> file for AUTH_TOKEN_1 or AUTH_TOKEN_2</li>
              <li><strong>Important:</strong> Only paste the token value (after the = sign)</li>
              <li>Example: If your .env shows <code>AUTH_TOKEN_1=abc123xyz</code>, paste only <code>abc123xyz</code></li>
            </ol>

            <div className="guest-mode-info">
              <strong>Guest Mode:</strong> Without logging in, you can still explore the dashboard
              with normalized data (all amounts scaled proportionally for privacy).
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
