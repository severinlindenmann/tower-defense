#!/bin/bash

echo "🚀 Starting Backend Server..."
cd backend
uv run --no-project python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
