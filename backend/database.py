"""
Database configuration and models for Finance Analysis
"""
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment (Railway provides DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup
engine = None
SessionLocal = None
Base = declarative_base()
_db_initialized = False


class Transaction(Base):
    """Model for financial transactions (both expenses and income)"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    account = Column(String(255))
    category = Column(String(255), index=True)
    tags = Column(Text)  # Comma-separated tags
    expense_amount = Column(Float, default=0.0)
    income_amount = Column(Float, default=0.0)
    currency = Column(String(10))
    main_currency = Column(String(10))
    in_main_currency = Column(Float, default=0.0)  # Amount converted to main currency
    description = Column(Text)

    def to_dict(self):
        """Convert to dictionary matching the CSV format"""
        return {
            "Date": self.date,
            "Account": self.account,
            "Category": self.category,
            "Tags": self.tags,
            "Expense amount": self.expense_amount,
            "Income amount": self.income_amount,
            "Currency": self.currency,
            "Main currency": self.main_currency,
            "In main currency": self.in_main_currency,
            "Description": self.description,
        }


def init_db():
    """
    Initialize database connection (lazy - only creates engine, doesn't connect yet)
    Tables are created on first database access
    """
    global engine, SessionLocal, _db_initialized

    if not DATABASE_URL:
        # For local development without PostgreSQL, skip database initialization
        return None

    if _db_initialized:
        return engine

    # Create engine (lazy connection - doesn't actually connect until first query)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    _db_initialized = True
    return engine


def ensure_tables_exist():
    """Create tables if they don't exist (called on first database access)"""
    global engine
    if engine is not None:
        Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI endpoints"""
    if SessionLocal is None:
        yield None
        return

    # Ensure tables exist on first database access
    ensure_tables_exist()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
