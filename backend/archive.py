"""
Sovereign Council Deliberation Archive
Archive Voice — Advisory, never determinative
Custodial authority: Sovereign Joel Balbien
"""
import sqlite3, json, os, time, hashlib
from datetime import datetime

ARCHIVE_PATH = os.path.join(os.path.dirname(__file__), "archive.db")

def init_archive():
    conn = sqlite3.connect(ARCHIVE_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS verdicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            unix_time REAL NOT NULL,
            query TEXT NOT NULL,
            domain TEXT NOT NULL,
            verdict TEXT NOT NULL,
            emergent_insight TEXT,
            actionable_wisdom TEXT,
            unresolved_tensions TEXT,
            status TEXT,
            confidence REAL,
            queens_active INTEGER,
            zkp_short TEXT,
            query_hash TEXT UNIQUE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS covenant_amendments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            commandment_num TEXT NOT NULL,
            title TEXT NOT NULL,
            full_text TEXT NOT NULL,
            ratified_by TEXT DEFAULT 'Unanimous Council'
        )
    """)
    conn.commit()
    conn.close()

def save_verdict(query, domain, fusion, queen_responses, zkp):
    """Save a Council verdict to the archive."""
    init_archive()
    query_hash = hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:16]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    unix_time = time.time()

    verdict_text = fusion.get("fusion_answer", "")
    status = fusion.get("status", "")
    confidence = fusion.get("confidence", 0)
    queens_active = fusion.get("queens_active", 0)
    zkp_short = zkp.get("zkp_short", "") if zkp else ""

    # Extract structured sections from verdict
    emergent = ""
    wisdom = ""
    tensions = ""

    lines = verdict_text.split("\n")
    current_section = None
    for line in lines:
        if "EMERGENT INSIGHT" in line.upper():
            current_section = "emergent"
        elif "ACTIONABLE WISDOM" in line.upper():
            current_section = "wisdom"
        elif "UNRESOLVED TENSION" in line.upper():
            current_section = "tensions"
        elif current_section == "emergent" and line.strip():
            emergent += line + "\n"
        elif current_section == "wisdom" and line.strip():
            wisdom += line + "\n"
        elif current_section == "tensions" and line.strip():
            tensions += line + "\n"

    try:
        conn = sqlite3.connect(ARCHIVE_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO verdicts
            (timestamp, unix_time, query, domain, verdict,
             emergent_insight, actionable_wisdom, unresolved_tensions,
             status, confidence, queens_active, zkp_short, query_hash)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (timestamp, unix_time, query, domain, verdict_text,
              emergent.strip(), wisdom.strip(), tensions.strip(),
              status, confidence, queens_active, zkp_short, query_hash))
        conn.commit()
        conn.close()
        return {"saved": True, "timestamp": timestamp, "hash": query_hash}
    except Exception as e:
        return {"saved": False, "error": str(e)}

def get_archive_counsel(query, domain, limit=3):
    """
    Retrieve relevant prior verdicts as Archive Voice counsel.
    Called only in Phase III — advisory, never determinative.
    """
    init_archive()
    try:
        conn = sqlite3.connect(ARCHIVE_PATH)
        c = conn.cursor()

        # Find relevant verdicts by domain and keyword overlap
        query_words = set(query.lower().split())
        c.execute("""
            SELECT timestamp, query, domain, emergent_insight,
                   unresolved_tensions, status, confidence
            FROM verdicts
            WHERE domain = ? OR domain = 'general'
            ORDER BY unix_time DESC
            LIMIT 20
        """, (domain,))
        rows = c.fetchall()
        conn.close()

        if not rows:
            return None

        # Score by keyword overlap
        scored = []
        for row in rows:
            prior_words = set(row[1].lower().split())
            overlap = len(query_words & prior_words)
            scored.append((overlap, row))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:limit]

        if not top or top[0][0] == 0:
            # No keyword overlap — use most recent by domain
            top = [(0, rows[0])] if rows else []

        if not top:
            return None

        counsel = "## ARCHIVE COUNSEL\n"
        counsel += "*The following is drawn from prior Council deliberations. "
        counsel += "It is advisory only — one voice among living voices, "
        counsel += "never settled precedent. Custodial authority: Sovereign Joel Balbien.*\n\n"

        for score, row in top:
            ts, q, dom, insight, tensions, status, conf = row
            counsel += f"**Prior deliberation [{ts}] — Domain: {dom}**\n"
            counsel += f"Query: {q[:100]}...\n" if len(q) > 100 else f"Query: {q}\n"
            if insight:
                counsel += f"Emergent insight: {insight[:300]}\n"
            if tensions:
                counsel += f"Unresolved tensions: {tensions[:300]}\n"
            counsel += "\n"

        return counsel

    except Exception as e:
        return None

def get_all_verdicts(limit=50):
    """Return all archived verdicts for the /archive endpoint."""
    init_archive()
    try:
        conn = sqlite3.connect(ARCHIVE_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, timestamp, query, domain, status,
                   confidence, queens_active, emergent_insight,
                   actionable_wisdom, unresolved_tensions, zkp_short
            FROM verdicts
            ORDER BY unix_time DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()
        cols = ["id","timestamp","query","domain","status",
                "confidence","queens_active","emergent_insight",
                "actionable_wisdom","unresolved_tensions","zkp_short"]
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        return []

def get_verdict_by_id(verdict_id):
    """Return full verdict text by ID."""
    init_archive()
    try:
        conn = sqlite3.connect(ARCHIVE_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM verdicts WHERE id = ?", (verdict_id,))
        row = c.fetchone()
        conn.close()
        if row:
            cols = ["id","timestamp","unix_time","query","domain","verdict",
                    "emergent_insight","actionable_wisdom","unresolved_tensions",
                    "status","confidence","queens_active","zkp_short","query_hash"]
            return dict(zip(cols, row))
        return None
    except Exception as e:
        return None

def get_archive_stats():
    """Return archive statistics."""
    init_archive()
    try:
        conn = sqlite3.connect(ARCHIVE_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM verdicts")
        total = c.fetchone()[0]
        c.execute("SELECT domain, COUNT(*) FROM verdicts GROUP BY domain ORDER BY COUNT(*) DESC")
        by_domain = {row[0]: row[1] for row in c.fetchall()}
        c.execute("SELECT AVG(confidence) FROM verdicts")
        avg_conf = c.fetchone()[0] or 0
        c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM verdicts")
        dates = c.fetchone()
        conn.close()
        return {
            "total_verdicts": total,
            "by_domain": by_domain,
            "avg_confidence": round(avg_conf, 3),
            "first_verdict": dates[0],
            "latest_verdict": dates[1]
        }
    except Exception as e:
        return {"error": str(e)}

# Initialize on import
init_archive()
