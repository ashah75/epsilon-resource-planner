#!/bin/bash

echo "🚀 Starting Resource Planner Backend..."
echo ""
echo "📊 Database: SQLite (resource_planner.db)"
echo "🌐 API will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
echo "🧪 Running backend unit tests..."
python3 -m unittest discover -s backend/tests -v
echo ""
python3 backend.py
