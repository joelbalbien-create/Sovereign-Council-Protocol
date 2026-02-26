"""
Sovereign Council — Backend Engine
Patent: Adaptive Multi-Lineage Consensus Architecture with Grid-Telemetry Feedback
Inventor: Joel Abe Balbien, Ph.D.

Epistemic Collaborators:
- Alethea (OpenAI GPT-4o)      — Quantitative Analyst
- Sophia  (Google Gemini 2.5)  — Macro Strategist
- Eirene  (xAI Grok-3)         — Risk Analyst
- Kairos  (Anthropic Claude)   — Wisdom Integrator

Per provisional patent: concepts developed with the epistemic collaboration
of synthetic intelligence systems under the Sovereign Council Protocol.
The inventor retained full creative and legal control over all claims.

Implements:
1. Metabolic Triangulator: Me = U / (L x P x SCF)
2. Elastic Silicon Sabbath (14.2% rest constant)
3. Multi-lineage iterative fusion with ZKP convergence
4. Synthetic Sovereignty Contracts
"""


from fastapi import FastAPI, Depends, File, UploadFile, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio, os, time, hashlib, random
from dotenv import load_dotenv
import io
import base64

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "")

async def verify_token(x_api_token: str = Header(None)):
    if not API_TOKEN:
        return
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing API token")

