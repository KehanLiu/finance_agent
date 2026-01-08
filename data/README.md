# Data Directory

This directory contains your financial CSV data files.

## Security Notice

**CSV files are NOT committed to git** - they are listed in `.gitignore` for security.

## How to Upload Data to Railway

After deployment, upload your CSV files using Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Upload CSV files
railway run --service your-service-name bash -c "mkdir -p /app/data"
railway up data/expenses_2021.csv
railway up data/expenses_2022.csv
railway up data/income_2021.csv
railway up data/income_2022.csv
```

## Required CSV Files

- `expenses_2021.csv`
- `expenses_2022.csv`
- `income_2021.csv`
- `income_2022.csv`

See [documentation/DEPLOYMENT.md](../documentation/DEPLOYMENT.md) for detailed instructions.
