import { useState, useEffect, useRef } from "react";

const URGENCY_CONFIG = {
  RED: { label: "SOVEREIGN OVERRIDE", color: "#ff2020", glow: "rgba(255,32,32,0.4)", cycles: 1 },
  YELLOW: { label: "CRITICAL", color: "#ffb800", glow: "rgba(255,184,0,0.4)", cycles: 2 },
  GREEN: { label: "ELEVATED", color: "#00e87a", glow: "rgba(0,232,122,0.4)", cycles: 3 },
  BLUE: { label: "ROUTINE", color: "#00aaff", glow: "rgba(0,170,255,0.4)", cycles: 3 },
};

const DOMAINS = [
  { id: "wealth", label: "WEALTH", icon: "◈" },
  { id: "health", label: "HEALTH", icon: "◉" },
  { id: "longevity", label: "LONGEVITY", icon: "◊" },
  { id: "general", label: "GENERAL", icon: "◎" },
];

const QUEENS = [
  { id: "alethea", name: "ALETHEA", role: "Analyst", color: "#00aaff" },
  { id: "sophia", name: "SOPHIA", role: "Strategist", color: "#a855f7" },
  { id: "eirene", name: "EIRENE", role: "Risk", color: "#ff6b35" },
  { id: "kairos", name: "KAIROS", role: "Wisdom", color: "#00e87a" },
];

function PulsingOrb({ color, size = 12, active = false }) {
  return (
    <div style={{ position: "relative", width: size, height: size }}>
      <div style={{
        width: size, height: size, borderRadius: "50%",
        background: active ? color : "#333",
        boxShadow: active ? `0 0 ${size}px ${color}` : "none",
        transition: "all 0.5s ease",
      }} />
      {active && (
        <div style={{
          position: "absolute", top: 0, left: 0,
          width: size, height: size, borderRadius: "50%",
          background: color, opacity: 0.4,
          animation: "pulse 2s infinite",
        }} />
      )}
    </div>
  );
}

function QueenCard({ queen, response, active, loading }) {
  const isUnavailable = response && response.toLowerCase().includes("unavailable");
  const hasResponse = response && !loading;
  return (
    <div style={{
      border: `1px solid ${active ? queen.color + "60" : "#1e1e1e"}`,
      borderRadius: 8, padding: "16px",
      background: active ? `${queen.color}08` : "#0a0a0a",
      transition: "all 0.5s ease", position: "relative", overflow: "hidden",
    }}>
      {active && (
        <div style={{
          position: "absolute", top: 0, left: 0, right: 0, height: 1,
          background: `linear-gradient(90deg, transparent, ${queen.color}, transparent)`,
        }} />
      )}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
        <PulsingOrb color={queen.color} size={8} active={active} />
        <span style={{ color: queen.color, fontFamily: "monospace", fontSize: 11, letterSpacing: 3, fontWeight: 700 }}>
          {queen.name}
        </span>
        <span style={{ color: "#444", fontFamily: "monospace", fontSize: 9, letterSpacing: 2 }}>
          {queen.role}
        </span>
      </div>
      {loading && active && (
        <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
          {[0,1,2].map(i => (
            <div key={i} style={{
              width: 4, height: 4, borderRadius: "50%", background: queen.color,
              animation: `bounce 1.2s ${i * 0.2}s infinite`,
            }} />
          ))}
        </div>
      )}
      {hasResponse && (
        <div style={{
          color: isUnavailable ? "#444" : "#b0b0b0",
          fontSize: 11, lineHeight: 1.7,
          fontFamily: isUnavailable ? "monospace" : "Georgia, serif",
          maxHeight: 180, overflowY: "auto",
        }}>
          {isUnavailable ? "— LINEAGE UNAVAILABLE —" : response}
        </div>
      )}
    </div>
  );
}

