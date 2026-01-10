from fastapi import FastAPI, HTTPException, Depends, Header, Response, Request, UploadFile, File
import tempfile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import os
from datetime import datetime
from collections import defaultdict
import anthropic
from dotenv import load_dotenv
try:
    from backend.auth import verify_token, normalize_amount, get_normalization_factor, anonymize_income_entry, TRUSTED_TOKENS, anonymize_income_text
except ImportError:
    from auth import verify_token, normalize_amount, get_normalization_factor, anonymize_income_entry, TRUSTED_TOKENS, anonymize_income_text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load environment variables
load_dotenv()

# Initialize database (PostgreSQL on Railway, CSV fallback for local)
try:
    from backend.database import init_db, get_db
    from backend.db_operations import get_all_transactions_as_dataframe
except ImportError:
    from database import init_db, get_db
    from db_operations import get_all_transactions_as_dataframe

# Initialize database connection
print("[STARTUP] Initializing database...")
print(f"[STARTUP] DATABASE_URL present: {bool(os.getenv('DATABASE_URL'))}")
USE_DATABASE = bool(os.getenv("DATABASE_URL"))
if USE_DATABASE:
    try:
        init_db()
        print("[DB] PostgreSQL database initialized successfully")
    except Exception as e:
        print(f"[DB ERROR] Failed to initialize database: {e}")
        import traceback
        traceback.print_exc()
        raise
else:
    print("[DB] No DATABASE_URL found - using CSV fallback mode")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Finance Analysis API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Get allowed origins from environment variable (comma-separated)
# Default to localhost for development
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3001,http://localhost:5173").split(",")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Load CSV data (optional at startup - will be loaded when endpoints are accessed)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
df = None
NORMALIZATION_FACTOR = None

def load_data(db=None):
    """
    Load financial data - from PostgreSQL if available, otherwise CSV fallback

    Args:
        db: Database session (optional, for PostgreSQL mode)

    Returns:
        pandas DataFrame with financial data
    """
    global df, NORMALIZATION_FACTOR

    # If using PostgreSQL and db session provided
    if USE_DATABASE and db is not None:
        df = get_all_transactions_as_dataframe(db)
        if df.empty:
            raise HTTPException(status_code=503, detail="No financial data in database. Please run migration script.")
        NORMALIZATION_FACTOR = get_normalization_factor(df)
        return df

    # CSV fallback mode (for local development or if no DB)
    if df is not None:
        return df

    csv_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.csv')]
    if not csv_files:
        raise HTTPException(status_code=503, detail="No financial data available. Please upload CSV files or configure DATABASE_URL.")

    CSV_FILE = os.path.join(DATA_PATH, csv_files[0])
    df = pd.read_csv(CSV_FILE)

    # Data cleaning
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
    df['Expense amount'] = df['Expense amount'].replace(',', '', regex=True).astype(float)
    df['Income amount'] = df['Income amount'].replace(',', '', regex=True).astype(float)
    df['In main currency'] = df['In main currency'].replace(',', '', regex=True).astype(float)
    df = df.sort_values('Date', ascending=False)

    # Calculate normalization factor once at startup
    NORMALIZATION_FACTOR = get_normalization_factor(df)

    return df

class ExpenseFilter(BaseModel):
    category: Optional[str] = None
    tag: Optional[str] = None
    search: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

class AIInsightRequest(BaseModel):
    query: Optional[str] = None
    time_period: Optional[str] = "all"

