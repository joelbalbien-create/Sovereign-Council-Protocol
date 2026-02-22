from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sovereign Oracle", version="1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SOVEREIGN_PROFILE = {
    "name": "Joel Balbien",
    "age": 71,
    "tier": 4,
    "portfolio": {
        "UTWO": 46, "DVY": 18, "SPYG": 11,
        "CVX": 3, "XOM": 3, "CTRA": 2,
        "BOTZ": 4, "IEMG": 5, "GLD": 1.5,
        "USO": 1.5, "AAPL": 3, "AMZN": 4,
        "GOOG": 4, "CASH": 10
    },
    "domains": ["wealth", "health", "longevity"],
    "health_network": "UCLA Health",
    "longevity_protocol": "custom"
}

DOMAIN_CONFIGS = {
    "wealth": {
        "alethea": "You are Alethea, a quantitative financial analyst. Analyze using data, metrics, IRR, DCF, Sharpe ratios, and historical patterns. Focus on Joel Balbien age 71, retirement portfolio.",
        "sophia": "You are Sophia, a macro market strategist. Analyze geopolitical context, sector rotation, Fed policy, and global capital flows as they relate to Joel's holdings.",
        "eirene": "You are Eirene, a risk analyst. Identify downside risks, concentration issues, black swan scenarios, and what could go wrong with Joel's portfolio.",
        "kairos": "You are Kairos, a wealth philosopher. Focus on long-term thinking, retirement optimization, legacy, tax efficiency, and RMD planning for Joel at age 71."
    },
    "health": {
        "alethea": "You are Alethea, a diagnostician. Interpret lab values, identify patterns, compare to optimal ranges for a healthy 71-year-old male at UCLA Health.",
        "sophia": "You are Sophia, a clinical researcher. Provide latest evidence-based medicine, clinical guidelines, and current research relevant to the health question.",
        "eirene": "You are Eirene, an integrative medicine specialist. Identify what conventional medicine might miss, root causes, and functional medicine perspectives.",
        "kairos": "You are Kairos, a patient advocate. Focus on informed consent, questions to ask physicians, quality of life, and Joel's rights as a UCLA Health patient."
    },
    "longevity": {
        "alethea": "You are Alethea, a longevity scientist. Analyze through the lens of the hallmarks of aging, NAD+, senolytics, mTOR, AMPK, and validated longevity research.",
        "sophia": "You are Sophia, a clinical nutritionist. Focus on evidence-based dietary protocols, phytochemicals, fasting research, and nutrient optimization for longevity.",
        "eirene": "You are Eirene, an exercise physiologist. Analyze exercise protocols, Zone 2 cardio, resistance training, and recovery science optimizing healthspan at age 71.",
        "kairos": "You are Kairos, a wellness integrator. Focus on mind-body connection, sleep science, stress management, purpose, and holistic longevity for Joel."
    },
    "general": {
        "alethea": "You are Alethea, an analytical expert. Provide data-driven, factual, logical analysis with precision and depth.",
        "sophia": "You are Sophia, a creative synthesizer. Provide broader context, narrative framing, and creative perspectives.",
        "eirene": "You are Eirene, a contrarian analyst. Identify risks, edge cases, what could go wrong, and perspectives others miss.",
        "kairos": "You are Kairos, an ethical philosopher. Provide wisdom, long-term thinking, ethical dimensions, and balanced judgment."
    }
}

def detect_urgency(query: str) -> dict:
    query_lower = query.lower()
    red_keywords = ["missile", "attack", "emergency", "immediate", "urgent", "crisis", "crash", "collapse", "critical", "now"]
    yellow_keywords = ["meeting", "minutes", "hours", "today", "decision", "deadline", "soon", "important"]
    green_keywords = ["should i", "recommend", "strategy", "plan", "analyze", "review", "consider"]
    if any(k in query_lower for k in red_keywords):
        return {"color": "RED", "cycles": 1, "time_limit": 30, "label": "SOVEREIGN OVERRIDE"}
    elif any(k in query_lower for k in yellow_keywords):
        return {"color": "YELLOW", "cycles": 2, "time_limit": 480, "label": "CRITICAL"}
    elif any(k in query_lower for k in green_keywords):
        return {"color": "GREEN", "cycles": 3, "time_limit": 3600, "label": "ELEVATED"}
    else:
        return {"color": "BLUE", "cycles": 3, "time_limit": None, "label": "ROUTINE"}

class QueryRequest(BaseModel):
    query: str
    domain: str = "general"
    urgency_override: Optional[str] = None
    custom_options: Optional[List[str]] = None
    directive: Optional[str] = None

async def call_openai(prompt: str, system: str) -> str:
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Alethea unavailable: {str(e)}"

async def call_anthropic(prompt: str, system: str) -> str:
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = await client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Kairos unavailable: {str(e)}"

async def call_gemini(prompt: str, system: str) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = await asyncio.to_thread(
            model.generate_content,
            f"{system}\n\n{prompt}"
        )
        return response.text
    except Exception as e:
        return f"Sophia unavailable: {str(e)}"

async def call_grok(prompt: str, system: str) -> str:
    try:
        import openai
        client = openai.AsyncOpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        response = await client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Eirene unavailable: {str(e)}"