function FusionDisplay({ fusion }) {
  if (!fusion) return null;
  const confidence = Math.round(fusion.confidence * 100);
  const statusColor = fusion.status === "UNIFIED" ? "#00e87a"
    : fusion.status === "CONSENSUS" ? "#00aaff"
    : fusion.status === "PARTIAL" ? "#ffb800" : "#ff2020";
  return (
    <div style={{
      border: `1px solid ${statusColor}40`, borderRadius: 8,
      padding: 20, background: `${statusColor}06`,
      position: "relative", overflow: "hidden",
    }}>
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: 1,
        background: `linear-gradient(90deg, transparent, ${statusColor}, transparent)`,
      }} />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ color: statusColor, fontFamily: "monospace", fontSize: 10, letterSpacing: 3 }}>
            SOVEREIGN FUSION
          </span>
          <span style={{
            background: statusColor, color: "#000",
            padding: "2px 8px", borderRadius: 2,
            fontFamily: "monospace", fontSize: 9, letterSpacing: 2, fontWeight: 700,
          }}>
            {fusion.status}
          </span>
        </div>
        <span style={{ color: statusColor, fontFamily: "monospace", fontSize: 16, fontWeight: 700 }}>
          {confidence}%
        </span>
      </div>
      <div style={{ marginBottom: 14 }}>
        <div style={{ height: 2, background: "#111", borderRadius: 1, marginBottom: 4 }}>
          <div style={{
            height: "100%", width: `${confidence}%`,
            background: `linear-gradient(90deg, ${statusColor}80, ${statusColor})`,
            borderRadius: 1, transition: "width 1s ease",
          }} />
        </div>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <span style={{ color: "#333", fontSize: 9, fontFamily: "monospace" }}>CONFIDENCE</span>
          <span style={{ color: "#333", fontSize: 9, fontFamily: "monospace" }}>{fusion.queens_active}/4 LINEAGES</span>
        </div>
      </div>
      <div style={{
        background: `${statusColor}10`,
        border: `1px solid ${statusColor}30`,
        borderLeft: `4px solid ${statusColor}`,
        borderRadius: 6, padding: "16px 20px", marginTop: 8,
      }}>
        <div style={{ color: statusColor, fontFamily: "monospace", fontSize: 9, letterSpacing: 3, marginBottom: 8 }}>
          SOVEREIGN VERDICT
        </div>
        <p style={{
          color: "#e0e0e0", fontSize: 14, lineHeight: 1.9,
          fontFamily: "Georgia, serif", margin: 0, fontWeight: "normal",
        }}>
          {fusion.fusion_answer}
        </p>
      </div>
    </div>
  );
}

