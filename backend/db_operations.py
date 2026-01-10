"""
Database operations for querying financial data
"""
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import Optional, Dict, List

try:
    from backend.database import Transaction
except ImportError:
    from database import Transaction


def get_all_transactions_as_dataframe(db: Session) -> pd.DataFrame:
    """
    Fetch all transactions from database and convert to pandas DataFrame
    matching the original CSV format
    """
    transactions = db.query(Transaction).all()

    if not transactions:
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=[
            "Date", "Account", "Category", "Tags", "Expense amount",
            "Income amount", "Currency", "Main currency", "Description"
        ])

    # Convert to list of dictionaries
    data = [t.to_dict() for t in transactions]

    # Create DataFrame
    df = pd.DataFrame(data)

    # Ensure date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    return df


def get_transactions_by_date_range(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Transaction]:
    """Get transactions within a date range"""
    query = db.query(Transaction)

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    return query.order_by(Transaction.date.desc()).all()


def get_expenses(db: Session, category: Optional[str] = None) -> List[Transaction]:
    """Get all expense transactions, optionally filtered by category"""
    query = db.query(Transaction).filter(Transaction.expense_amount > 0)

    if category:
        query = query.filter(Transaction.category == category)

    return query.order_by(Transaction.date.desc()).all()


def get_income(db: Session, category: Optional[str] = None) -> List[Transaction]:
    """Get all income transactions, optionally filtered by category"""
    query = db.query(Transaction).filter(Transaction.income_amount > 0)

    if category:
        query = query.filter(Transaction.category == category)

    return query.order_by(Transaction.date.desc()).all()


def get_categories(db: Session) -> List[str]:
    """Get all unique categories"""
    categories = db.query(Transaction.category).distinct().filter(
        Transaction.category.isnot(None)
    ).all()
    return sorted([c[0] for c in categories if c[0]])


def get_all_tags(db: Session) -> List[str]:
    """Get all unique tags"""
    transactions = db.query(Transaction.tags).filter(
        Transaction.tags.isnot(None)
    ).all()

    all_tags = set()
    for (tags_str,) in transactions:
        if tags_str:
            for tag in tags_str.split(','):
                tag = tag.strip()
                if tag:
                    all_tags.add(tag)

    return sorted(list(all_tags))


def search_transactions(
    db: Session,
    query_text: str,
    category: Optional[str] = None
) -> List[Transaction]:
    """Search transactions by description or tags"""
    search_query = db.query(Transaction).filter(
        (Transaction.description.ilike(f"%{query_text}%")) |
        (Transaction.tags.ilike(f"%{query_text}%"))
    )

    if category:
        search_query = search_query.filter(Transaction.category == category)

    return search_query.order_by(Transaction.date.desc()).all()


def get_transaction_count(db: Session) -> int:
    """Get total number of transactions"""
    return db.query(Transaction).count()


def get_summary_stats(db: Session) -> Dict:
    """Get summary statistics"""
    total_expenses = db.query(func.sum(Transaction.expense_amount)).scalar() or 0
    total_income = db.query(func.sum(Transaction.income_amount)).scalar() or 0
    expense_count = db.query(Transaction).filter(Transaction.expense_amount > 0).count()
    income_count = db.query(Transaction).filter(Transaction.income_amount > 0).count()

    return {
        "total_expenses": float(total_expenses),
        "total_income": float(total_income),
        "net": float(total_income - total_expenses),
        "expense_count": expense_count,
        "income_count": income_count,
    }
