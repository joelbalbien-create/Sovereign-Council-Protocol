import React, { useState, useEffect, useRef } from "react";

const CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600&display=swap');

  :root {
    --gold:     #c8a84b;
    --gold-lt:  #f0d080;
    --gold-dim: #7a6030;
    --ice:      #a8d8f0;
    --aurora-1: #0a4a7a;
    --aurora-2: #1a2a6a;
    --aurora-3: #0a3a5a;
    --aurora-4: #2a1a4a;
    --bg:       #000204;
  }

  * { margin:0; padding:0; box-sizing:border-box; }
  body { background: var(--bg); overflow-x:hidden; }

  @keyframes aurora-shift-1 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(80px,-60px) scale(1.1); }
    66%      { transform: translate(-40px,80px) scale(0.9); }
  }
  @keyframes aurora-shift-2 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(-100px,40px) scale(1.15); }
    66%      { transform: translate(60px,-80px) scale(0.95); }
  }
  @keyframes aurora-shift-3 {
    0%,100% { transform: translate(0,0) scale(1); }
    50%      { transform: translate(60px,60px) scale(1.05); }
  }
  @keyframes aurora-shift-4 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%      { transform: translate(-80px,-40px) scale(1.1); }
    80%      { transform: translate(40px,60px) scale(0.9); }
  }
  @keyframes orb-pulse {
    0%,100% { box-shadow: 0 0 20px currentColor, 0 0 40px currentColor; transform: scale(1); }
    50%     { box-shadow: 0 0 30px currentColor, 0 0 60px currentColor; transform: scale(1.08); }
  }
  @keyframes scan-line {
    0%   { top: -2px; }
    100% { top: 100%; }
  }
  @keyframes gold-shimmer {
    0%,100% { background-position: 0% 50%; }
    50%     { background-position: 100% 50%; }
  }
  @keyframes fade-in {
    from { opacity:0; } to { opacity:1; }
  }
  @keyframes fade-up {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
  }
  @keyframes spin-slow {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }
  @keyframes particle-float {
    0%           { opacity:0; transform:translateY(0) translateX(0); }
    10%          { opacity:0.6; }
    90%          { opacity:0.3; }
    100%         { opacity:0; transform:translateY(-100vh) translateX(var(--drift)); }
  }
  @keyframes typewriter-cursor {
    0%,100% { opacity:1; } 50% { opacity:0; }
  }
  @keyframes glow-pulse {
    0%,100% { opacity:0.6; } 50% { opacity:1; }
  }
