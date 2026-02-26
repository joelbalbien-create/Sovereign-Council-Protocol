#!/bin/bash
echo "Starting Sovereign Council..."

# Kill any existing processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
sleep 2

# Start backend
cd ~/sovereign-council/backend
export PATH="/Users/joelbalbien/Library/Python/3.9/bin:$PATH"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8002 &
echo "Backend starting..."

# Wait for backend
sleep 4

# Start frontend
cd ~/sovereign-council/frontend
npm start &
echo "Frontend starting..."

echo "Sovereign Council launching at localhost:3000"
sleep 6
open -a Safari http://localhost:3000
