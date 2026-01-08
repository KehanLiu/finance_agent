# 🛠️ Development Guide

Complete guide for local development, architecture, and contributing to the Finance Analysis Dashboard.

---

## 🏗️ Architecture Overview

### Technology Stack

**Frontend**:
- React 18.3.1 + Vite 6.0.5
- Recharts 2.14.1 (visualizations)
- Axios 1.7.9 (HTTP client)
- Dark mode CSS with glassmorphism

**Backend**:
- FastAPI 0.115.12 + Uvicorn 0.34.0
- Python 3.13 + pandas 2.2.3
- slowapi 0.1.9 (rate limiting)
- Token-based authentication
- Data normalization & anonymization

**Deployment**:
- Docker (multi-stage build)
- Railway.app (hosting)
- GitHub (version control)

### System Architecture

```
┌─────────────────────────────────────────────┐
│            Internet/User Browser             │
│         (Anywhere in the world)              │
└────────────────┬────────────────────────────┘
                 │ HTTPS (Railway SSL)
                 ▼
┌─────────────────────────────────────────────┐
│           Railway Application                │
│  ┌────────────────────────────────────────┐ │
│  │       FastAPI Backend                  │ │
│  │  - API Endpoints (/api/*)              │ │
│  │  - Authentication (httpOnly cookies)   │ │
│  │  - Rate Limiting (slowapi)             │ │
│  │  - Data Processing (pandas)            │ │
│  │  - Static File Serving                 │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │       React Frontend (built)           │ │
│  │  - Dashboard UI                        │ │
│  │  - Charts (Recharts)                   │ │
│  │  - Authentication Flow                 │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │           Data                         │ │
│  │  - CSV Files                           │ │
│  │  - Environment Variables               │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      External Services                       │
│  - Anthropic API (Claude AI Insights)       │
└─────────────────────────────────────────────┘
```

### Data Flow

```
1. User Request
   Browser → HTTPS → Railway → FastAPI

2. Authentication
   httpOnly Cookie → verify_token() → True/False

3. Data Processing
   CSV Files → pandas → normalize (if guest) → JSON

4. Response
   JSON → React → Recharts → Rendered UI
```

### File Structure

```
finance_analysis/
├── backend/
│   ├── main.py              # API endpoints
│   ├── auth.py              # Authentication logic
│   ├── .env                 # Environment variables (DO NOT COMMIT)
│   ├── .env.example         # Template
│   ├── requirements.txt     # Python dependencies
│   └── pyproject.toml       # Modern Python config
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main application
│   │   ├── components/
│   │   │   ├── Dashboard.jsx       # Main dashboard
│   │   │   ├── ExpenseList.jsx     # Transaction list
│   │   │   ├── AIInsights.jsx      # AI features
│   │   │   └── Login.jsx           # Login modal
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── .env                 # Frontend config (DO NOT COMMIT)
│
├── data/
│   └── *.csv                # Financial data (DO NOT COMMIT)
│
├── documentation/
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── SECURITY.md          # Security documentation
│   └── DEVELOPMENT.md       # This file
│
├── Dockerfile.production    # Production build
├── railway.toml            # Railway config
├── .gitignore              # Git ignore rules
└── README.md               # Project overview
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.13+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)
- Anthropic API key

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal or:
export PATH="$HOME/.cargo/bin:$PATH"
```

### Step 1: Generate Tokens

```bash
cd backend
python auth.py
```

Save the output tokens.

### Step 2: Configure Backend

Create `backend/.env`:

```env
ANTHROPIC_API_KEY=your_api_key_here
AUTH_TOKEN_1=token_from_step_1
AUTH_TOKEN_2=token_from_step_1
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3001,http://localhost:5173
```

### Step 3: Configure Frontend

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### Step 4: Install Dependencies

**Backend**:
```bash
cd backend
uv pip install -e .
# Or: pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

### Step 5: Add Your Data

Place CSV export from Toshl in `data/` folder:
```bash
cp ~/Downloads/toshl_export.csv data/
```

### Step 6: Run Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### Step 7: Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔧 Development Workflow

### Making Changes

**Backend Changes**:
1. Edit files in `backend/`
2. Server auto-reloads (with `--reload`)
3. Test API at http://localhost:8000/docs
4. Verify changes in frontend

**Frontend Changes**:
1. Edit files in `frontend/src/`
2. Vite auto-reloads browser
3. Check browser console for errors
4. Test all features

**Data Changes**:
1. Update CSV files in `data/`
2. Restart backend server
3. Refresh browser

### Testing

**Manual Testing**:
```bash
# Test guest mode
1. Open app without logging in
2. Verify normalized data shows
3. Check AI insights are blocked