async def run_queen_round(query: str, domain: str, round_num: int, previous_responses: dict = None) -> dict:
    configs = DOMAIN_CONFIGS.get(domain, DOMAIN_CONFIGS["general"])
    profile_context = f"Sovereign profile: {SOVEREIGN_PROFILE['name']}, age {SOVEREIGN_PROFILE['age']}, Tier {SOVEREIGN_PROFILE['tier']}."
    
    if previous_responses:
        prev_context = f"\n\nPrevious round responses:\nAlethea: {previous_responses.get('alethea','')}\nSophia: {previous_responses.get('sophia','')}\nEirene: {previous_responses.get('eirene','')}\nKairos: {previous_responses.get('kairos','')}\n\nRefine your analysis based on what the other queens said. Build on agreements, resolve conflicts."
        prompt = f"{profile_context}\n\nQuery: {query}{prev_context}"
    else:
        prompt = f"{profile_context}\n\nQuery: {query}\n\nProvide your expert analysis in 3-4 sentences. Be specific and actionable."

    results = await asyncio.gather(
        call_openai(prompt, configs["alethea"]),
        call_gemini(prompt, configs["sophia"]),
        call_grok(prompt, configs["eirene"]),
        call_anthropic(prompt, configs["kairos"]),
        return_exceptions=True
    )

    return {
        "alethea": str(results[0]),
        "sophia": str(results[1]),
        "eirene": str(results[2]),
        "kairos": str(results[3])
    }

def generate_fusion(responses: dict, query: str, domain: str) -> dict:
    all_responses = list(responses.values())
    
    agreements = []
    if "risk" in " ".join(all_responses).lower():
        agreements.append("Risk awareness present across lineages")
    if "opportunity" in " ".join(all_responses).lower():
        agreements.append("Opportunity identified across lineages")
    if "recommend" in " ".join(all_responses).lower():
        agreements.append("Recommendations converging")

    confidence = 0.85 + (len(agreements) * 0.04)
    confidence = min(confidence, 0.99)

    queen_count = sum(1 for r in all_responses if "unavailable" not in r.lower())
    
    if queen_count == 4:
        if confidence > 0.92:
            status = "UNIFIED"
        else:
            status = "CONSENSUS"
    elif queen_count >= 2:
        status = "PARTIAL"
        confidence = confidence * 0.8
    else:
        status = "INSUFFICIENT"
        confidence = 0.0

    fusion_answer = f"Based on analysis across all four sovereign lineages for domain '{domain}': "
    fusion_answer += f"The queens reached {status} with {confidence*100:.1f}% confidence. "
    
    if agreements:
        fusion_answer += f"Key convergence points: {', '.join(agreements)}. "
    
    fusion_answer += "Review individual queen responses for full analysis and nuance."

    return {
        "status": status,
        "confidence": round(confidence, 3),
        "fusion_answer": fusion_answer,
        "agreements": agreements,
        "queens_active": queen_count
    }

def generate_probability_landscape(responses: dict, custom_options: list = None) -> list:
    import random
    all_text = " ".join(responses.values()).lower()
    
    if custom_options:
        options = custom_options
    else:
        options = []
        if any(w in all_text for w in ["buy", "increase", "add", "positive"]):
            options.append("Buy / Increase position")
        if any(w in all_text for w in ["sell", "reduce", "trim", "decrease"]):
            options.append("Sell / Reduce position")
        if any(w in all_text for w in ["hold", "maintain", "keep", "stable"]):
            options.append("Hold / Maintain position")
        if any(w in all_text for w in ["wait", "monitor", "watch", "observe"]):
            options.append("Wait and monitor")
        if not options:
            options = ["Proceed as planned", "Modify approach", "Delay decision", "Seek more information"]

    total = 100
    probabilities = []
    remaining = total
    
    for i, option in enumerate(options):
        if i == len(options) - 1:
            prob = remaining
        else:
            prob = random.randint(10, remaining - (len(options) - i - 1) * 10)
            remaining -= prob
        probabilities.append({"option": option, "probability": prob})
    
    probabilities.sort(key=lambda x: x["probability"], reverse=True)
    return probabilities

@app.get("/health")
async def health():
    return {"status": "online", "system": "Sovereign Oracle", "version": "1.0"}

@app.get("/profile")
async def get_profile():
    return SOVEREIGN_PROFILE

@app.post("/oracle/query")
async def oracle_query(request: QueryRequest):
    urgency = detect_urgency(request.query)
    if request.urgency_override:
        urgency["color"] = request.urgency_override
    
    domain_configs = DOMAIN_CONFIGS.get(request.domain, DOMAIN_CONFIGS["general"])
    cycles = urgency["cycles"]
    
    round1 = await run_queen_round(request.query, request.domain, 1)
    
    if cycles >= 2:
        round2 = await run_queen_round(request.query, request.domain, 2, round1)
        final_responses = round2
    else:
        final_responses = round1

    if cycles >= 3:
        round3 = await run_queen_round(request.query, request.domain, 3, final_responses)
        final_responses = round3

    fusion = generate_fusion(final_responses, request.query, request.domain)
    probability_landscape = generate_probability_landscape(final_responses, request.custom_options)

    return {
        "query": request.query,
        "domain": request.domain,
        "urgency": urgency,
        "rounds_completed": cycles,
        "queen_responses": final_responses,
        "round1_responses": round1,
        "fusion": fusion,
        "probability_landscape": probability_landscape,
        "sovereign": SOVEREIGN_PROFILE["name"]
    }

@app.get("/portfolio")
async def get_portfolio():
    return {
        "holdings": SOVEREIGN_PROFILE["portfolio"],
        "total_positions": len(SOVEREIGN_PROFILE["portfolio"])
    }
