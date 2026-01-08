#!/bin/bash

echo "🚀 Finance Analysis Dashboard - Setup Script"
echo "=============================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Generate auth tokens
echo "🔐 Generating authentication tokens..."
cd backend
python auth.py > tokens.txt
echo ""
echo "✅ Tokens generated and saved to backend/tokens.txt"
echo "⚠️  Please save these tokens securely and delete tokens.txt after copying!"
echo ""

# Create .env file
echo "📝 Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit backend/.env and add:"
    echo "   - Your ANTHROPIC_API_KEY"
    echo "   - The tokens from tokens.txt"
else
    echo "⚠️  .env file already exists, skipping..."
fi

echo ""
echo "📦 Installing backend dependencies with uv..."
uv pip install -e .

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API key and tokens"
echo "2. Start backend: cd backend && uv run python main.py"
echo "3. In another terminal, start frontend:"
echo "   cd frontend && npm install && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "🔐 Login with your generated tokens to see real data!"
