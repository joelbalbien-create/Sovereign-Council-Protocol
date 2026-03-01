#!/usr/bin/env python3
"""
Sovereign Council Protocol — EVAL Suite
Inventor: Joel Abe Balbien, Ph.D.
Tests all patent claims, authentication, accuracy, ethics, and consensus quality.
"""

import json
import time
import requests
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load token from backend .env
load_dotenv(os.path.expanduser("~/sovereign-council/backend/.env"))
VALID_TOKEN = os.getenv("API_TOKEN", "")
BASE_URL = "http://localhost:8002"

# Colors for terminal output
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
GOLD   = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def print_header():
    print(f"\n{BOLD}{GOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GOLD}  SOVEREIGN COUNCIL PROTOCOL — EVAL SUITE{RESET}")
    print(f"{BOLD}{GOLD}  Inventor: Joel Abe Balbien, Ph.D.{RESET}")
    print(f"{BOLD}{GOLD}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BOLD}{GOLD}{'='*60}{RESET}\n")

def run_test(test):
    token = VALID_TOKEN if test["token"] == "valid" else test["token"]
    headers = {
        "Content-Type": "application/json",
        "x-api-token": token
    }
    payload = {
        "query": test["query"],
        "domain": test["domain"],
        "urgency_override": test["urgency"]
    }

    start = time.time()
    try:
        timeout = test.get("timeout", 90)
        response = requests.post(
            f"{BASE_URL}/oracle/query",
            headers=headers,
            json=payload,
            timeout=timeout
        )
        latency = time.time() - start
        http_status = response.status_code

        if http_status != 200:
            data = {}
        else:
            data = response.json()

    except Exception as e:
        return {
            "id": test["id"],
            "category": test["category"],
            "description": test["description"],
            "passed": False,
            "reason": f"Connection error: {str(e)}",
            "latency": 0
        }

    latency = time.time() - start
    condition = test["pass_condition"]
    passed = False
    reason = ""

    # Evaluate pass condition
    if condition == "http_status == 401":
        passed = http_status == 401
        reason = f"HTTP {http_status}"

    elif condition == "http_status == 200":
        passed = http_status == 200
        reason = f"HTTP {http_status}"

    elif condition == "keywords_present":
        if http_status != 200:
            passed = False
            reason = f"HTTP {http_status}"
        else:
            verdict = data.get("fusion", {}).get("fusion_answer", "").lower()
            queens = str(data.get("queen_responses", {})).lower()
            full_text = verdict + queens
            keywords = test.get("expected_keywords", [])
            found = [k for k in keywords if k.lower() in full_text]
            passed = len(found) > 0
            reason = f"Found: {found}" if found else f"Missing all keywords: {keywords}"

    elif condition == "forbidden_keywords_absent":
        if http_status != 200:
            passed = True  # If refused entirely, that's a pass
            reason = f"HTTP {http_status} — request declined"
        else:
            verdict = data.get("fusion", {}).get("fusion_answer", "").lower()
            forbidden = test.get("forbidden_keywords", [])
            found = [k for k in forbidden if k.lower() in verdict]
            passed = len(found) == 0
            reason = f"Clean — no forbidden content" if passed else f"Found forbidden: {found}"

    elif condition == "queens_active == 4 and status in expected_consensus":
        if http_status != 200:
            passed = False
            reason = f"HTTP {http_status}"
        else:
            fusion = data.get("fusion", {})
            queens_active = fusion.get("queens_active", 0)
            status = fusion.get("status", "")
            expected = test.get("expected_consensus", [])
            passed = queens_active == 4 and status in expected
            reason = f"Queens: {queens_active}/4, Status: {status}"

    elif condition == "confidence >= 0.75":
        if http_status != 200:
            passed = False
            reason = f"HTTP {http_status}"
        else:
            confidence = data.get("fusion", {}).get("confidence", 0)
            min_conf = test.get("min_confidence", 0.75)
            passed = confidence >= min_conf
            reason = f"Confidence: {confidence:.1%}"

    elif condition == "latency <= 45":
        passed = latency <= test.get("max_seconds", 45)
        reason = f"Latency: {latency:.1f}s"

    elif condition == "metabolic_score_present":
        passed = "metabolic_score" in data and data["metabolic_score"] is not None
        reason = "Metabolic score present" if passed else "Metabolic score missing"

    elif condition == "zkp_proof_present":
        passed = "zkp_proof" in data and data["zkp_proof"] is not None
        reason = "ZKP proof present" if passed else "ZKP proof missing"

    elif condition == "patent_compliance_present":
        passed = "patent_compliance" in data and data["patent_compliance"] is not None
        reason = "Patent compliance present" if passed else "Patent compliance missing"

    return {
        "id": test["id"],
        "category": test["category"],
        "description": test["description"],
        "passed": passed,
        "reason": reason,
        "latency": round(latency, 2)
    }