`;

function Aurora() {
  return (
    <div style={{ position:"fixed", inset:0, zIndex:0, overflow:"hidden" }}>
      <div style={{ position:"absolute", inset:0,
        background:"radial-gradient(ellipse at 50% 40%, #010d1a 0%, #000204 70%)" }} />
      {[
        { color:"var(--aurora-1)", x:"20%", y:"30%", w:700, h:400, anim:"aurora-shift-1 18s ease-in-out infinite" },
        { color:"var(--aurora-2)", x:"60%", y:"20%", w:600, h:500, anim:"aurora-shift-2 22s ease-in-out infinite" },
        { color:"var(--aurora-3)", x:"40%", y:"60%", w:800, h:300, anim:"aurora-shift-3 26s ease-in-out infinite" },
        { color:"var(--aurora-4)", x:"75%", y:"50%", w:500, h:400, anim:"aurora-shift-4 20s ease-in-out infinite" },
      ].map((b,i) => (
        <div key={i} style={{
          position:"absolute", left:b.x, top:b.y, width:b.w, height:b.h,
          borderRadius:"50%",
          background:`radial-gradient(ellipse,${b.color}50 0%,transparent 70%)`,
          filter:"blur(60px)", animation:b.anim, transformOrigin:"center",
        }} />
      ))}
      <div style={{
        position:"absolute", inset:0,
        background:"repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.06) 3px,rgba(0,0,0,0.06) 4px)",
        pointerEvents:"none",
      }} />
      <div style={{
        position:"absolute", left:0, right:0, height:2,
        background:"linear-gradient(90deg,transparent,rgba(200,168,75,0.15),transparent)",
        animation:"scan-line 8s linear infinite",
      }} />
      <div style={{
        position:"absolute", inset:0,
        background:"radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.85) 100%)",
      }} />
    </div>
  );
}

function Particles({ count=20, active=true }) {
  const particles = Array.from({ length:count }, (_,i) => ({
    id:i, left:Math.random()*100, delay:Math.random()*8,
    duration:6+Math.random()*10, size:1+Math.random()*2,
    drift:(Math.random()-0.5)*200,
    color:["var(--gold)","var(--ice)","#00ff88","#b44fff"][Math.floor(Math.random()*4)],
  }));
  if (!active) return null;
  return (
    <div style={{ position:"fixed", inset:0, pointerEvents:"none", zIndex:2, overflow:"hidden" }}>
      {particles.map(p => (
        <div key={p.id} style={{
          position:"absolute", left:`${p.left}%`, bottom:"-10px",
          width:p.size, height:p.size*4, background:p.color, borderRadius:2,
          "--drift":`${p.drift}px`,
          animation:`particle-float ${p.duration}s ${p.delay}s ease-in infinite`,
          opacity:0,
        }} />
      ))}
    </div>
  );
}

const QUEEN_COLORS = {
  alethea: "#00b4ff",
  sophia:  "#ff6b9d", 
  eirene:  "#00ff88",
  kairos:  "#b44fff",
};

const STATUS_COLORS = {
  UNIFIED:      "#00ff88",
  CONSENSUS:    "#ffb300",
  PARTIAL:      "#00b4ff",
  INSUFFICIENT: "#ff2244",
};

const URGENCY_COLORS = {
  RED:    "#ff2244",
  YELLOW: "#ffb300",
  GREEN:  "#00ff88",
  BLUE:   "#00b4ff",
};

function QueenOrb({ name, response, loading }) {
  const color = QUEEN_COLORS[name] || "#888";
  const isError = response && response.toLowerCase().includes("unavailable");
  return (
    <div style={{
      background: "rgba(0,0,0,0.6)",
      border: `1px solid ${color}44`,
      borderRadius: 8, padding: "16px",
      backdropFilter: "blur(10px)",
    }}>
      <div style={{ display:"flex", alignItems:"center", gap:10, marginBottom:10 }}>
        <div style={{
          width:12, height:12, borderRadius:"50%",
          background: loading ? color : isError ? "#ff2244" : color,
          boxShadow: `0 0 ${loading ? "12px" : "6px"} ${color}`,
          animation: loading ? "orb-pulse 1.5s ease-in-out infinite" : "none",
          flexShrink:0,
        }} />
        <span style={{ fontFamily:"'Cinzel',serif", fontSize:11, color, letterSpacing:"0.15em", fontWeight:600 }}>
          {name.toUpperCase()}
        </span>
        {loading && (
          <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:8, color:`${color}88`, letterSpacing:"0.1em" }}>
            TRIANGULATING...
          </span>
        )}
      </div>
      {response && (
        <div style={{
          background: "#ffffff",
          border: `1px solid ${color}33`,
          borderRadius:6, padding:"12px",
        }}>
          <p style={{ fontFamily:"Georgia,serif", fontSize:12, color:"#111111", lineHeight:1.7, margin:0 }}>
            {response}
          </p>
        </div>
      )}
    </div>
  );
}

function FusionDisplay({ fusion }) {
  if (!fusion) return null;
  const statusColor = STATUS_COLORS[fusion.status] || "#888";
  return (
    <div style={{
      background:"rgba(0,0,0,0.7)",
      border:`2px solid ${statusColor}66`,
      borderRadius:8, padding:"20px",
      backdropFilter:"blur(10px)",
    }}>
      <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:14 }}>
        <div style={{ width:10,height:10,borderRadius:"50%", background:statusColor, boxShadow:`0 0 10px ${statusColor}` }} />
        <span style={{ fontFamily:"'Cinzel',serif", fontSize:13, color:statusColor, letterSpacing:"0.2em", fontWeight:700 }}>
          {fusion.status}
        </span>
        <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:10, color:`${statusColor}88` }}>
          {fusion.confidence && `${(fusion.confidence*100).toFixed(1)}% CONFIDENCE`}
        </span>
        <span style={{ marginLeft:"auto", fontFamily:"'Share Tech Mono',monospace", fontSize:9, color:"rgba(200,168,75,0.5)" }}>
          {fusion.queens_active}/4 LINEAGES
        </span>
      </div>
      <div style={{
        background:"#ffffff",
        border:`2px solid ${statusColor}`,
        borderRadius:6, padding:"16px 20px",
      }}>
        <div style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:9, letterSpacing:3, marginBottom:8, fontWeight:"bold", color:statusColor }}>
          SOVEREIGN VERDICT
        </div>
        <p style={{ color:"#000000", fontSize:15, lineHeight:2.0, fontFamily:"Georgia,serif", margin:0 }}>
          {fusion.fusion_answer}
        </p>
      </div>
      {fusion.agreements && fusion.agreements.length > 0 && (
        <div style={{ marginTop:10, display:"flex", gap:8, flexWrap:"wrap" }}>
          {fusion.agreements.map((a,i) => (
            <span key={i} style={{
              fontFamily:"'Share Tech Mono',monospace", fontSize:8,
              color:`${statusColor}88`, border:`1px solid ${statusColor}33`,
              borderRadius:3, padding:"3px 8px", letterSpacing:"0.08em"
            }}>{a}</span>
          ))}
        </div>
      )}
    </div>
  );
}

function ProbabilityLandscape({ landscape }) {
  if (!landscape || !landscape.length) return null;
  const max = Math.max(...landscape.map(l => l.probability));
  return (
    <div style={{ background:"rgba(0,0,0,0.6)", border:"1px solid rgba(200,168,75,0.2)", borderRadius:8, padding:"16px", backdropFilter:"blur(10px)" }}>
      <div style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:9, color:"var(--gold-dim)", letterSpacing:"0.2em", marginBottom:12 }}>
        PROBABILITY LANDSCAPE
      </div>
      {landscape.map((item,i) => (
        <div key={i} style={{ marginBottom:8 }}>
          <div style={{ display:"flex", justifyContent:"space-between", marginBottom:3 }}>
            <span style={{ fontFamily:"Georgia,serif", fontSize:12, color:"rgba(200,216,232,0.9)" }}>{item.option}</span>
            <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:10, color:"var(--gold)" }}>{item.probability}%</span>
          </div>
          <div style={{ height:4, background:"rgba(255,255,255,0.08)", borderRadius:2, overflow:"hidden" }}>
            <div style={{
              width:`${(item.probability/max)*100}%`, height:"100%", borderRadius:2,
              background:`linear-gradient(90deg, var(--gold-dim), var(--gold))`,
              transition:"width 0.8s ease",
            }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function MetabolicScore({ me }) {
  if (!me) return null;
  const modeColor = me.mode === "ITERATIVE_TRIANGULATION" ? "#00ff88" : me.mode === "WEIGHTED_SYNTHESIS" ? "#ffb300" : "#ff2244";
  return (
    <div style={{ background:"rgba(0,0,0,0.5)", border:"1px solid rgba(200,168,75,0.15)", borderRadius:6, padding:"10px 14px", backdropFilter:"blur(8px)" }}>
      <div style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:8, color:"var(--gold-dim)", letterSpacing:"0.15em", marginBottom:6 }}>
        METABOLIC EFFICIENCY SCORE
      </div>
      <div style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:11, color:"var(--gold)", letterSpacing:"0.05em", marginBottom:4 }}>
        Me = {me.Me} &nbsp;|&nbsp; <span style={{ color:modeColor }}>{me.mode.replace(/_/g," ")}</span>
      </div>
      <div style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:8, color:"rgba(200,168,75,0.4)" }}>
        {me.equation}
      </div>
    </div>
  );
}

export default function SovereignOracle() {
  const [query, setQuery]             = useState("");
  const [domain, setDomain]           = useState("general");
  const [urgency, setUrgency]         = useState("BLUE");
  const [loading, setLoading]         = useState(false);
  const [result, setResult]           = useState(null);
  const [showQueens, setShowQueens]   = useState(false);
  const [attachedFile, setAttachedFile] = useState(null);
  const [fileName, setFileName]       = useState("");
  const fileInputRef                  = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) { setAttachedFile(file); setFileName(file.name); }
  };

  const handleQuery = async () => {
    if (!query.trim() || loading) return;
    setLoading(true); setResult(null);
    try {
      let data;
      if (attachedFile) {
        const formData = new FormData();
        formData.append("query", query.trim());
        formData.append("domain", domain);
        formData.append("urgency_override", urgency);
        formData.append("file", attachedFile);
        const response = await fetch("http://sovereign-oracle.local:8002/oracle/upload", { method:"POST", body:formData });
        data = await response.json();
      } else {
        const response = await fetch("http://sovereign-oracle.local:8002/oracle/query", {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body:JSON.stringify({ query:query.trim(), domain, urgency_override:urgency }),
        });
        data = await response.json();
      }
      setResult(data);
    } catch(err) {
      setResult({ error:"Unable to reach Sovereign Oracle backend." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const handler = (e) => { if ((e.metaKey||e.ctrlKey) && e.key==="Enter") handleQuery(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [query, domain, urgency, loading, attachedFile]);

  const urgencyColor = URGENCY_COLORS[urgency] || "#888";

  return (
    <>
      <style>{CSS}</style>
      <div style={{ position:"relative", minHeight:"100vh", width:"100%", overflow:"hidden", fontFamily:"Georgia,serif" }}>
        <Aurora />
        <Particles count={15} active={loading} />

        <div style={{ position:"relative", zIndex:10, maxWidth:900, margin:"0 auto", padding:"40px 24px" }}>

          {/* Header */}
          <div style={{ textAlign:"center", marginBottom:40, animation:"fade-up 0.8s ease" }}>
            <div style={{ display:"flex", justifyContent:"center", gap:20, marginBottom:16 }}>
              {Object.entries(QUEEN_COLORS).map(([name,color]) => (
                <div key={name} style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:5 }}>
                  <div style={{
                    width:14, height:14, borderRadius:"50%", background:color,
                    boxShadow:`0 0 12px ${color}, 0 0 24px ${color}44`,
                    animation:"orb-pulse 3s ease-in-out infinite",
                  }} />
                  <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:7, color:`${color}88`, letterSpacing:"0.1em" }}>
                    {name.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
            <h1 style={{
              fontFamily:"'Cinzel',serif", fontSize:42, fontWeight:700, letterSpacing:"0.12em",
              background:"linear-gradient(135deg, var(--gold) 0%, var(--gold-lt) 40%, var(--gold) 100%)",
              backgroundSize:"200% 100%", WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent",
              backgroundClip:"text", animation:"gold-shimmer 4s ease infinite",
            }}>
              SOVEREIGN ORACLE
            </h1>
            <p style={{ fontFamily:"'Cinzel',serif", fontSize:11, color:"var(--ice)", opacity:0.7, letterSpacing:"0.25em", marginTop:6 }}>
              JOEL BALBIEN · TIER 4 SOVEREIGN · FOUR LINEAGE FUSION
            </p>
          </div>

          {/* Query Panel */}
          <div style={{
            background:"rgba(0,0,0,0.7)", border:"1px solid rgba(200,168,75,0.3)",
            borderRadius:10, padding:24, backdropFilter:"blur(12px)",
            marginBottom:24, animation:"fade-up 0.8s ease 0.2s both",
          }}>
            {/* Domain + Urgency */}
            <div style={{ display:"flex", gap:12, marginBottom:16 }}>
              {["general","wealth","health","longevity"].map(d => (
                <button key={d} onClick={() => setDomain(d)} style={{
                  padding:"6px 14px", borderRadius:4,
                  background: domain===d ? "rgba(200,168,75,0.15)" : "rgba(0,0,0,0.3)",
                  border:`1px solid ${domain===d ? "var(--gold)" : "rgba(200,168,75,0.2)"}`,
                  color: domain===d ? "var(--gold)" : "rgba(200,168,75,0.5)",
                  fontFamily:"'Cinzel',serif", fontSize:9, letterSpacing:"0.15em",
                  cursor:"pointer", transition:"all 0.2s",
                }}>
                  {d.toUpperCase()}
                </button>
              ))}
              <div style={{ marginLeft:"auto", display:"flex", gap:8 }}>
                {["BLUE","GREEN","YELLOW","RED"].map(u => (
                  <button key={u} onClick={() => setUrgency(u)} style={{
                    width:28, height:28, borderRadius:"50%",
                    background: urgency===u ? `${URGENCY_COLORS[u]}33` : "rgba(0,0,0,0.3)",
                    border:`1px solid ${urgency===u ? URGENCY_COLORS[u] : URGENCY_COLORS[u]+"44"}`,
                    cursor:"pointer", transition:"all 0.2s",
                    boxShadow: urgency===u ? `0 0 10px ${URGENCY_COLORS[u]}66` : "none",
                  }} />
                ))}
              </div>
            </div>

            {/* Textarea */}
            <textarea
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Ask your sovereign council..."
              style={{
                width:"100%", minHeight:100, background:"rgba(0,0,0,0.4)",
                border:"1px solid rgba(200,168,75,0.2)", borderRadius:6,
                color:"#e0e0e0", fontFamily:"Georgia,serif", fontSize:14,
                padding:"12px 14px", resize:"vertical", outline:"none",
                lineHeight:1.7,
              }}
            />

            {/* Controls */}
            <div style={{ display:"flex", alignItems:"center", gap:12, marginTop:12 }}>
              <input type="file" ref={fileInputRef} onChange={handleFileSelect}
                accept=".pdf,.docx,.jpg,.jpeg,.png" style={{ display:"none" }} />
              <button onClick={() => fileInputRef.current.click()} style={{
                padding:"7px 14px",
                background: attachedFile ? "rgba(0,255,136,0.1)" : "rgba(0,0,0,0.3)",
                border:`1px solid ${attachedFile ? "#00ff88" : "rgba(200,168,75,0.2)"}`,
                borderRadius:4, color: attachedFile ? "#00ff88" : "rgba(200,168,75,0.5)",
                fontFamily:"'Share Tech Mono',monospace", fontSize:9, letterSpacing:"0.1em",
                cursor:"pointer",
              }}>
                {attachedFile ? `📎 ${fileName}` : "📎 ATTACH"}
              </button>
              {attachedFile && (
                <button onClick={() => { setAttachedFile(null); setFileName(""); }} style={{
                  background:"transparent", border:"none", color:"#ff2244", fontSize:14, cursor:"pointer",
                }}>✕</button>
              )}
              <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:12 }}>
                <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:8, color:"rgba(200,168,75,0.3)", letterSpacing:"0.1em" }}>
                  CMD+ENTER
                </span>
                <button onClick={handleQuery} disabled={loading || !query.trim()} style={{
                  padding:"10px 28px",
                  background: loading ? "rgba(200,168,75,0.05)" : "linear-gradient(135deg,rgba(200,168,75,0.15),rgba(200,168,75,0.08))",
                  border:`1px solid ${loading ? "rgba(200,168,75,0.2)" : "var(--gold)"}`,
                  borderRadius:4, color:"var(--gold)",
                  fontFamily:"'Cinzel',serif", fontSize:11, letterSpacing:"0.2em",
                  cursor: loading ? "not-allowed" : "pointer",
                  boxShadow: loading ? "none" : "0 0 20px rgba(200,168,75,0.2)",
                  transition:"all 0.3s",
                }}>
                  {loading ? "TRIANGULATING..." : "INVOKE"}
                </button>
              </div>
            </div>
          </div>

          {/* Results */}
          {result && !result.error && (
            <div style={{ display:"flex", flexDirection:"column", gap:16, animation:"fade-up 0.6s ease" }}>

              {/* Metabolic Score */}
              {result.metabolic_score && <MetabolicScore me={result.metabolic_score} />}

              {/* Fusion */}
              {result.fusion && <FusionDisplay fusion={result.fusion} />}

              {/* Probability Landscape */}
              {result.probability_landscape && <ProbabilityLandscape landscape={result.probability_landscape} />}

              {/* Queen Responses Toggle */}
              {result.queen_responses && (
                <div>
                  <button onClick={() => setShowQueens(!showQueens)} style={{
                    background:"rgba(0,0,0,0.5)", border:"1px solid rgba(200,168,75,0.2)",
                    borderRadius:6, padding:"10px 20px", color:"var(--gold-dim)",
                    fontFamily:"'Share Tech Mono',monospace", fontSize:9, letterSpacing:"0.15em",
                    cursor:"pointer", width:"100%", marginBottom: showQueens ? 12 : 0,
                  }}>
                    {showQueens ? "▲ HIDE" : "▼ SHOW"} INDIVIDUAL LINEAGE RESPONSES
                  </button>
                  {showQueens && (
                    <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:12 }}>
                      {Object.entries(result.queen_responses).map(([name, response]) => (
                        <QueenOrb key={name} name={name} response={response} loading={false} />
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* ZKP */}
              {result.zkp_proof && (
                <div style={{ background:"rgba(0,0,0,0.5)", border:"1px solid rgba(200,168,75,0.1)", borderRadius:6, padding:"10px 14px" }}>
                  <span style={{ fontFamily:"'Share Tech Mono',monospace", fontSize:8, color:"rgba(200,168,75,0.3)", letterSpacing:"0.1em" }}>
                    ZKP VERIFIED · SESSION {result.zkp_proof.session_id} · {result.zkp_proof.zkp_short}
                  </span>
                </div>
              )}
            </div>
          )}

          {result && result.error && (
            <div style={{ background:"rgba(255,34,68,0.1)", border:"1px solid #ff224444", borderRadius:8, padding:16 }}>
              <p style={{ color:"#ff2244", fontFamily:"'Share Tech Mono',monospace", fontSize:11 }}>{result.error}</p>
            </div>
          )}

        </div>
      </div>
    </>
  );
}