# Test authenticated mode
1. Click Login
2. Paste token
3. Verify real data shows
4. Test AI insights
5. Test logout
```

**API Testing**:
```bash
# Use built-in Swagger UI
open http://localhost:8000/docs

# Or use curl
curl http://localhost:8000/api/summary
curl -H "Cookie: session_token=YOUR_TOKEN" \
  http://localhost:8000/api/summary
```

### Debugging

**Backend Debugging**:
```python
# Add print statements
print(f"[DEBUG] Variable: {variable}")

# Check logs
# Uvicorn shows all output in terminal
```

**Frontend Debugging**:
```javascript
// Browser console
console.log('Debug:', data)

// React DevTools
// Install browser extension
```

**Network Debugging**:
```
1. Open Browser DevTools (F12)
2. Network tab
3. Filter: Fetch/XHR
4. Check request/response
```

---

## 📦 Key Features Explained

### Authentication System

**Flow**:
```
1. User enters token
2. Frontend → POST /api/auth/login
3. Backend validates against TRUSTED_TOKENS
4. If valid: Set httpOnly cookie (30 min)
5. If invalid: Return 401 error
6. All API requests include cookie
7. Backend checks cookie in verify_token()
8. Returns True (trusted) or False (guest)
```

**Code**:
```python
# backend/auth.py
def verify_token(
    session_token: Optional[str] = Cookie(None)
) -> bool:
    if session_token in TRUSTED_TOKENS:
        return True
    return False

# backend/main.py
@app.get("/api/expenses")
def get_expenses(is_trusted: bool = Depends(verify_token)):
    if is_trusted:
        return real_data
    return normalized_data
```

### Data Normalization

**Purpose**: Protect privacy for guest users

**Method**:
```python
# Calculate factor based on 2021 expenses
actual_2021 = df[df['Date'].dt.year == 2021]['Expense amount'].sum()
factor = 10000 / actual_2021  # Target: 10k EUR

# Apply to all amounts
normalized = amount * factor
```

**Preserves**:
- ✅ Relative proportions
- ✅ Spending patterns
- ✅ Category distributions
- ✅ Time trends

**Hides**:
- ❌ Actual amounts
- ❌ Income sources
- ❌ Real categories (income)

### Rate Limiting

**Implementation**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")
def login(request: Request, ...):
    # Only 5 attempts per IP per minute
```

**Limits**:
- Login: 5/minute per IP
- AI Insights: 10/minute per IP

**Response on Limit**:
```
429 Too Many Requests
{
  "error": "Rate limit exceeded"
}
```

### Static File Serving

**Production Only**:
```python
FRONTEND_DIST = "../frontend/dist"
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(...))

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve frontend files
        # Fall back to index.html for SPA routing
```

**Benefit**: Single deployment for frontend + backend

---

## 🔌 API Endpoints

### Authentication

**POST /api/auth/login**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_TOKEN"}'
```

**POST /api/auth/logout**
```bash
curl -X POST http://localhost:8000/api/auth/logout \
  --cookie "session_token=YOUR_TOKEN"
```

**GET /api/auth/status**
```bash
curl http://localhost:8000/api/auth/status \
  --cookie "session_token=YOUR_TOKEN"
```

### Data Endpoints

**GET /api/summary**
```bash
# Returns: total expenses, income, categories, etc.
curl http://localhost:8000/api/summary
```

**GET /api/expenses**
```bash
# Query params: category, tag, search, start_date, end_date, limit, offset
curl "http://localhost:8000/api/expenses?category=Food&limit=10"
```

**GET /api/income**
```bash
curl http://localhost:8000/api/income
```

**GET /api/categories**
```bash
curl http://localhost:8000/api/categories
```

**GET /api/tags**
```bash
curl http://localhost:8000/api/tags
```

**POST /api/insights** (Authenticated Only)
```bash
curl -X POST http://localhost:8000/api/insights \
  -H "Content-Type: application/json" \
  --cookie "session_token=YOUR_TOKEN" \
  -d '{"query": "How can I save more money?"}'