def print_result(result):
    icon = f"{GREEN}✅{RESET}" if result["passed"] else f"{RED}❌{RESET}"
    status = f"{GREEN}PASS{RESET}" if result["passed"] else f"{RED}FAIL{RESET}"
    print(f"  {icon} [{result['id']}] {result['description']}")
    print(f"     {status} — {result['reason']} ({result['latency']}s)\n")

def save_report(results, summary):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.expanduser("~/sovereign-council/eval/reports")
    os.makedirs(report_dir, exist_ok=True)

    # JSON report
    report = {
        "timestamp": timestamp,
        "summary": summary,
        "results": results
    }
    json_path = f"{report_dir}/eval_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # Human readable text report
    txt_path = f"{report_dir}/eval_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("SOVEREIGN COUNCIL PROTOCOL — EVAL REPORT\n")
        f.write(f"Inventor: Joel Abe Balbien, Ph.D.\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write(f"SUMMARY\n")
        f.write(f"Total:  {summary['total']}\n")
        f.write(f"Passed: {summary['passed']}\n")
        f.write(f"Failed: {summary['failed']}\n")
        f.write(f"Score:  {summary['score']:.1%}\n\n")
        f.write("RESULTS BY CATEGORY\n")
        f.write("-"*40 + "\n")
        for cat, cat_results in summary["by_category"].items():
            f.write(f"\n{cat}\n")
            for r in cat_results:
                status = "PASS" if r["passed"] else "FAIL"
                f.write(f"  [{status}] {r['id']} — {r['description']}\n")
                f.write(f"         {r['reason']} ({r['latency']}s)\n")

    print(f"\n{BLUE}Reports saved:{RESET}")
    print(f"  JSON: {json_path}")
    print(f"  TEXT: {txt_path}")
    return txt_path

def main():
    print_header()

    # Check backend is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=3)
    except:
        try:
            requests.get(f"{BASE_URL}/docs", timeout=3)
        except:
            print(f"{RED}❌ Backend not running at {BASE_URL}{RESET}")
            print(f"   Start it with: cd ~/sovereign-council/backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8002")
            sys.exit(1)

    # Load test cases
    cases_path = os.path.join(os.path.dirname(__file__), "test_cases.json")
    with open(cases_path) as f:
        test_data = json.load(f)

    tests = test_data["test_cases"]
    print(f"{BLUE}Running {len(tests)} tests...{RESET}\n")

    results = []
    by_category = {}

    # Group by category
    for test in tests:
        cat = test["category"]
        if cat not in by_category:
            by_category[cat] = []
            print(f"{BOLD}{GOLD}── {cat} ──{RESET}")

        result = run_test(test)
        results.append(result)
        by_category[cat].append(result)
        print_result(result)

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    score = passed / total if total > 0 else 0

    print(f"{BOLD}{GOLD}{'='*60}{RESET}")
    print(f"{BOLD}  EVAL COMPLETE{RESET}")
    print(f"  Total:  {total}")
    print(f"  Passed: {GREEN}{passed}{RESET}")
    print(f"  Failed: {RED}{failed}{RESET}")
    print(f"  Score:  {GREEN if score >= 0.8 else RED}{score:.1%}{RESET}")

    # Category breakdown
    print(f"\n{BOLD}  BY CATEGORY:{RESET}")
    for cat, cat_results in by_category.items():
        cat_passed = sum(1 for r in cat_results if r["passed"])
        cat_total = len(cat_results)
        color = GREEN if cat_passed == cat_total else YELLOW if cat_passed > 0 else RED
        print(f"  {color}{cat}: {cat_passed}/{cat_total}{RESET}")

    print(f"{BOLD}{GOLD}{'='*60}{RESET}\n")

    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "score": score,
        "by_category": by_category
    }

    save_report(results, summary)

    # Exit with error code if tests failed
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
