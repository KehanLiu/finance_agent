"""
Temporary migration endpoint for initial data import
Add this to main.py for one-time use
"""

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
        import tempfile
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Parse CSV
        df = pd.read_csv(tmp_path)

        # Clean data
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
        df['Expense amount'] = df['Expense amount'].replace(',', '', regex=True).astype(float)
        df['Income amount'] = df['Income amount'].replace(',', '', regex=True).astype(float)

        # Fill NaN
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

        # Import to database
        from backend.database import SessionLocal, Transaction
        db = SessionLocal()

        try:
            # Check existing
            existing = db.query(Transaction).count()
            if existing > 0:
                return {
                    "status": "error",
                    "message": f"Database already contains {existing} transactions. Clear manually if needed."
                }

            # Bulk insert
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

            final_count = db.query(Transaction).count()

            # Clean up temp file
            os.unlink(tmp_path)

            return {
                "status": "success",
                "message": f"Successfully imported {inserted} transactions",
                "total_count": final_count
            }

        finally:
            db.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Migration failed: {str(e)}")
