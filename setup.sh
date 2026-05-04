#!/bin/bash

# Conflict Tracker Setup Script
# This script sets up both backend and frontend for the project

echo "🌍 Setting up Conflict Tracker..."
echo ""

# Backend Setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend Setup
echo "📦 Setting up Frontend..."
cd ../frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi

echo "✅ Frontend setup complete!"
echo ""

echo "🚀 Setup complete! To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "The application will open at http://localhost:3000"
