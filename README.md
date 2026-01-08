# Finance Analysis Dashboard

A secure, production-ready web application for analyzing your Toshl expense and income data with AI-powered insights. Access your financial dashboard securely from anywhere in the world.

## 🚀 Quick Start

**Ready to deploy?** → **[Deployment Guide](documentation/DEPLOYMENT.md)** (20-25 min, complete step-by-step)

## 📚 Documentation

- **[🚀 Deployment Guide](documentation/DEPLOYMENT.md)** - Complete Railway deployment (includes CSV upload via CLI)
- **[🔒 Security Guide](documentation/SECURITY.md)** - Security features & best practices
- **[🛠️ Development Guide](documentation/DEVELOPMENT.md)** - Local setup, architecture & API
- **[📦 UV Package Manager](documentation/UV_GUIDE.md)** - Dependency management with UV

## ✨ Features

### 📊 Core Features
- **Interactive Dashboard**: Beautiful charts showing spending by category, tags, and monthly/yearly trends
- **Income Tracking**: Full income analysis alongside expenses for complete financial picture
- **Smart Search**: Quickly find transactions by keyword (e.g., "skiing", "restaurant")
- **AI Insights**: Get personalized financial advice powered by Claude AI (authenticated users only)
- **Responsive Design**: Works seamlessly on phone, tablet, and desktop

### 🔐 Production-Ready Security
- **httpOnly Cookies**: Secure authentication protected against XSS attacks
- **HTTPS Enforcement**: Automatic SSL in production (Railway)
- **Rate Limiting**: Protection against brute force attacks (5 login attempts/min)
- **CORS Whitelist**: Only your domain can access the API
- **Data Obfuscation**: Guests see obfuscated data with daily-changing random factors (impossible to reverse-engineer)
- **Token-Based Auth**: Secure tokens for authorized users only
- **Auto-Expiring Sessions**: 30-minute session timeout for security

## Tech Stack

- **Frontend**: React 18 + Vite, Recharts for visualizations
- **Backend**: FastAPI (Python 3.13), Pandas for data processing
- **Package Management**: uv (fast Python package manager)
- **AI**: Anthropic Claude API for financial insights
- **Deployment**: Docker, Vercel, Railway support

## Quick Start

### Prerequisites

- Python 3.13+ with [uv](https://github.com/astral-sh/uv) installed
- Node.js 18+
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com/))

### Installation

#### Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Local Development

1. **Generate Authentication Tokens**
   ```bash
   cd backend
   python auth.py
   ```
   This will generate two secure tokens - one for you and one for your wife. Save these securely!

2. **Set up Backend**
   ```bash
   cd backend

   # Create .env file with your credentials
   cat > .env << EOF
   ANTHROPIC_API_KEY=your_anthropic_key_here
   AUTH_TOKEN_1=your_token_from_step_1
   AUTH_TOKEN_2=your_wife_token_from_step_1
   EOF

   # Install dependencies with uv
   uv pip install -e .

   # Start backend server
   uv run python main.py
   ```
   Backend will run at http://localhost:8000

3. **Set up Frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend will run at http://localhost:3000

4. **Open your browser**
   Navigate to http://localhost:3000

## Usage

### 🏠 Dashboard
View your overall financial statistics with interactive charts:
- **Summary Cards**: Total expenses, income, and net balance
- **Pie Chart**: Spending breakdown by category
- **Bar Chart**: Top spending tags
- **Line Chart**: Monthly spending trends over time
- **Yearly Summary**: Compare finances year-over-year

### 🔍 Search
Use the search bar to quickly find specific transactions:
- "skiing" - find all skiing-related expenses
- "restaurant" - see all restaurant spending
- "travel" - track travel costs
- Results show both expense and income totals

The search looks through categories, tags, and descriptions.

### 💰 Income Tab
View all your income transactions:
- Filter and browse income by date
- See income categories
- Track income trends alongside expenses

### 🤖 AI Insights (Authenticated Users Only)
Get personalized financial advice with Claude AI:
1. Login with your secure token
2. Click the "AI Insights" tab
3. Choose a quick question or ask your own
4. Get detailed analysis and actionable recommendations

Example questions:
- "What are my top spending categories and how can I reduce them?"
- "Analyze my income vs expenses ratio"
- "How can I optimize my monthly spending?"
- "Find unusual spending patterns"

### 🔐 Authentication

**Guest Mode (Default)**:
- View normalized data (all amounts scaled proportionally)
- Browse dashboard and search functionality
- Cannot access AI insights

**Trusted Mode (With Login)**:
- See real financial numbers
- Full access to AI insights
- Complete data analysis

**To Login**:
1. Click "Login" button in header
2. Enter your secure access token
3. Token is stored locally for convenience

**To Share Access**:
- Share your token securely (use password managers, in-person, or encrypted channels)
- Never share tokens via email or public chat
- Each person gets their own token

## Deployment

### Option 1: Docker (Self-Hosted)

```bash
# Using Docker Compose
docker-compose up -d

# Or build the full application
docker build -t finance-analysis .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  -e AUTH_TOKEN_1=token1 \
  -e AUTH_TOKEN_2=token2 \
  finance-analysis
```

### Option 2: Railway (Recommended for Full-Stack)

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI: `npm i -g @railway/cli`
3. Login: `railway login`
4. Initialize: `railway init`
5. Add environment variables:
   ```bash
   railway variables set ANTHROPIC_API_KEY=your_key
   railway variables set AUTH_TOKEN_1=your_token1
   railway variables set AUTH_TOKEN_2=your_token2
   ```
6. Deploy: `railway up`

### Option 3: Separate Frontend/Backend