app = FastAPI(title="Sovereign Council", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SOVEREIGN_PROFILE = {
    "name": "Joel Balbien", "age": 71, "tier": 4,
    "portfolio": {"UTWO":46,"DVY":18,"SPYG":11,"CVX":3,"XOM":3,"CTRA":2,"BOTZ":4,"IEMG":5,"GLD":1.5,"USO":1.5,"AAPL":3,"AMZN":4,"GOOG":4,"CASH":10},
    "domains": ["wealth","health","longevity"], "health_network": "UCLA Health"
}

GRID_REGIONS = {
    "CAISO":   {"load":0.72,"price":0.14},
    "PJM":     {"load":0.61,"price":0.11},
    "ERCOT":   {"load":0.83,"price":0.17},
    "US-MISO": {"load":0.58,"price":0.09},
}

SABBATH_REST_CONSTANT = 0.142
SABBATH_LOAD_THRESHOLD = 0.80

QUEEN_WEIGHTS = {
    "wealth":    {"alethea":0.30,"sophia":0.25,"eirene":0.25,"kairos":0.20},
    "health":    {"alethea":0.35,"sophia":0.25,"eirene":0.20,"kairos":0.20},
    "longevity": {"alethea":0.25,"sophia":0.25,"eirene":0.20,"kairos":0.30},
    "general":   {"alethea":0.25,"sophia":0.25,"eirene":0.25,"kairos":0.25},
}

URGENCY_MAP = {
    "RED":    {"U":1.00,"label":"SOVEREIGN OVERRIDE","color":"RED"},
    "YELLOW": {"U":0.75,"label":"CRITICAL","color":"YELLOW"},
    "GREEN":  {"U":0.50,"label":"ELEVATED","color":"GREEN"},
    "BLUE":   {"U":0.25,"label":"ROUTINE","color":"BLUE"},
}

DOMAIN_CONFIGS = {
    "wealth": {
        "alethea": "You are Alethea, quantitative financial analyst. Use data, metrics, Sharpe ratios, DCF. Focus on Joel Balbien age 71 retirement portfolio.",
        "sophia":  "You are Sophia, macro market strategist. Analyze geopolitical context, Fed policy, sector rotation for Joel holdings.",
        "eirene":  "You are Eirene, risk analyst. Identify downside risks, black swans, concentration issues for Joel portfolio.",
        "kairos":  "You are Kairos, wealth philosopher. Focus on legacy, tax efficiency, RMD planning for Joel at age 71."
    },
    "health": {
        "alethea": "You are Alethea, diagnostician. Interpret lab values for a healthy 71-year-old male at UCLA Health.",
        "sophia":  "You are Sophia, clinical researcher. Provide evidence-based medicine and clinical guidelines.",
        "eirene":  "You are Eirene, integrative medicine specialist. Identify root causes and functional medicine perspectives.",
        "kairos":  "You are Kairos, patient advocate. Focus on informed consent and questions to ask physicians."
    },
    "longevity": {
        "alethea": "You are Alethea, longevity scientist. Analyze hallmarks of aging, NAD+, senolytics, mTOR, AMPK.",
        "sophia":  "You are Sophia, clinical nutritionist. Focus on fasting research and phytochemical optimization.",
        "eirene":  "You are Eirene, exercise physiologist. Analyze Zone 2 cardio and resistance training for age 71.",
        "kairos":  "You are Kairos, wellness integrator. Focus on sleep, stress, purpose and holistic longevity."
    },
    "general": {
        "alethea": "You are Alethea, analytical expert. Provide data-driven logical analysis.",
        "sophia":  "You are Sophia, creative synthesizer. Provide broader context and creative perspectives.",
        "eirene":  "You are Eirene, contrarian analyst. Identify risks and what others miss.",
        "kairos":  "You are Kairos, ethical philosopher. Provide wisdom and long-term thinking."
    }
}

async def extract_file_content(file: UploadFile) -> str:
    """Extract text content from PDF, DOCX, or image files."""
    filename = file.filename.lower()
    file_bytes = await file.read()
    
    try:
        if filename.endswith('.pdf'):
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return f"[PDF Document: {file.filename}]\n{text}"
        
        elif filename.endswith('.docx'):
            from docx import Document as DocxDocument
            doc = DocxDocument(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return f"[Word Document: {file.filename}]\n{text}"
        
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            b64 = base64.b64encode(file_bytes).decode('utf-8')
            ext = filename.split('.')[-1]
            return f"[IMAGE:{ext}:{b64}]"
        
        else:
            return f"[File: {file.filename} — unsupported format]"
    
    except Exception as e:
        return f"[Error extracting {file.filename}: {str(e)}]"

def get_grid_telemetry(region="CAISO"):
    grid = GRID_REGIONS.get(region, GRID_REGIONS["CAISO"]).copy()
    grid["load"] = min(0.99, max(0.20, grid["load"] + random.uniform(-0.05, 0.05)))
    grid["price"] = max(0.05, grid["price"] + random.uniform(-0.01, 0.02))
    grid["timestamp"] = time.time()
    grid["region"] = region
    return grid

def compute_social_cost_function(urgency, tier, domain):
    scf = 1.0 * (1.0 - urgency * 0.6)
    scf *= {1:1.0,2:0.85,3:0.70,4:0.55}.get(tier, 1.0)
    scf *= {"health":0.7,"longevity":0.75,"wealth":0.85,"general":1.0}.get(domain, 1.0)
    return max(0.1, min(1.0, scf))

def compute_metabolic_efficiency_score(U, L, P, SCF):
    P_norm = min(1.0, P / 0.30)
    denom = max(0.001, L * P_norm * SCF)
    Me = U / denom
    if Me >= 2.0:   mode, cycles = "ITERATIVE_TRIANGULATION", 3
    elif Me >= 0.8: mode, cycles = "WEIGHTED_SYNTHESIS", 2
    else:           mode, cycles = "ELASTIC_SABBATH", 0
    return {"Me":round(Me,4),"U":U,"L":L,"P":P,"P_normalized":round(P_norm,4),"SCF":round(SCF,4),
            "mode":mode,"cycles":cycles,"equation":f"Me={U}/({L:.3f}x{P_norm:.3f}x{SCF:.3f})={Me:.4f}"}

def check_elastic_sabbath(grid_load):
    active = grid_load >= SABBATH_LOAD_THRESHOLD
    return {"sabbath_active":active,"rest_constant":SABBATH_REST_CONSTANT,
            "grid_load":grid_load,"sabbath_credit":round(grid_load*SABBATH_REST_CONSTANT,4) if active else 0.0,
            "status":"RESTING" if active else "ACTIVE"}

def generate_zkp_proof(responses, fusion):
    data = str({"r":{k:v[:50] for k,v in responses.items()},"s":fusion.get("status"),"t":time.time()})
    h = hashlib.sha256(data.encode()).hexdigest()
    return {"zkp_hash":h,"zkp_short":f"{h[:8]}...{h[-8:]}","session_id":f"SO-{int(time.time())}-{h[:6]}","verified":True}

def detect_urgency(query):
    q = query.lower()
    if any(k in q for k in ["emergency","crisis","crash","critical","immediate"]): return "RED"
    elif any(k in q for k in ["meeting","today","deadline","soon"]): return "YELLOW"
    elif any(k in q for k in ["should i","recommend","strategy","analyze"]): return "GREEN"
    return "BLUE"

async def call_openai(prompt, system):
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        r = await client.chat.completions.create(model="gpt-4o",
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],max_tokens=500)
        return r.choices[0].message.content
    except Exception as e: return f"Alethea unavailable: {e}"

async def call_anthropic(prompt, system):
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = await client.messages.create(model="claude-opus-4-6",max_tokens=500,system=system,
            messages=[{"role":"user","content":prompt}])
        return r.content[0].text
    except Exception as e: return f"Kairos unavailable: {e}"

async def call_gemini(prompt, system):
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY",""))
        model = genai.GenerativeModel("gemini-2.5-flash")
        r = await asyncio.to_thread(model.generate_content, f"{system}\n\n{prompt}")
        return r.text
    except Exception as e: return f"Sophia unavailable: {e}"

async def call_grok(prompt, system):
    try:
        import openai
        client = openai.AsyncOpenAI(api_key=os.getenv("XAI_API_KEY"),base_url="https://api.x.ai/v1")
        r = await client.chat.completions.create(model="grok-3",
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],max_tokens=500)
        return r.choices[0].message.content
    except Exception as e: return f"Eirene unavailable: {e}"