function ProbabilityLandscape({ landscape }) {
  if (!landscape || !landscape.length) return null;
  return (
    <div style={{ marginTop: 16 }}>
      <div style={{ color: "#444", fontFamily: "monospace", fontSize: 9, letterSpacing: 3, marginBottom: 10 }}>
        PROBABILITY LANDSCAPE
      </div>
      {landscape.map((item, i) => (
        <div key={i} style={{ marginBottom: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
            <span style={{ color: "#888", fontSize: 10, fontFamily: "Georgia, serif" }}>{item.option}</span>
            <span style={{ color: "#00e87a", fontFamily: "monospace", fontSize: 10 }}>{item.probability}%</span>
          </div>
          <div style={{ height: 1, background: "#111" }}>
            <div style={{
              height: "100%", width: `${item.probability}%`,
              background: i === 0 ? "#00e87a" : i === 1 ? "#00aaff" : "#444",
              transition: "width 1s ease",
            }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function SovereignOracle() {
  const [query, setQuery] = useState("");
  const [domain, setDomain] = useState("wealth");
  const [urgency, setUrgency] = useState("BLUE");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showQueens, setShowQueens] = useState(true);
  const [dots, setDots] = useState("");

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setDots(d => d.length >= 3 ? "" : d + ".");
      }, 500);
      return () => clearInterval(interval);
    }
  }, [loading]);

  const handleQuery = async () => {
    if (!query.trim() || loading) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("http://sovereign-oracle.local:8002/oracle/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query.trim(), domain, urgency_override: urgency }),
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Unable to reach Sovereign Oracle backend." });
    } finally {
      setLoading(false);
    }
  };

  const urgencyConfig = URGENCY_CONFIG[urgency];

  return (
    <div style={{ minHeight: "100vh", background: "#050505", color: "#e0e0e0", fontFamily: "Georgia, serif" }}>
      <style>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        @keyframes pulse { 0%,100%{transform:scale(1);opacity:0.4} 50%{transform:scale(2.5);opacity:0} }
        @keyframes bounce { 0%,80%,100%{transform:scale(0)} 40%{transform:scale(1)} }
        @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
        textarea:focus { outline: none; }
        button { cursor: pointer; border: none; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
      `}</style>

      <div style={{
        borderBottom: "1px solid #111", padding: "20px 32px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        position: "sticky", top: 0, background: "#050505", zIndex: 100,
      }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 900, letterSpacing: 6, color: "#e0e0e0", fontFamily: "Georgia, serif" }}>
            SOVEREIGN ORACLE
          </h1>
          <div style={{ color: "#333", fontFamily: "monospace", fontSize: 9, letterSpacing: 4, marginTop: 2 }}>
            JOEL BALBIEN · TIER 4 · FOUR LINEAGE FUSION
          </div>
        </div>
        <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
          {QUEENS.map(q => (
            <div key={q.id} style={{ display: "flex", alignItems: "center", gap: 5 }}>
              <PulsingOrb color={q.color} size={6} active={!!result && !loading} />
              <span style={{ color: "#333", fontFamily: "monospace", fontSize: 8, letterSpacing: 2 }}>{q.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "32px 24px" }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {DOMAINS.map(d => (
            <button key={d.id} onClick={() => setDomain(d.id)} style={{
              padding: "6px 16px",
              background: domain === d.id ? "#111" : "transparent",
              border: `1px solid ${domain === d.id ? "#333" : "#1a1a1a"}`,
              borderRadius: 4, color: domain === d.id ? "#e0e0e0" : "#444",
              fontFamily: "monospace", fontSize: 9, letterSpacing: 3,
            }}>
              {d.icon} {d.label}
            </button>
          ))}
        </div>

        <div style={{ display: "flex", gap: 8, marginBottom: 24, alignItems: "center" }}>
          {Object.entries(URGENCY_CONFIG).map(([key, val]) => (
            <button key={key} onClick={() => setUrgency(key)} style={{
              padding: "4px 12px",
              background: urgency === key ? `${val.color}15` : "transparent",
              border: `1px solid ${urgency === key ? val.color + "60" : "#1a1a1a"}`,
              borderRadius: 3, color: urgency === key ? val.color : "#333",
              fontFamily: "monospace", fontSize: 8, letterSpacing: 2,
              boxShadow: urgency === key ? `0 0 12px ${val.glow}` : "none",
            }}>
              {key}
            </button>
          ))}
          <span style={{ marginLeft: "auto", color: urgencyConfig.color, fontFamily: "monospace", fontSize: 8, letterSpacing: 3 }}>
            {urgencyConfig.label} · {urgencyConfig.cycles} CYCLE{urgencyConfig.cycles > 1 ? "S" : ""}
          </span>
        </div>

        <div style={{
          border: `1px solid ${loading ? urgencyConfig.color + "40" : "#1e1e1e"}`,
          borderRadius: 8, overflow: "hidden",
          boxShadow: loading ? `0 0 20px ${urgencyConfig.glow}` : "none",
          marginBottom: 12,
        }}>
          <textarea
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleQuery(); }}
            placeholder="Address the Oracle..."
            rows={4}
            style={{
              width: "100%", background: "#080808", color: "#d0d0d0",
              padding: "16px 20px", fontFamily: "Georgia, serif",
              fontSize: 14, lineHeight: 1.7, resize: "none", border: "none",
            }}
          />
          <div style={{
            background: "#080808", padding: "10px 16px",
            display: "flex", justifyContent: "space-between", alignItems: "center",
            borderTop: "1px solid #111",
          }}>
            <span style={{ color: "#2a2a2a", fontFamily: "monospace", fontSize: 8, letterSpacing: 2 }}>CMD+ENTER TO INVOKE</span>
            <button onClick={handleQuery} disabled={loading || !query.trim()} style={{
              padding: "8px 24px",
              background: loading ? "transparent" : urgencyConfig.color,
              color: loading ? urgencyConfig.color : "#000",
              border: `1px solid ${urgencyConfig.color}`,
              borderRadius: 4, fontFamily: "monospace", fontSize: 9,
              letterSpacing: 3, fontWeight: 700,
              opacity: !query.trim() ? 0.3 : 1,
            }}>
              {loading ? `INVOKING${dots}` : "INVOKE"}
            </button>
          </div>
        </div>

        {result && !result.error && (
          <div style={{ animation: "fadeIn 0.6s ease" }}>
            <FusionDisplay fusion={result.fusion} />
            <ProbabilityLandscape landscape={result.probability_landscape} />
            <button onClick={() => setShowQueens(s => !s)} style={{
              background: "transparent", border: "1px solid #1e1e1e",
              borderRadius: 4, color: "#444", fontFamily: "monospace",
              fontSize: 9, letterSpacing: 3, padding: "6px 14px", margin: "16px 0",
            }}>
              {showQueens ? "HIDE" : "SHOW"} LINEAGE RESPONSES
            </button>
            {showQueens && (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                {QUEENS.map(queen => (
                  <QueenCard key={queen.id} queen={queen}
                    response={result.queen_responses?.[queen.id]}
                    active={result.queen_responses?.[queen.id] && !result.queen_responses[queen.id].toLowerCase().includes("unavailable")}
                    loading={false}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {result?.error && (
          <div style={{ border: "1px solid #ff202040", borderRadius: 8, padding: 20, color: "#ff6060", fontFamily: "monospace", fontSize: 11 }}>
            {result.error}
          </div>
        )}
      </div>
    </div>
  );
}