**Backend on Railway:**
1. Create new project on Railway
2. Add Python service
3. Connect your GitHub repo
4. Set root directory to `backend`
5. Add environment variables: `ANTHROPIC_API_KEY`, `AUTH_TOKEN_1`, `AUTH_TOKEN_2`

**Frontend on Vercel:**
1. Import project on [vercel.com](https://vercel.com)
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-backend-url.railway.app`
4. Deploy

## API Endpoints

### Public Endpoints (work with normalized data for guests)
- `GET /api/summary` - Overall financial statistics
- `GET /api/expenses` - List expenses with filtering
- `GET /api/income` - List income transactions
- `GET /api/search?q=keyword` - Search transactions
- `GET /api/categories` - Get all categories
- `GET /api/tags` - Get all tags

### Authenticated Endpoints (require valid token)
- `GET /api/auth/status` - Check authentication status
- `POST /api/insights` - Get AI-powered financial insights

All endpoints automatically normalize data for unauthenticated requests.

## Project Structure

```
finance_analysis/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication & normalization
│   ├── pyproject.toml       # uv dependencies (Python 3.13)
│   ├── .python-version      # Python version specification
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── AIInsights.jsx
│   │   │   ├── ExpenseList.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   └── Login.jsx
│   │   ├── App.jsx          # Main app with auth
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── data/
│   └── [your-toshl-export].csv  # Your financial data
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # This file
```

## Environment Variables

### Backend (.env)
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key

# Authentication tokens (generate using: python auth.py)
AUTH_TOKEN_1=your_secure_token
AUTH_TOKEN_2=your_wife_secure_token
```

### Frontend (.env.local)
```bash
VITE_API_URL=http://localhost:8000  # Backend URL
```

## Security Features

### How Data Normalization Works

When guests (unauthenticated users) access the app:
1. All monetary amounts are multiplied by a normalization factor
2. Factor is calculated to make 2021 expenses appear as 10,000 EUR
3. Relative proportions are maintained (10% of budget stays 10%)
4. Categories, tags, and dates remain unchanged
5. AI insights are completely blocked

**Why This Approach?**
- You can safely share the app link with friends/family
- They can see the interface and features without your real data
- Maintains privacy while allowing demonstrations
- Only you and your wife see real numbers

### Token Security Best Practices

1. **Generate Strong Tokens**: Use the provided `auth.py` script
2. **Store Securely**: Keep tokens in password managers
3. **Share Safely**: Use encrypted channels for sharing
4. **Rotate Regularly**: Generate new tokens periodically
5. **Monitor Access**: Check auth logs if suspicious activity

### Future Security Enhancements

Consider adding:
- Token expiration dates
- Rate limiting per token
- Audit logging of authenticated actions
- Two-factor authentication
- Session management with Redis

## Troubleshooting

### Backend Issues

**CSV not found**
- Ensure your Toshl export CSV is in the `data/` folder
- The backend auto-detects any `.csv` file

**Authentication not working**
- Run `python auth.py` to generate tokens
- Ensure tokens are in `.env` file
- Restart backend after updating `.env`
- Check token format (no quotes, exact match)

**uv installation issues**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

**API key error**
- Create `.env` in `backend/` directory
- Add: `ANTHROPIC_API_KEY=your_key`
- Get key from https://console.anthropic.com/
- Restart backend server

**CORS errors**
- Update `allow_origins` in [backend/main.py:16](backend/main.py#L16)
- Add your frontend URL

### Frontend Issues

**Cannot connect to backend**
- Ensure backend is running on port 8000
- Check `VITE_API_URL` environment variable
- Verify proxy settings in [frontend/vite.config.js](frontend/vite.config.js)

**Login not working**
- Clear browser localStorage
- Check token format (no spaces)
- Verify backend has AUTH_TOKEN variables set
- Check browser console for errors

**Charts not displaying**
- Check browser console for errors
- Ensure backend is returning data: http://localhost:8000/api/summary
- Verify data has valid dates and amounts

## Development with uv

### Why uv?

- **10-100x faster** than pip for dependency resolution
- **Automatic virtual environment** management
- **Python 3.13** support out of the box
- **Lockfile** for reproducible builds
- **Drop-in replacement** for pip

### Common uv Commands

```bash
# Install dependencies
uv pip install -e .

# Add a new dependency
uv pip install package-name

# Run Python with uv
uv run python main.py

# Update dependencies
uv pip install --upgrade -e .

# Show installed packages
uv pip list
```

## Data Privacy Notice

This application processes financial data **locally or on your infrastructure**:
- No data is sent to third parties except Claude API for insights
- Claude API calls only happen when you explicitly request AI analysis
- Only authenticated users can trigger AI analysis
- Guest users see normalized data only
- Your CSV data stays on your server

## Contributing

Feel free to fork and customize. Some ideas:
- Add budget tracking and alerts
- Export reports to PDF
- Multi-currency support improvements
- Connect directly to Toshl API for real-time sync
- Add more charts (savings rate, category trends over time)
- Mobile app using React Native
- Automated monthly reports via email

## License

MIT License - use freely for personal or commercial projects.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at http://localhost:8000/docs (when backend running)
3. Check uv documentation: https://github.com/astral-sh/uv
4. Consult [FastAPI docs](https://fastapi.tiangolo.com/) or [React docs](https://react.dev/)

## Credits

- **Expense Tracking**: [Toshl Finance](https://toshl.com/)
- **AI**: [Anthropic Claude](https://anthropic.com/)
- **Package Management**: [uv by Astral](https://github.com/astral-sh/uv)
- **Charts**: [Recharts](https://recharts.org/)

---

**API Key**: Get your Anthropic API key at https://console.anthropic.com/

**Cost Estimate**: Typical usage costs a few cents per month for personal use with AI insights.