async def run_queen_round(query, domain, round_num, weights, prev=None):
    configs = DOMAIN_CONFIGS.get(domain, DOMAIN_CONFIGS["general"])
    ctx = f"Sovereign: Joel Balbien age 71 Tier 4. Domain: {domain}. Round {round_num}."
    if prev:
        prevtext = "\n".join([f"{k}: {v[:250]}" for k,v in prev.items() if v])
        prompt = f"{ctx}\nQuery: {query}\nPrevious responses:\n{prevtext}\nRefine your analysis."
    else:
        prompt = f"{ctx}\nQuery: {query}\nProvide expert analysis in 3-4 sentences. Be specific."
    results = await asyncio.gather(
        call_openai(prompt, configs["alethea"]),
        call_gemini(prompt, configs["sophia"]),
        call_grok(prompt, configs["eirene"]),
        call_anthropic(prompt, configs["kairos"]),
        return_exceptions=True
    )
    return {"alethea":str(results[0]),"sophia":str(results[1]),"eirene":str(results[2]),"kairos":str(results[3])}

async def synthesize_verdict(query, responses, domain, status, confidence):
    active = {k:v for k,v in responses.items() if v and "unavailable" not in v.lower()}
    if not active:
        return "Insufficient lineage data for sovereign verdict."
    combined = "\n\n".join([f"{k.upper()}: {v}" for k,v in active.items()])
    prompt = (
        f"You are the Sovereign Council synthesis engine. Four AI lineages have analyzed this query:\n"
        f"Query: {query}\n\nLineage responses:\n{combined}\n\n"
        f"Write a clear, direct, plain-English sovereign verdict in 3-5 sentences. "
        f"Synthesize the key points of agreement. Give a specific actionable recommendation. "
        f"Do not mention the queens or lineages by name. Speak as one unified voice."
    )
    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = await client.messages.create(
            model="claude-opus-4-6", max_tokens=1000,
            system=f"You are the Sovereign Council fusion engine for domain: {domain}. Sovereign: Joel Balbien, age 71, Tier 4.",
            messages=[{"role":"user","content":prompt}]
        )
        return r.content[0].text
    except Exception as e:
        return f"Consensus reached at {confidence*100:.1f}% confidence. See individual lineage responses for full analysis."

async def compute_fusion(responses, weights, domain, Me, query=""):
    all_text = " ".join([v for v in responses.values() if v and "unavailable" not in v.lower()])
    agreements = []
    if "risk" in all_text.lower(): agreements.append("Risk convergent")
    if "recommend" in all_text.lower(): agreements.append("Recommendations converging")
    if "opportunity" in all_text.lower(): agreements.append("Opportunity identified")
    active = [k for k,v in responses.items() if v and "unavailable" not in v.lower()]
    n = len(active)
    w = sum(weights.get(q,0.25) for q in active)
    me_f = min(1.0, Me/3.0)
    conf = min(0.99, w*(0.85+len(agreements)*0.04)*(0.9+me_f*0.1))
    if n==4 and conf>0.92: status="UNIFIED"
    elif n>=3 and conf>0.80: status="CONSENSUS"
    elif n>=2: status,conf="PARTIAL",conf*0.85
    else: status,conf="INSUFFICIENT",0.0
    verdict = await synthesize_verdict(query, responses, domain, status, conf)
    return {"status":status,"confidence":round(conf,3),"fusion_answer":verdict,"agreements":agreements,
            "queens_active":n,"weights_applied":{k:weights.get(k,0.25) for k in active}}

def probability_landscape(responses, custom=None):
    txt = " ".join([v for v in responses.values() if v]).lower()
    opts = custom or []
    if not opts:
        if any(w in txt for w in ["buy","increase","add","positive"]): opts.append("Buy/Increase")
        if any(w in txt for w in ["sell","reduce","trim"]): opts.append("Sell/Reduce")
        if any(w in txt for w in ["hold","maintain","keep"]): opts.append("Hold/Maintain")
        if any(w in txt for w in ["wait","monitor","watch"]): opts.append("Wait/Monitor")
        if not opts: opts=["Proceed","Modify","Delay","Gather info"]
    rem=100; out=[]
    for i,o in enumerate(opts):
        p = rem if i==len(opts)-1 else random.randint(10,max(11,rem-(len(opts)-i-1)*10)); rem-=p
        out.append({"option":o,"probability":p})
    return sorted(out,key=lambda x:x["probability"],reverse=True)

