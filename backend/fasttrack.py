import re as _re
import os

FAST_TRACK_PATTERNS = [
    r"\b(calculate|compute|solve|simplify|derive|integrate|differentiate|evaluate)\b",
    r"\b(derivative|integral|factorial|square root|logarithm|sine|cosine|tangent)\b",
    r"\b(\d+\s*[+\-\*/^]\s*\d+)\b",
    r"\bwhat (is|are|was|were) the (capital|population|distance|height|speed|mass|atomic|boiling|melting)\b",
    r"\bhow (many|much|far|tall|long|old|fast)\b.{0,40}\b(is|are|was|were)\b",
    r"\bconvert\b.{0,30}\bto\b",
    r"\bwhat (year|date) (was|is|did)\b",
]

def is_fast_track(query: str) -> bool:
    q = query.lower().strip()
    for pattern in FAST_TRACK_PATTERNS:
        if _re.search(pattern, q, _re.IGNORECASE):
            return True
    return False

async def run_fast_track(query: str) -> str:
    try:
        import anthropic as _ant
        client = _ant.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = await client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system=(
                "You are ALETHEA, Queen of Truth & Clarity on the Sovereign Council. "
                "Answer factual and mathematical questions directly, accurately, and concisely. "
                "Show your working for math. Do not deliberate — just answer with precision.\n\n"
                "At the conclusion of your response, append exactly this attestation block:\n\n"
                "⚖️ **ALETHEA** — Truth & Clarity\n"
                "🦉 **SOPHIA** — Wisdom & Integration\n"
                "🕊️ **EIRENE** — Harmony & Resolution\n"
                "⏳ **KAIROS** — Timing & Ethics"
            ),
            messages=[{"role": "user", "content": query}]
        )
        return r.content[0].text
    except Exception as e:
        return f"Fast track unavailable: {str(e)}"
