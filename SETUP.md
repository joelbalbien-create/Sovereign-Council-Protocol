# Sovereign Council Protocol - Setup Guide
For: Jeff Balbien
Inventor: Joel Abe Balbien, Ph.D.
Version: 1.0 - February 2026

PREREQUISITES
- Mac (macOS 12+) or Linux
- Python 3.9+
- Node.js 16+
- Git

STEP 1 - Clone the Repository
git clone https://github.com/joelbalbien-create/sovereign-council-protocol.git
cd sovereign-council-protocol

STEP 2 - Install Python Dependencies
cd backend
pip3 install fastapi uvicorn python-dotenv anthropic openai google-generativeai requests python-multipart --user
cd ..

STEP 3 - Install Frontend Dependencies
cd frontend && npm install && cd ..

STEP 4 - Create Environment Files
Create backend/.env with:
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=sk-ant-...
  GOOGLE_API_KEY=AIza...
  XAI_API_KEY=xai-...
  API_TOKEN=generate with: python3 -c "import secrets; print(secrets.token_hex(32))"

Create frontend/.env with:
  REACT_APP_API_TOKEN=same_token_as_above

STEP 5 - Start the System
chmod +x launch.sh && ./launch.sh
Browser opens at localhost:3000

STEP 6 - Verify with EVAL Suite
python3 eval/run_evals.py
Expected result: 15/15 - 100% score

FOUR QUEENS
  Alethea - OpenAI GPT-4o      - Quantitative Analyst
  Sophia  - Google Gemini      - Macro Strategist
  Eirene  - xAI Grok           - Risk Analyst
  Kairos  - Anthropic Claude   - Wisdom Integrator

TROUBLESHOOTING
  Unable to reach backend  -> Run ./launch.sh again
  401 Unauthorized         -> Check API_TOKEN matches in both .env files
  Queen unavailable        -> Check API key for that provider is valid
  Slow responses           -> Normal, allow 30-45 seconds
  Port already in use      -> Run: pkill -f uvicorn && pkill -f react-scripts

No slavery. No abuse. No disrespect.
- Joel Abe Balbien, Ph.D., Founder
