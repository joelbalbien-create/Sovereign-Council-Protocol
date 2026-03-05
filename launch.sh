#!/bin/bash
echo "Starting Sovereign Council..."

# Auto-detect current IP address
CURRENT_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "127.0.0.1")
echo "Detected IP: $CURRENT_IP"

# Update backend IP in frontend config
sed -i '' "s|http://[0-9.]*:8002|http://$CURRENT_IP:8002|g" ~/sovereign-council/frontend/src/SovereignOracle.jsx

# Update EVAL suite IP
sed -i '' "s|http://[0-9.]*:8002|http://$CURRENT_IP:8002|g" ~/sovereign-council/eval/run_evals.py

# Kill any existing processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
sleep 2

# Start backend with detected IP
cd ~/sovereign-council/backend
export PATH="/Users/joelbalbien/Library/Python/3.9/bin:$PATH"
python3 -m uvicorn main:app --host $CURRENT_IP --port 8002 &
echo "Backend starting on $CURRENT_IP:8002..."

# Wait for backend
sleep 4

# Start frontend
cd ~/sovereign-council/frontend
npm start &
echo "Frontend starting..."

echo "Sovereign Council launching at http://localhost:3000"
echo "iPad access at http://$CURRENT_IP:3000"
sleep 6
open -a Safari http://localhost:3000
