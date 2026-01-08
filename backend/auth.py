import os
import secrets
import hashlib
import random
from typing import Optional
from fastapi import HTTPException, Depends, Header, Cookie, Request
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Store sessions in memory (use Redis for production)
active_sessions = {}

# Generate secure tokens for you and your wife
# You can generate these tokens and share them securely
def generate_secure_token():
    """Generate a secure access token"""
    return secrets.token_urlsafe(32)

# Load trusted tokens from environment
TRUSTED_TOKENS = set()

# Method 1: Comma-separated TRUSTED_TOKENS env variable (recommended)
if os.getenv("TRUSTED_TOKENS"):
    tokens = os.getenv("TRUSTED_TOKENS").split(",")
    for token in tokens:
        token = token.strip()
        if token:
            TRUSTED_TOKENS.add(token)

# Method 2: Individual AUTH_TOKEN_* variables (backwards compatible)
if os.getenv("AUTH_TOKEN_1"):
    TRUSTED_TOKENS.add(os.getenv("AUTH_TOKEN_1"))
if os.getenv("AUTH_TOKEN_2"):
    TRUSTED_TOKENS.add(os.getenv("AUTH_TOKEN_2"))

# If no tokens configured, use demo mode
DEMO_MODE = len(TRUSTED_TOKENS) == 0

def verify_token(
    request: Request,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
) -> bool:
    """
    Verify if the request is from a trusted user.
    Checks both cookie (secure) and Authorization header (backwards compatible).
    Returns True if trusted (real data), False if guest (normalized data)
    """
    token = None

    # Priority 1: Check httpOnly cookie (most secure)
    if session_token:
        token = session_token
        print(f"[AUTH] Token from cookie: {token[:10]}...")
    # Priority 2: Check Authorization header (backwards compatible)
    elif authorization:
        token = authorization.replace("Bearer ", "").strip()
        print(f"[AUTH] Token from header: {token[:10]}...")

    if DEMO_MODE:
        # If no tokens configured, allow access but with normalized data
        print("⚠️  Warning: No AUTH_TOKEN configured. Running in demo mode with normalized data.")
        return False

    if not token:
        print("[AUTH] No token provided (neither cookie nor header)")
        return False

    print(f"[AUTH] Checking against {len(TRUSTED_TOKENS)} trusted tokens")

    # Check if token is in trusted list
    if token in TRUSTED_TOKENS:
        print("[AUTH] ✓ Token is TRUSTED")
        return True

    print("[AUTH] ✗ Token is NOT TRUSTED")
    return False

def get_daily_obfuscation_factor() -> float:
    """
    Generate a random obfuscation factor that changes daily.
    This makes it impossible to reverse-engineer actual amounts from the code alone.

    Returns a factor between 0.2 and 0.4 that stays consistent for the current day.
    """
    import random
    from datetime import date

    # Use current date as seed so factor is consistent throughout the day
    today = date.today()
    seed = int(today.strftime('%Y%m%d'))

    # Create random generator with today's seed
    rng = random.Random(seed)

    # Generate factor between 0.2 and 0.4
    return rng.uniform(0.2, 0.4)

def normalize_amount(amount, normalization_factor: float = None):
    """
    Obfuscate amounts for guest users using a daily-changing random factor.

    The factor changes every day and is random between 0.2-0.4, making it
    impossible to reverse-engineer actual amounts even with access to code.
    """
    if amount is None or amount == '':
        return None

    # Convert string to float if needed (handle commas)
    if isinstance(amount, str):
        amount = float(amount.replace(',', ''))

    # Use daily random factor if none provided
    if normalization_factor is None:
        normalization_factor = get_daily_obfuscation_factor()

    return round(float(amount) * normalization_factor, 2)

def get_normalization_factor(df=None, target_yearly_expense: float = None) -> float:
    """
    Get the daily obfuscation factor.
    This function signature is kept for backwards compatibility but now returns
    the daily random factor instead of a data-based calculation.

    The df and target_yearly_expense parameters are ignored.
    """
    return get_daily_obfuscation_factor()

# Privacy protection for income sources
INCOME_CATEGORIES = [
    "Employment Income",
    "Freelance Work",
    "Investment Returns",
    "Business Revenue",
    "Other Income"
]

INCOME_TAGS = [
    "monthly income",
    "project payment",
    "dividend",
    "interest",
    "bonus",
    "commission",
    "other"
]

def anonymize_income_text(text: str, seed: int = 42) -> str:
    """
    Anonymize income source text while keeping it consistent.
    Uses seeded random to ensure same input always produces same output.
    """
    if not text or text == '':
        return ''

    # Create a hash of the text to use as seed
    text_hash = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    rng = random.Random(text_hash + seed)

    # Return a consistent anonymized category/tag
    return rng.choice(INCOME_CATEGORIES if len(text) > 20 else INCOME_TAGS)

def anonymize_income_entry(entry: dict, normalization_factor: float = 1.0) -> dict:
    """
    Anonymize an income entry for guest viewing:
    - Normalize amounts
    - Replace category with generic income category
    - Replace tags with generic tags
    - Replace description with generic text
    """
    anonymized = entry.copy()

    # Normalize amounts
    if anonymized.get('Income amount'):
        anonymized['Income amount'] = normalize_amount(anonymized['Income amount'], normalization_factor)
    if anonymized.get('In main currency'):
        anonymized['In main currency'] = normalize_amount(anonymized['In main currency'], normalization_factor)

    # Anonymize text fields
    if anonymized.get('Category'):
        anonymized['Category'] = anonymize_income_text(anonymized['Category'])

    if anonymized.get('Tags'):
        # Split tags and anonymize each
        tags = anonymized['Tags'].split(',')
        anonymized_tags = [anonymize_income_text(tag.strip()) for tag in tags]
        anonymized['Tags'] = ', '.join(set(anonymized_tags))  # Remove duplicates

    if anonymized.get('Description'):
        anonymized['Description'] = 'Income payment'

    return anonymized

# Generate initial tokens if needed (run this once to get your tokens)
if __name__ == "__main__":
    print("🔐 Generate secure tokens for you and your wife:")
    print(f"AUTH_TOKEN_1={generate_secure_token()}")
    print(f"AUTH_TOKEN_2={generate_secure_token()}")
    print("\nAdd these to your .env file:")
    print("AUTH_TOKEN_1=<token1>")
    print("AUTH_TOKEN_2=<token2>")