def apply_data_normalization(data: dict, is_trusted: bool) -> dict:
    """Apply normalization to financial data if user is not trusted"""
    if is_trusted:
        return data

    # Normalize all monetary values
    if 'total_expenses' in data:
        data['total_expenses'] = normalize_amount(data['total_expenses'], NORMALIZATION_FACTOR)
    if 'total_income' in data:
        data['total_income'] = normalize_amount(data['total_income'], NORMALIZATION_FACTOR)
    if 'net' in data:
        data['net'] = normalize_amount(data['net'], NORMALIZATION_FACTOR)

    if 'category_breakdown' in data:
        data['category_breakdown'] = {
            k: normalize_amount(v, NORMALIZATION_FACTOR)
            for k, v in data['category_breakdown'].items()
        }

    if 'monthly_summary' in data:
        data['monthly_summary'] = {
            k: {
                'expenses': normalize_amount(v['expenses'], NORMALIZATION_FACTOR),
                'income': normalize_amount(v['income'], NORMALIZATION_FACTOR),
                'net': normalize_amount(v['net'], NORMALIZATION_FACTOR)
            }
            for k, v in data['monthly_summary'].items()
        }

    if 'yearly_summary' in data:
        data['yearly_summary'] = {
            k: {
                'expenses': normalize_amount(v['expenses'], NORMALIZATION_FACTOR),
                'income': normalize_amount(v['income'], NORMALIZATION_FACTOR),
                'net': normalize_amount(v['net'], NORMALIZATION_FACTOR)
            }
            for k, v in data['yearly_summary'].items()
        }

    if 'top_tags' in data:
        data['top_tags'] = {
            k: normalize_amount(v, NORMALIZATION_FACTOR)
            for k, v in data['top_tags'].items()
        }

    if 'income_breakdown' in data:
        data['income_breakdown'] = {
            k: normalize_amount(v, NORMALIZATION_FACTOR)
            for k, v in data['income_breakdown'].items()
        }

    return data

def normalize_expenses_list(expenses: list, is_trusted: bool) -> list:
    """Normalize expense amounts in a list"""
    if is_trusted:
        return expenses

    for expense in expenses:
        if 'Expense amount' in expense:
            expense['Expense amount'] = normalize_amount(expense['Expense amount'], NORMALIZATION_FACTOR)
        if 'Income amount' in expense:
            expense['Income amount'] = normalize_amount(expense['Income amount'], NORMALIZATION_FACTOR)
        if 'In main currency' in expense:
            expense['In main currency'] = normalize_amount(expense['In main currency'], NORMALIZATION_FACTOR)

    return expenses

class LoginRequest(BaseModel):
    token: str

@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    # Updated: 2026-01-10 - PostgreSQL migration with lazy initialization
    return {"message": "Finance Analysis API", "status": "running", "database": "postgresql" if USE_DATABASE else "csv"}

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
def login(request: Request, login_request: LoginRequest, response: Response):
    """Login endpoint that sets httpOnly cookie"""
    token = login_request.token.strip()

    if token in TRUSTED_TOKENS:
        # Set secure httpOnly cookie
        is_production = os.getenv("ENVIRONMENT", "development") == "production"
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,  # Not accessible to JavaScript
            secure=is_production,  # Only over HTTPS in production
            samesite="lax",  # CSRF protection
            max_age=1800,  # 30 minutes
            path="/"
        )
        return {
            "success": True,
            "authenticated": True,
            "mode": "trusted",
            "message": "Login successful"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/logout")
def logout(response: Response):
    """Logout endpoint that clears the cookie"""
    response.delete_cookie(key="session_token", path="/")
    return {
        "success": True,
        "authenticated": False,
        "mode": "guest",
        "message": "Logged out successfully"
    }

@app.get("/api/auth/status")
def auth_status(is_trusted: bool = Depends(verify_token)):
    """Check authentication status"""
    print(f"[AUTH] Auth status check: is_trusted={is_trusted}")
    return {
        "authenticated": is_trusted,
        "mode": "trusted" if is_trusted else "guest",
        "message": "Real data" if is_trusted else "Viewing normalized data for privacy"
    }

@app.get("/api/expenses")
def get_expenses(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 10000,
    offset: int = 0,
    is_trusted: bool = Depends(verify_token),
    db=Depends(get_db)
):
    """Get filtered expenses"""
    data = load_data(db)
    filtered_df = data.copy()

    if category:
        filtered_df = filtered_df[filtered_df['Category'].str.contains(category, case=False, na=False)]

    if tag:
        filtered_df = filtered_df[filtered_df['Tags'].str.contains(tag, case=False, na=False)]

    if search:
        mask = (
            filtered_df['Category'].str.contains(search, case=False, na=False) |
            filtered_df['Tags'].str.contains(search, case=False, na=False) |
            filtered_df['Description'].str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]

    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]

    total = len(filtered_df)
    filtered_df = filtered_df.iloc[offset:offset + limit]

    records = filtered_df.to_dict('records')
    for record in records:
        if pd.isna(record['Date']):
            record['Date'] = None
        else:
            record['Date'] = record['Date'].isoformat()

        for key in record:
            if pd.isna(record[key]):
                record[key] = None

    records = normalize_expenses_list(records, is_trusted)

    return {
        "total": total,
        "expenses": records,
        "limit": limit,
        "offset": offset,
        "is_normalized": not is_trusted
    }

