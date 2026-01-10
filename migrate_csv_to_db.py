#!/usr/bin/env python3
"""
Migration script to load CSV data into PostgreSQL database

Usage:
    # Railway: railway run python migrate_csv_to_db.py
    # Local: python migrate_csv_to_db.py path/to/file.csv
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.database import init_db, SessionLocal, Transaction
from dotenv import load_dotenv

load_dotenv()


def migrate_csv_to_database(csv_file_path: str):
    """Migrate CSV data to PostgreSQL database"""

    print(f"📊 Starting migration from CSV to PostgreSQL...")
    print(f"   CSV File: {csv_file_path}")

    # Check file exists
    if not os.path.exists(csv_file_path):
        print(f"❌ Error: CSV file not found: {csv_file_path}")
        sys.exit(1)

    # Initialize database
    print("🔌 Connecting to database...")
    if not os.getenv("DATABASE_URL"):
        print("❌ Error: DATABASE_URL environment variable not set")
        sys.exit(1)

    engine = init_db()
    print(f"✅ Connected to database")

    # Load CSV
    print(f"📖 Reading CSV file...")
    df = pd.read_csv(csv_file_path)
    print(f"   Found {len(df)} transactions")

    # Data cleaning
    print("🧹 Cleaning data...")
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
    df['Expense amount'] = df['Expense amount'].replace(',', '', regex=True).astype(float)
    df['Income amount'] = df['Income amount'].replace(',', '', regex=True).astype(float)

    # Fill NaN values
    df = df.fillna({
        'Account': '',
        'Category': '',
        'Tags': '',
        'Expense amount': 0.0,
        'Income amount': 0.0,
        'Currency': 'EUR',
        'Main currency': 'EUR',
        'Description': ''
    })

    # Create database session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Transaction).count()
        if existing_count > 0:
            print(f"⚠️  Warning: Database already contains {existing_count} transactions")
            response = input("   Do you want to clear existing data and reimport? (yes/no): ")
            if response.lower() == 'yes':
                print("🗑️  Deleting existing transactions...")
                db.query(Transaction).delete()
                db.commit()
                print(f"   Deleted {existing_count} transactions")
            else:
                print("❌ Migration cancelled")
                return

        # Insert transactions
        print(f"💾 Importing {len(df)} transactions...")
        inserted = 0
        batch_size = 1000

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
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
                    description=str(row.get('Description', ''))
                )
                transactions.append(transaction)

            db.bulk_save_objects(transactions)
            db.commit()
            inserted += len(transactions)
            print(f"   Progress: {inserted}/{len(df)} transactions imported")

        print(f"✅ Successfully imported {inserted} transactions!")

        # Verify
        final_count = db.query(Transaction).count()
        print(f"✅ Database now contains {final_count} transactions")

    except Exception as e:
        print(f"❌ Error during migration: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Determine CSV file path
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        # Try to find CSV in data directory
        data_dir = Path(__file__).parent / "data"
        csv_files = list(data_dir.glob("*.csv"))

        if not csv_files:
            print("❌ Error: No CSV files found in data/ directory")
            print("   Usage: python migrate_csv_to_db.py path/to/file.csv")
            sys.exit(1)

        csv_path = str(csv_files[0])
        print(f"📁 Auto-detected CSV file: {csv_path}")

    migrate_csv_to_database(csv_path)
