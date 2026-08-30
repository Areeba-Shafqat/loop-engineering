#!/bin/bash
# Start WatchLoop Backend Server
echo "================================================"
echo "  WatchLoop Backend Server"
echo "================================================"
echo ""
echo "Starting backend on http://localhost:5000"
echo "Check interval: 60 seconds (production default)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

cd backend
python run_production.py
