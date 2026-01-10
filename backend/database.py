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
            "Description": self.description,
        }


def init_db():
    """Initialize database connection"""
    global engine, SessionLocal

    if not DATABASE_URL:
        # For local development without PostgreSQL, skip database initialization
        return None

    # Create engine
    engine = create_engine(DATABASE_URL)

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    return engine


def get_db():
    """Dependency for FastAPI endpoints"""
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
