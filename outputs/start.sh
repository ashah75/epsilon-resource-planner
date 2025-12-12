#!/bin/bash

# Resource Planner - React Setup and Run Script
# This script sets up both backend and frontend and runs them

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Epsilon Resource Planner - React Setup & Launch      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "${BLUE}🔍 Checking prerequisites...${NC}"
echo ""

if ! command_exists python3; then
    echo "${YELLOW}❌ Python 3 is not installed. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

if ! command_exists node; then
    echo "${YELLOW}❌ Node.js is not installed. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo "${YELLOW}❌ npm is not installed. Please install npm.${NC}"
    exit 1
fi

echo "${GREEN}✅ Python 3: $(python3 --version)${NC}"
echo "${GREEN}✅ Node.js: $(node --version)${NC}"
echo "${GREEN}✅ npm: $(npm --version)${NC}"
echo ""

# Setup backend
echo "${BLUE}📦 Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install flask flask-cors --break-system-packages 2>/dev/null || pip install flask flask-cors

echo "${GREEN}✅ Backend setup complete!${NC}"
echo ""

# Setup frontend
echo "${BLUE}📦 Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Dependencies already installed."
fi

echo "${GREEN}✅ Frontend setup complete!${NC}"
echo ""

# Start services
echo "${BLUE}🚀 Starting services...${NC}"
echo ""

# Start backend in background
cd ../backend
echo "${GREEN}Starting backend server on http://localhost:5000${NC}"
python3 backend.py &
BACKEND_PID=$!

# Give backend time to start
sleep 2

# Start frontend
cd ../frontend
echo "${GREEN}Starting frontend server on http://localhost:3000${NC}"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                     🎉 Ready to Go!                      ║"
echo "║                                                           ║"
echo "║  Backend:  http://localhost:5000                         ║"
echo "║  Frontend: http://localhost:3000                         ║"
echo "║                                                           ║"
echo "║  Press Ctrl+C to stop both servers                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

npm run dev

# Cleanup on exit
cleanup() {
    echo ""
    echo "${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM
