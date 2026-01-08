#!/bin/bash

# Post-create setup script for devcontainer
set -e

echo "🚀 Setting up Finance Dashboard development environment..."

# Navigate to workspace
cd /workspace

# Install Python backend dependencies using UV
echo "📦 Installing Python backend dependencies with UV..."
cd backend
uv pip install -e . --system
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies with npm..."
cd frontend
npm install
cd ..

# Create .env files from examples if they don't exist
echo "⚙️  Setting up environment files..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env from example"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✓ Created frontend/.env from example"
fi

# Set up git hooks or other post-install tasks if needed
echo "✅ Development environment setup complete!"
echo ""
echo "📝 Quick start:"
echo "  Backend:  cd backend && python -m uvicorn main:app --reload --host 0.0.0.0"
echo "  Frontend: cd frontend && npm run dev"
echo "  Or run production build: docker compose -f docker-compose.dev.yml up"
echo ""
echo "🌐 Access the app at: http://localhost:8000"