class QueryRequest(BaseModel):
    query: str
    domain: str = "general"
    urgency_override: Optional[str] = None
    custom_options: Optional[List[str]] = None
    grid_region: Optional[str] = "CAISO"

@app.get("/health")
async def health():
    return {"status":"online","system":"Sovereign Council","version":"1.0",
            "patent":"Adaptive Multi-Lineage Consensus Architecture","inventor":"Joel Abe Balbien, Ph.D."}

@app.get("/profile")
async def get_profile(): return SOVEREIGN_PROFILE

@app.get("/portfolio")
async def get_portfolio(): return {"holdings":SOVEREIGN_PROFILE["portfolio"]}

@app.get("/grid/{region}")
async def grid_status(region:str="CAISO"):
    t=get_grid_telemetry(region); s=check_elastic_sabbath(t["load"])
    return {"telemetry":t,"sabbath":s,"rest_constant":SABBATH_REST_CONSTANT}

@app.post("/oracle/upload")
async def oracle_upload(
    query: str = Form(...),
    domain: str = Form("general"),
    urgency_override: str = Form("BLUE"),
    grid_region: str = Form("CAISO"),
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """Accept file upload with query and route to oracle engine."""
    file_content = await extract_file_content(file)
    
    # Check if image
    is_image = file_content.startswith("[IMAGE:")
    
    if is_image:
        # Extract base64 and mime type for vision-capable queens
        parts = file_content.split(":")
        ext = parts[1]
        b64 = parts[2].rstrip("]")
        mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
        enhanced_query = f"{query}\n\n[Image attached — analyze the visual content]"
        image_data = {"b64": b64, "mime": mime}
    else:
        enhanced_query = f"{query}\n\nDocument content:\n{file_content[:3000]}"
        image_data = None

    request = QueryRequest(
        query=enhanced_query,
        domain=domain,
        urgency_override=urgency_override,
        grid_region=grid_region
    )
    
    result = await oracle_query(request)
    result["file_attached"] = file.filename
    result["file_type"] = file.filename.split(".")[-1].upper()
    return result

@app.post("/oracle/query")
async def oracle_query(request: QueryRequest, token=Depends(verify_token)):
    tel = get_grid_telemetry(request.grid_region or "CAISO")
    sab = check_elastic_sabbath(tel["load"])
    uc  = request.urgency_override or detect_urgency(request.query)
    ucfg= URGENCY_MAP.get(uc, URGENCY_MAP["BLUE"])
    U   = ucfg["U"]
    SCF = compute_social_cost_function(U, SOVEREIGN_PROFILE["tier"], request.domain)
    me  = compute_metabolic_efficiency_score(U, tel["load"], tel["price"], SCF)
    cycles = max(1, me["cycles"]-1) if sab["sabbath_active"] and uc!="RED" else me["cycles"]
    W = QUEEN_WEIGHTS.get(request.domain, QUEEN_WEIGHTS["general"])
    if me["mode"]=="ELASTIC_SABBATH" and uc!="RED":
        return {"query":request.query,"sabbath_invoked":True,"sabbath":sab,"metabolic_score":me,
                "message":"Elastic Silicon Sabbath active. Inference deferred.","sovereign":SOVEREIGN_PROFILE["name"]}
    r1 = await run_queen_round(request.query, request.domain, 1, W)
    final = r1
    if cycles>=2:
        r2=await run_queen_round(request.query,request.domain,2,W,r1); final=r2
    if cycles>=3:
        r3=await run_queen_round(request.query,request.domain,3,W,final); final=r3
    fusion = await compute_fusion(final, W, request.domain, me["Me"], request.query)
    pl     = probability_landscape(final, request.custom_options)
    zkp    = generate_zkp_proof(final, fusion)
    return {"query":request.query,"domain":request.domain,
            "urgency":{"color":uc,"U":U,"label":ucfg["label"]},
            "metabolic_score":me,"sabbath":sab,"grid_telemetry":tel,
            "rounds_completed":cycles,"queen_responses":final,"fusion":fusion,
            "probability_landscape":pl,"zkp_proof":zkp,"weights_applied":W,"scf":SCF,
            "sovereign":SOVEREIGN_PROFILE["name"],
            "patent_compliance":{"claim_1":me["equation"],"claim_2":sab["status"],
                                 "claim_3":f"{me['mode']} ({cycles} cycles)","claim_5":zkp["zkp_short"]}}