@app.get("/api/income")
def get_income(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 10000,
    offset: int = 0,
    is_trusted: bool = Depends(verify_token),
    db=Depends(get_db)
):
    """Get income entries"""
    data = load_data(db)
    income_df = data[data['Income amount'] > 0].copy()

    if start_date:
        income_df = income_df[income_df['Date'] >= pd.to_datetime(start_date)]

    if end_date:
        income_df = income_df[income_df['Date'] <= pd.to_datetime(end_date)]

    total = len(income_df)
    income_df = income_df.iloc[offset:offset + limit]

    records = income_df.to_dict('records')
    for record in records:
        if pd.isna(record['Date']):
            record['Date'] = None
        else:
            record['Date'] = record['Date'].isoformat()

        for key in record:
            if pd.isna(record[key]):
                record[key] = None

    # Apply anonymization and normalization for guest users
    if not is_trusted:
        normalization_factor = get_normalization_factor(df)
        records = [anonymize_income_entry(record, normalization_factor) for record in records]

    return {
        "total": total,
        "income": records,
        "limit": limit,
        "offset": offset,
        "is_normalized": not is_trusted
    }

@app.get("/api/summary")
def get_summary(is_trusted: bool = Depends(verify_token), db=Depends(get_db)):
    """Get overall spending and income summary"""
    data = load_data(db)
    # Use 'In main currency' for EUR-converted amounts
    df_expenses = data[data['Expense amount'] > 0].copy()
    df_income = data[data['Income amount'] > 0].copy()

    total_expenses = df_expenses['In main currency'].sum()
    total_income = df_income['In main currency'].sum()

    category_summary = df_expenses.groupby('Category')['In main currency'].sum().sort_values(ascending=False).to_dict()
    income_by_category_raw = df_income.groupby('Category')['In main currency'].sum().sort_values(ascending=False).to_dict()

    # Anonymize income categories for guests
    if not is_trusted:
        income_by_category = {}
        for category, amount in income_by_category_raw.items():
            anonymized_cat = anonymize_income_text(str(category))
            # Aggregate amounts for same anonymized category
            income_by_category[anonymized_cat] = income_by_category.get(anonymized_cat, 0) + amount
    else:
        income_by_category = income_by_category_raw

    df_with_month = data.copy()
    df_with_month['Month'] = df_with_month['Date'].dt.to_period('M').astype(str)
    monthly_expenses = df_with_month[df_with_month['Expense amount'] > 0].groupby('Month')['In main currency'].sum().to_dict()
    monthly_income = df_with_month[df_with_month['Income amount'] > 0].groupby('Month')['In main currency'].sum().to_dict()

    all_months = set(monthly_expenses.keys()) | set(monthly_income.keys())
    monthly_summary = {
        month: {
            'expenses': float(monthly_expenses.get(month, 0)),
            'income': float(monthly_income.get(month, 0)),
            'net': float(monthly_income.get(month, 0)) - float(monthly_expenses.get(month, 0))
        }
        for month in sorted(all_months)
    }

    tag_summary = {}
    for _, row in df_expenses.iterrows():
        if pd.notna(row['Tags']):
            tags = str(row['Tags']).split(',')
            for tag in tags:
                tag = tag.strip()
                if tag:
                    tag_summary[tag] = tag_summary.get(tag, 0) + row['In main currency']

    tag_summary = dict(sorted(tag_summary.items(), key=lambda x: x[1], reverse=True)[:20])

    df_with_year = data.copy()
    df_with_year['Year'] = df_with_year['Date'].dt.year
    yearly_summary = {}
    for year in df_with_year['Year'].dropna().unique():
        year_data = df_with_year[df_with_year['Year'] == year]
        year_expenses = year_data[year_data['Expense amount'] > 0]['In main currency'].sum()
        year_income = year_data[year_data['Income amount'] > 0]['In main currency'].sum()
        yearly_summary[int(year)] = {
            'expenses': float(year_expenses),
            'income': float(year_income),
            'net': float(year_income - year_expenses)
        }

    result = {
        "total_expenses": float(total_expenses),
        "total_income": float(total_income),
        "net": float(total_income - total_expenses),
        "category_breakdown": category_summary,
        "income_breakdown": income_by_category,
        "monthly_summary": monthly_summary,
        "yearly_summary": yearly_summary,
        "top_tags": tag_summary,
        "currency": data['Main currency'].mode()[0] if len(df) > 0 else "EUR",
        "date_range": {
            "start": data['Date'].min().isoformat() if pd.notna(data['Date'].min()) else None,
            "end": data['Date'].max().isoformat() if pd.notna(data['Date'].max()) else None
        },
        "income_count": len(data[data['Income amount'] > 0]),
        "expense_count": len(data[data['Expense amount'] > 0]),
        "is_normalized": not is_trusted
    }

    return apply_data_normalization(result, is_trusted)

