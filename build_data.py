#!/usr/bin/env python3
"""Merge agent-produced data_src files into the final question bank: data/questions.json.

Run:  python3 build_data.py
Idempotent — rebuilds data/questions.json from scratch each time.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "data_src")
OUT = os.path.join(HERE, "data")

FOUND_DOMAINS = {
    1: ("Agent architecture and orchestration", 27),
    2: ("Tool design and MCP integration", 18),
    3: ("Claude Code configuration and workflows", 20),
    4: ("Prompt engineering and structured output", 20),
    5: ("Context management and reliability", 15),
}
PRO_DOMAINS = {
    1: ("Solution Design & Architecture", 17),
    2: ("Claude Models, Prompting & Context Engineering", 13),
    3: ("Integration", 19),
    4: ("Evaluation, Testing & Optimization", 16),
    5: ("Governance, Safety & Risk Management", 14),
    6: ("Stakeholder Communication & Lifecycle Management", 14),
    7: ("Developer Productivity & Operational Enablement", 7),
}
# Blueprint item counts for the Professional mock exam.
# Matches the current official 70-question CCAR-P blueprint (see pro_ccarp70.json).
PRO_PLAN = {1: 12, 2: 9, 3: 13, 4: 11, 5: 10, 6: 10, 7: 5}
PRO_MINUTES = 130


def load(name, required=True):
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        if required:
            sys.exit(f"missing required file: {path}")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    bank = []

    # ---------- Foundations ----------
    raw = load("found_bank_raw.json")
    review = load("found_review.json", required=False) or {}
    tagging = review.get("domain_tagging", {})

    # scenario -> default domain fallback when tagging is missing
    scen_default = {
        "Multi-agent Research System": 1,
        "Customer Support Agent": 1,
        "Code Generation with Claude Code": 3,
        "Claude Code for Continuous Integration": 3,
    }

    for q in raw:
        dom = tagging.get(q["id"]) or scen_default.get(q.get("scenario", ""), 1)
        text = q.get("situation", "").strip()
        if q.get("question"):
            text = (text + "\n\n" + q["question"].strip()) if text else q["question"].strip()
        name, weight = FOUND_DOMAINS[dom]
        bank.append({
            "id": q["id"],
            "cert": "foundations",
            "domain_id": dom,
            "domain": name,
            "weight": weight,
            "scenario": q.get("scenario", ""),
            "type": "single",
            "text": text,
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q.get("explanation", ""),
        })

    for q in review.get("extra_questions", []):
        dom = q.get("domain_id") or 1
        name, weight = FOUND_DOMAINS[dom]
        text = q.get("situation", "").strip()
        if q.get("question"):
            text = (text + "\n\n" + q["question"].strip()) if text else q["question"].strip()
        bank.append({
            "id": q["id"],
            "cert": "foundations",
            "domain_id": dom,
            "domain": name,
            "weight": weight,
            "scenario": q.get("scenario", ""),
            "type": "single",
            "text": text,
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q.get("explanation", ""),
        })

    for q in load("found_authored.json", required=False) or []:
        dom = q.get("domain_id") or 1
        name, weight = FOUND_DOMAINS[dom]
        text = q.get("situation", "").strip()
        if q.get("question"):
            text = (text + "\n\n" + q["question"].strip()) if text else q["question"].strip()
        bank.append({
            "id": q["id"],
            "cert": "foundations",
            "domain_id": dom,
            "domain": name,
            "weight": weight,
            "scenario": q.get("scenario", ""),
            "type": "single",
            "text": text,
            "options": q["options"],
            "answer": q["answer"],
            "explanation": q.get("explanation", ""),
        })

    # ---------- Professional ----------
    # pro_ccarp70.json is the 70-question CCAR-P mock exam (Downloads/CCAR-P.pdf),
    # transcribed verbatim. Its questions use domain_id per the PDF's own sections.
    for fname in ("pro_d1_d2.json", "pro_d3_d4.json", "pro_d5_d7.json", "pro_ccarp70.json"):
        for q in load(fname, required=False) or []:
            dom = q.get("domain_id") or 1
            name, weight = PRO_DOMAINS.get(dom, (q.get("domain", "?"), q.get("weight", 0)))
            item = {
                "id": q["id"],
                "cert": "professional",
                "domain_id": dom,
                "domain": name,
                "weight": weight,
                "scenario": "",
                "type": q.get("type", "single"),
                "text": q.get("text", ""),
                "options": q.get("options", []),
                "answer": q.get("answer", []),
                "explanation": q.get("explanation", ""),
            }
            if q.get("source"):
                item["source"] = q["source"]
            if item["type"] == "multi":
                item["select"] = q.get("select", 2)
            if item["type"] == "matching":
                item["items"] = q.get("items", [])
            bank.append(item)

    # ---------- write ----------
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "questions.json"), "w", encoding="utf-8") as f:
        json.dump({
            "foundations_domains": {str(k): {"name": v[0], "weight": v[1]} for k, v in FOUND_DOMAINS.items()},
            "professional_domains": {str(k): {"name": v[0], "weight": v[1]} for k, v in PRO_DOMAINS.items()},
            "professional_plan": {str(k): v for k, v in PRO_PLAN.items()},
            "professional_plan_total": sum(PRO_PLAN.values()),
            "professional_minutes": PRO_MINUTES,
            "foundations_minutes": 90,
            "foundations_plan_total": 60,
            "questions": bank,
        }, f, indent=1, ensure_ascii=False)

    # study notes (from the Foundations review agent), if present
    if review.get("domain_notes"):
        with open(os.path.join(OUT, "notes.json"), "w", encoding="utf-8") as f:
            json.dump(review["domain_notes"], f, indent=1, ensure_ascii=False)
        print(f"Wrote study notes ({len(review['domain_notes'])} domains) -> data/notes.json")

    # summary
    from collections import Counter
    c = Counter((q["cert"], q["domain_id"]) for q in bank)
    tot = Counter(q["cert"] for q in bank)
    print(f"Wrote {len(bank)} questions -> data/questions.json")
    for cert in ("foundations", "professional"):
        print(f"\n{cert.upper()}: {tot[cert]} questions")
        for d in sorted(k for (cc, k) in c if cc == cert):
            ds = FOUND_DOMAINS if cert == "foundations" else PRO_DOMAINS
            print(f"  D{d} {ds[d][0][:52]:<52} {c[(cert, d)]}")


if __name__ == "__main__":
    main()