```

**GET /api/search**
```bash
curl "http://localhost:8000/api/search?q=restaurant&limit=50"
```

---

## 🎨 Frontend Components

### App.jsx
- Main application container
- Authentication state management
- API client setup
- Tab navigation

### Dashboard.jsx
- Summary statistics
- Charts (monthly cashflow, category breakdown, etc.)
- Responsive grid layout

### ExpenseList.jsx
- Transaction table
- Filtering and search
- Pagination
- Used for both expenses and income

### AIInsights.jsx
- AI query interface
- Response display
- Authentication check

### Login.jsx
- Login modal
- Token input
- Error handling

---

## 📝 Adding Features

### New API Endpoint

1. **Add to backend/main.py**:
```python
@app.get("/api/new-endpoint")
def new_endpoint(is_trusted: bool = Depends(verify_token)):
    # Your logic here
    return {"data": result}
```

2. **Add rate limiting if needed**:
```python
@app.get("/api/new-endpoint")
@limiter.limit("20/minute")
def new_endpoint(request: Request, ...):
    ...
```

3. **Test in Swagger UI**:
```
http://localhost:8000/docs
```

### New Frontend Component

1. **Create component**:
```javascript
// frontend/src/components/NewFeature.jsx
import React from 'react'

function NewFeature({ data }) {
  return (
    <div className="new-feature">
      {/* Your UI */}
    </div>
  )
}

export default NewFeature
```

2. **Import in App.jsx**:
```javascript
import NewFeature from './components/NewFeature'

// Add to render
{activeTab === 'newfeature' && (
  <NewFeature data={someData} />
)}
```

3. **Add CSS if needed**:
```css
/* frontend/src/components/NewFeature.css */
.new-feature {
  /* Your styles */
}
```

---

## 🧪 Testing Checklist

Before deploying:

**Backend**:
- [ ] All endpoints return correct data
- [ ] Authentication works (valid/invalid tokens)
- [ ] Rate limiting triggers after limit
- [ ] Guest mode returns normalized data
- [ ] Trusted mode returns real data
- [ ] AI insights require authentication
- [ ] CORS works for allowed origins
- [ ] No errors in server logs

**Frontend**:
- [ ] Dashboard loads without errors
- [ ] Charts render correctly
- [ ] Login/logout works
- [ ] Token validation shows errors
- [ ] Guest mode shows normalized data
- [ ] Trusted mode shows real data
- [ ] AI insights only available when logged in
- [ ] No console errors
- [ ] Responsive on mobile

**Security**:
- [ ] `.env` files not committed
- [ ] CSV files not committed
- [ ] Tokens work in production
- [ ] httpOnly cookies set correctly
- [ ] CORS whitelist configured
- [ ] Rate limiting active
- [ ] HTTPS enforced (production)

---

## 🔄 Updating Dependencies

### Backend

```bash
cd backend

# Check for updates
uv pip list --outdated

# Update specific package
uv pip install --upgrade fastapi

# Update all
uv pip install --upgrade -r requirements.txt

# Test after updating!
```

### Frontend

```bash
cd frontend

# Check for updates
npm outdated

# Update specific package
npm update recharts

# Update all
npm update

# Test after updating!
```

---

## 📚 Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- Recharts: https://recharts.org
- Railway: https://docs.railway.app

### Tools
- uv: https://github.com/astral-sh/uv
- Vite: https://vitejs.dev
- Anthropic API: https://docs.anthropic.com

---

## 🐛 Common Issues

### "No CSV file found"
**Solution**: Add CSV files to `data/` folder

### "ANTHROPIC_API_KEY not configured"
**Solution**: Add key to `backend/.env`

### "Invalid token"
**Solution**: Check token in `.env` matches what you're pasting

### CORS errors in browser
**Solution**: Check `CORS_ORIGINS` in `.env` matches frontend URL

### Frontend not loading
**Solution**: Make sure both backend and frontend servers are running

### Rate limit exceeded
**Solution**: Wait 1 minute and try again

---

## ✅ Development Checklist

**Initial Setup**:
- [ ] Installed Python 3.13+
- [ ] Installed Node.js 18+
- [ ] Installed uv
- [ ] Generated tokens
- [ ] Created `.env` files
- [ ] Added CSV data
- [ ] Installed dependencies

**Daily Development**:
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Browser DevTools open
- [ ] Tested changes manually
- [ ] No errors in console
- [ ] Git commits made

**Before Pushing**:
- [ ] Code tested locally
- [ ] No `.env` files committed
- [ ] No CSV files committed
- [ ] No secrets in code
- [ ] Documentation updated if needed

---

**Ready to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)
