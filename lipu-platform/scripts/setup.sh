#!/bin/bash

# Development setup script for LIPU Platform

set -e

echo "🚀 LIPU Platform - Development Setup"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 20+."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+."
    exit 1
fi

echo "✅ All prerequisites installed"
echo ""

# Clone/setup repository
echo "📦 Setting up repository..."

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.example .env.local
    echo "⚠️  Please edit .env.local with your credentials"
fi

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Setup backend
echo "🔧 Setting up backend..."
cd apps/api

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt > /dev/null 2>&1
pip install -r requirements-dev.txt > /dev/null 2>&1

cd ../..

# Setup frontend
echo "⚙️  Setting up frontend..."
cd apps/web
npm install > /dev/null 2>&1
cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Edit .env.local with your credentials"
echo "  2. Terminal 1: npm run api:dev"
echo "  3. Terminal 2: npm run web:dev"
echo "  4. Frontend: http://localhost:3000"
echo "  5. API Docs: http://localhost:8000/docs"
echo ""
echo "📚 For more info, see docs/guides/development-setup.md"