@app.get("/api/categories")
def get_categories(db=Depends(get_db)):
    """Get all unique categories"""
    data = load_data(db)
    categories = data['Category'].dropna().unique().tolist()
    return {"categories": sorted(categories)}

@app.get("/api/tags")
def get_tags(db=Depends(get_db)):
    """Get all unique tags"""
    data = load_data(db)
    all_tags = set()
    for tags in data['Tags'].dropna():
        for tag in str(tags).split(','):
            tag = tag.strip()
            if tag:
                all_tags.add(tag)
    return {"tags": sorted(list(all_tags))}

@app.post("/api/insights")
@limiter.limit("10/minute")  # Max 10 AI requests per minute
async def get_ai_insights(request: Request, insight_request: AIInsightRequest, is_trusted: bool = Depends(verify_token), db=Depends(get_db)):
    """Get AI-powered financial insights using Claude - Only for authenticated users"""
    data = load_data(db)
    if not is_trusted:
        raise HTTPException(
            status_code=403,
            detail="AI insights are only available for authenticated users. Please log in to access this feature."
        )

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")

    # Always use real data for AI analysis
    summary_data = get_summary(is_trusted=True)

    context = f"""
You are a financial advisor analyzing expense data. Here's the summary:

Total Expenses: {summary_data['total_expenses']:.2f} {summary_data['currency']}
Total Income: {summary_data['total_income']:.2f} {summary_data['currency']}
Net Balance: {summary_data['net']:.2f} {summary_data['currency']}
Date Range: {summary_data['date_range']['start']} to {summary_data['date_range']['end']}

Top Spending Categories:
"""
    for cat, amount in list(summary_data['category_breakdown'].items())[:10]:
        context += f"- {cat}: {amount:.2f} {summary_data['currency']}\n"

    context += f"\nIncome by Category:\n"
    for cat, amount in list(summary_data['income_breakdown'].items())[:5]:
        context += f"- {cat}: {amount:.2f} {summary_data['currency']}\n"

    context += f"\nTop Expense Tags:\n"
    for tag, amount in list(summary_data['top_tags'].items())[:10]:
        context += f"- {tag}: {amount:.2f} {summary_data['currency']}\n"

    user_query = insight_request.query or "Analyze my spending and income patterns and provide advice on how to optimize my finances."

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"{context}\n\nQuestion: {user_query}\n\nProvide specific, actionable financial advice based on this data."
                }
            ]
        )

        return {
            "insights": message.content[0].text,
            "query": user_query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.get("/api/search")
def search_expenses(q: str, limit: int = 50, is_trusted: bool = Depends(verify_token), db=Depends(get_db)):
    """Search expenses by keyword"""
    data = load_data(db)
    search_term = q.lower()

    mask = (
        data['Category'].astype(str).str.lower().str.contains(search_term, na=False) |
        data['Tags'].astype(str).str.lower().str.contains(search_term, na=False) |
        data['Description'].astype(str).str.lower().str.contains(search_term, na=False)
    )

    results = data[mask].head(limit)
    # Use EUR-converted amounts for totals
    matched_df = data[mask]
    total_amount = matched_df[matched_df['Expense amount'] > 0]['In main currency'].sum()
    total_income = matched_df[matched_df['Income amount'] > 0]['In main currency'].sum()
    count = len(matched_df)

    records = results.to_dict('records')
    for record in records:
        if pd.isna(record['Date']):
            record['Date'] = None
        else:
            record['Date'] = record['Date'].isoformat()

        for key in record:
            if pd.isna(record[key]):
                record[key] = None

    records = normalize_expenses_list(records, is_trusted)

    if not is_trusted:
        total_amount = normalize_amount(total_amount, NORMALIZATION_FACTOR)
        total_income = normalize_amount(total_income, NORMALIZATION_FACTOR)

    return {
        "query": q,
        "total_amount": float(total_amount),
        "total_income": float(total_income),
        "count": count,
        "results": records,
        "is_normalized": not is_trusted
    }

@app.post("/api/admin/reset-database")
async def reset_database(is_trusted: bool = Depends(verify_token)):
    """Drop and recreate all database tables - USE WITH CAUTION"""
    if not is_trusted:
        raise HTTPException(status_code=403, detail="Authentication required")

    if not USE_DATABASE:
        raise HTTPException(status_code=400, detail="Not using PostgreSQL database")

    try:
        from backend.database import Base, engine
    except ImportError:
        from database import Base, engine

    if engine is None:
        raise HTTPException(status_code=500, detail="Database engine not initialized")

    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    Base.metadata.create_all(bind=engine)

    return {"status": "success", "message": "Database tables reset successfully"}

@app.post("/api/admin/migrate-csv")
async def migrate_csv_data(file: UploadFile = File(...), is_trusted: bool = Depends(verify_token)):
    """
    One-time migration endpoint to upload CSV and import into PostgreSQL
    Only accessible with trusted token
    """
    if not is_trusted:
        raise HTTPException(status_code=403, detail="Authentication required")

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    if not USE_DATABASE:
        raise HTTPException(status_code=400, detail="DATABASE_URL not configured - cannot migrate to PostgreSQL")

    try:
        # Read CSV content
        content = await file.read()

        # Save temporarily
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Parse CSV
        df_migration = pd.read_csv(tmp_path)

        # Clean data
        df_migration['Date'] = pd.to_datetime(df_migration['Date'], format='%m/%d/%y', errors='coerce')
        df_migration['Expense amount'] = df_migration['Expense amount'].replace(',', '', regex=True).astype(float)
        df_migration['Income amount'] = df_migration['Income amount'].replace(',', '', regex=True).astype(float)
        if 'In main currency' in df_migration.columns:
            df_migration['In main currency'] = df_migration['In main currency'].replace(',', '', regex=True).astype(float)

        # Fill NaN
        df_migration = df_migration.fillna({
            'Account': '',
            'Category': '',
            'Tags': '',
            'Expense amount': 0.0,
            'Income amount': 0.0,
            'Currency': 'EUR',
            'Main currency': 'EUR',
            'In main currency': 0.0,
            'Description': ''
        })

        # Import to database
        try:
            from backend.database import SessionLocal, Transaction, ensure_tables_exist
        except ImportError:
            from database import SessionLocal, Transaction, ensure_tables_exist

        # Ensure tables exist before migration
        ensure_tables_exist()

        db_session = SessionLocal()

        try:
            # Check existing
            existing = db_session.query(Transaction).count()
            if existing > 0:
                db_session.close()
                os.unlink(tmp_path)
                return {
                    "status": "error",
                    "message": f"Database already contains {existing} transactions. Clear manually if needed."
                }

            # Bulk insert
            inserted = 0
            batch_size = 1000

            for i in range(0, len(df_migration), batch_size):
                batch = df_migration.iloc[i:i+batch_size]
                transactions = []

                for _, row in batch.iterrows():
                    transaction = Transaction(
                        date=row['Date'],
                        account=str(row['Account']),
                        category=str(row['Category']),
                        tags=str(row['Tags']),
                        expense_amount=float(row['Expense amount']),
                        income_amount=float(row['Income amount']),
                        currency=str(row['Currency']),
                        main_currency=str(row['Main currency']),
                        in_main_currency=float(row.get('In main currency', 0.0)),
                        description=str(row.get('Description', ''))
                    )
                    transactions.append(transaction)

                db_session.bulk_save_objects(transactions)
                db_session.commit()
                inserted += len(transactions)

            final_count = db_session.query(Transaction).count()

            # Clean up temp file
            os.unlink(tmp_path)

            return {
                "status": "success",
                "message": f"Successfully imported {inserted} transactions",
                "total_count": final_count
            }

        finally:
            db_session.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")

# Serve frontend static files in production
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend or fall back to index.html for client-side routing"""
        # Don't serve frontend for API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")

        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)

        # Fall back to index.html for client-side routing
        index_path = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)

        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
