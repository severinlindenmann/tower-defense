#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏰 Tower Defense Game - Quick Start${NC}\n"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed${NC}"
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites checked${NC}\n"

# Backend setup
echo -e "${BLUE}Setting up backend...${NC}"
cd backend
if [ ! -d ".venv" ]; then
    echo "Installing backend dependencies..."
    uv sync
    uv pip install fastapi "uvicorn[standard]" websockets pydantic
fi
echo -e "${GREEN}✓ Backend ready${NC}\n"

# Frontend setup
echo -e "${BLUE}Setting up frontend...${NC}"
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
echo -e "${GREEN}✓ Frontend ready${NC}\n"

cd ..

echo -e "${GREEN}🎮 Setup complete!${NC}\n"
echo "To start the game:"
echo "  1. Backend:  cd backend && uv run uvicorn main:app --reload"
echo "  2. Frontend: cd frontend && npm run dev"
echo ""
echo "Or run them in separate terminals:"
echo "  Terminal 1: ./start-backend.sh"
echo "  Terminal 2: ./start-frontend.sh"
