#!/usr/bin/env python3
"""
Claude Certified Architect — Exam Prep (terminal edition)
Covers: Foundations + Professional

Run:  python3 exam_prep.py
"""
import json
import os
import random
import sys
import textwrap
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "questions.json")
NOTES = os.path.join(HERE, "data", "notes.json")
HISTORY = os.path.join(HERE, "results", "history.jsonl")

# ---------------------------------------------------------------- ansi ----

def _color_on():
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()

C = _color_on()

def ansi(code, s):
    return f"\033[{code}m{s}\033[0m" if C else s

BOLD = lambda s: ansi("1", s)
DIM = lambda s: ansi("2", s)
GREEN = lambda s: ansi("32", s)
RED = lambda s: ansi("31", s)
YELLOW = lambda s: ansi("33", s)
CYAN = lambda s: ansi("36", s)
MAGENTA = lambda s: ansi("35", s)

WIDTH = 100

def wrap(text, indent=0):
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        out.extend(textwrap.wrap(para, width=WIDTH - indent,
                                 initial_indent=" " * indent,
                                 subsequent_indent=" " * indent))
    return "\n".join(out)

def hr(char="-"):
    print(DIM(char * WIDTH))

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def pause(msg="Press Enter to continue..."):
    try:
        input(DIM(msg))
    except EOFError:
        sys.exit(0)

def ask(msg, default=None):
    suffix = f" [{default}]" if default else ""
    try:
        v = input(f"{msg}{suffix} > ").strip()
    except EOFError:
        print()
        sys.exit(0)
    return v or (default or "")

def ask_choice(msg, choices, default=None):
    """choices: list of (key, label). Returns key or None."""
    for k, label in choices:
        print(f"  {BOLD(k)}. {label}")
    while True:
        v = ask(msg, default).lower()
        keys = [k.lower() for k, _ in choices]
        if v in keys:
            return [k for k, _ in choices][keys.index(v)]
        print(RED(f"  Please enter one of: {', '.join(k for k, _ in choices)}"))

# ---------------------------------------------------------------- data ----

def load_bank():
    if not os.path.exists(DATA):
        sys.exit(f"Question bank not found at {DATA}.\n"
                 f"Run 'python3 build_data.py' first.")
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def record_result(entry):
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# ------------------------------------------------------- review reports ---

REVIEWS_DIR = os.path.join(HERE, "results", "reviews")

FOUND_STUDY = {
    1: "Study guide Part I — Ch. 3 (Agent SDK, coordinator/subagents, hooks), Ch. 8 (task decomposition), Ch. 9 (escalation & human-in-the-loop), Ch. 10 (error handling in multi-agent systems); then Part II Domain 1 notes.",
    2: "Study guide Part I — Ch. 2 (tool_use, tool_choice, tool descriptions, JSON schemas) and Ch. 4 (MCP servers, isError, resources, .mcp.json); then Part II Domain 2 notes.",
    3: "Study guide Part I — Ch. 5 (CLAUDE.md hierarchy, rules, commands, skills, planning mode, /compact, /memory, CI/CD headless mode, sessions) and Ch. 13 (built-in tools); then Part II Domain 3 notes.",
    4: "Study guide Part I — Ch. 6 (few-shot, explicit criteria, chaining, interview pattern, validation/retry, self-correction), Ch. 2.4 (JSON schema design), Ch. 7 (Message Batches API); then Part II Domain 4 notes.",
    5: "Study guide Part I — Ch. 11 (context management in production), Ch. 12 (provenance), Ch. 9-10 (escalation & error handling); then Part II Domain 5 notes.",
}
PRO_STUDY = {
    1: "Revisit solution design trade-offs: fixed workflows vs autonomous agents vs multi-agent systems, when to decompose, routing/supervisor patterns, build-vs-buy decisions.",
    2: "Revisit model selection (cost/latency/capability trade-offs), prompt-prefix caching rules, context engineering, and structured-output strategies.",
    3: "Revisit integration architecture: MCP design and tool sprawl, API patterns, latency/caching reasoning, and reliability of external integrations.",
    4: "Revisit evaluation design: golden datasets, LLM-as-judge calibration, offline vs online testing, launch thresholds, and optimisation loops.",
    5: "Revisit governance: bias/fairness incidents, guardrails, auditability, compliance in regulated settings, and risk escalation.",
    6: "Revisit stakeholder management: expectation setting, evidence-based communication, change control, lifecycle phases (discovery→design→handoff→monitoring).",
    7: "Revisit developer-productivity patterns: code review with AI, CI/CD integration, rollouts and enablement for engineering teams.",
}

def write_review_report(cert, mode, results, minutes_used=None, minutes_limit=None, focus=None):
    """results: list of (question, answer_or_None, correct_bool). Returns the report path."""
    os.makedirs(REVIEWS_DIR, exist_ok=True)
    ts = datetime.now()
    total = len(results)
    correct = sum(1 for _, _, ok in results if ok)
    skipped = sum(1 for _, ans, _ in results if ans is None)
    pct = 100 * correct / total if total else 0

    by_dom = {}
    for q, ans, ok in results:
        d = by_dom.setdefault((q["domain_id"], q["domain"]), [0, 0])
        d[1] += 1
        if ok:
            d[0] += 1
    weak = [(did, name, got, of) for (did, name), (got, of) in by_dom.items()
            if (100 * got / of) < 75]
    weak.sort(key=lambda w: w[2] / w[3])

    title_cert = "Foundations" if cert == "foundations" else "Professional"
    L = []
    L.append(f"# Performance Review — {title_cert} {'Mock Exam' if mode == 'mock' else 'Practice Session'}")
    L.append("")
    L.append(f"- **Date:** {ts.strftime('%Y-%m-%d %H:%M')}")
    L.append(f"- **Mode:** {'Timed mock exam' if mode == 'mock' else 'Practice session'}"
             + (f" · focus: {focus}" if focus else ""))
    L.append(f"- **Score:** **{correct}/{total} ({pct:.1f}%)** · skipped: {skipped}")
    if minutes_used is not None:
        L.append(f"- **Time used:** {minutes_used:.1f} min of {minutes_limit} min")
    if cert == "foundations":
        scaled = 100 + 9 * pct
        L.append(f"- **Scaled estimate:** ≈{scaled:.0f}/1000 (passing = 720) — "
                 + ("**PASS (estimated)**" if scaled >= 720 else "**below passing (estimated)**"))
    else:
        L.append(f"- **Benchmark:** ≥75% overall and in every domain — "
                 + ("**ON TRACK**" if pct >= 75 and not weak else "**NEEDS WORK in the domains below**"))
    L.append("")

    L.append("## Domain breakdown")
    L.append("")
    L.append("| Domain | Score | % | Status |")
    L.append("|---|---|---|---|")
    for (did, name), (got, of) in sorted(by_dom.items()):
        dp = 100 * got / of
        status = "✅ solid" if dp >= 75 else ("⚠️ borderline" if dp >= 60 else "❌ weak")
        L.append(f"| D{did} {name} | {got}/{of} | {dp:.0f}% | {status} |")
    L.append("")

    L.append("## Areas to read up on")
    L.append("")
    if not weak:
        L.append("All domains are at or above the 75% target. To consolidate:")
        L.append("")
        L.append("- Re-run a mock exam on a different day to confirm retention.")
        L.append("- Skim the explanations of any question you got right but guessed on.")
    else:
        L.append("Prioritise these domains (weakest first):")
        L.append("")
        study_map = FOUND_STUDY if cert == "foundations" else PRO_STUDY
        for did, name, got, of in weak:
            dp = 100 * got / of
            L.append(f"### {did}. {name} — {got}/{of} ({dp:.0f}%)")
            L.append("")
            L.append(f"- What to revisit: {study_map.get(did, 'Review the explanations below.')}")
            missed = [q for q, ans, ok in results if q["domain_id"] == did and not ok]
            ids = ", ".join(q["id"] for q in missed[:12])
            L.append(f"- Your missed questions: {ids}")
            L.append("")
    L.append("")

    L.append("## Missed & skipped questions — walkthrough")
    L.append("")
    missed = [(q, ans) for q, ans, ok in results if not ok]
    if not missed:
        L.append("Nothing missed — perfect run. 🎯")
    for q, ans in missed:
        L.append(f"### {q['id']} · {q['domain']}")
        L.append("")
        for para in q["text"].split("\n"):
            if para.strip():
                L.append(f"> {para.strip()}")
        L.append("")
        if q["type"] == "matching":
            your = ", ".join(f"{n}:{a}" for n, a in enumerate(ans, 1)) if ans else "— skipped —"
            right = ", ".join(f"{n}:{a}" for n, a in enumerate(q["answer"], 1))
            L.append(f"- **Your matches:** {your}")
            L.append(f"- **Correct matches:** {right}")
        else:
            yours = ", ".join(ans) if ans else "— skipped —"
            L.append(f"- **Your answer:** {yours}")
            L.append(f"- **Correct answer:** {', '.join(q['answer'])}")
        if q.get("explanation"):
            L.append(f"- **Explanation:** {q['explanation']}")
        L.append("")

    L.append("---")
    L.append(f"*Generated by exam_prep.py · {ts.isoformat(timespec='seconds')}*")

    path = os.path.join(REVIEWS_DIR, f"{ts.strftime('%Y-%m-%d_%H%M%S')}_{cert}_{mode}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return path

def load_history():
    if not os.path.exists(HISTORY):
        return []
    out = []
    with open(HISTORY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out

# ---------------------------------------------------------------- ui ------

BANNER = r"""
   ____ _                 _       ____          _            _       _
  / ___| | __ _ _   _  __| | ___ / ___|___   __| | ___ _ __ | | __ _| |_
 | |   | |/ _` | | | |/ _` |/ _ \ |   / _ \ / _` |/ _ \ '_ \| |/ _` | __|
 | |___| | (_| | |_| | (_| |  __/ |__| (_) | (_| |  __/ | | | | (_| | |_
  \____|_|\__,_|\__,_|\__,_|\___|\____\___/ \__,_|\___|_| |_|_|\__,_|\__|
"""

def banner():
    clear()
    print(CYAN(BANNER))
    print(BOLD("   Claude Certified Architect — Exam Prep"))
    print(DIM("   Foundations  ·  Professional    (Ctrl+C anytime to abort)"))
    print()

def main_menu():
    banner()
    print("  " + BOLD("PRACTICE"))
    print("    1. Foundations — practice session")
    print("    2. Professional — practice session")
    print()
    print("  " + BOLD("MOCK EXAMS (timed, real exam format)"))
    print("    3. Foundations — mock exam")
    print("    4. Professional — mock exam")
    print()
    print("  " + BOLD("STUDY"))
    print("    5. Domain study notes")
    print("    6. Practical exercises (hands-on drills)")
    print("    7. Exam formats, scope & prep plan")
    print("    8. My results history")
    print()
    print("    0. Exit")
    while True:
        v = ask("Choose", default="1").strip()
        if v in "123456780" and len(v) == 1:
            return v
        print(RED("  Enter a number from the menu."))

# ------------------------------------------------------------- practice ---

def pick_questions(bank, cert, dom_id=None, scen=None, count=None, seed=None):
    pool = [q for q in bank["questions"] if q["cert"] == cert]
    if dom_id:
        pool = [q for q in pool if q["domain_id"] == dom_id]
    if scen:
        pool = [q for q in pool if q["scenario"] == scen]
    rng = random.Random(seed) if seed is not None else random
    rng.shuffle(pool)
    if count:
        pool = pool[:count]
    return pool

def show_question(q, num, total, timer_str=""):
    print()
    head = f"Q{num}/{total}"
    tag = f" · {q['domain']}"
    if q.get("scenario"):
        tag += f" · {q['scenario']}"
    line = f"[{head}]{tag}"
    if timer_str:
        line = f"{timer_str}  " + line
    print(CYAN(BOLD(line)))
    hr()
    print(wrap(q["text"]))
    print()
    if q["type"] == "matching":
        for i, opt in enumerate(q["options"], 1):
            print(f"   {BOLD(str(i))}. {opt}")
        print()
        for i, item in enumerate(q["items"], 1):
            print(f"   {BOLD(f'[{i}])')} {wrap(item, indent=6).strip()}")
    else:
        for o in q["options"]:
            print(f"   {BOLD(o['key'])}. {wrap(o['text'], indent=5).strip()}")
    if q["type"] == "multi":
        print(DIM(f"   (select {q.get('select', 2)} answers)"))
    print()

class EarlySubmit(Exception):
    pass

def read_answer(q):
    """Returns a normalized answer (list of keys / list of option strings) or None to skip.
    Raises EarlySubmit when the user types q."""
    try:
        if q["type"] == "single":
            letters = [o["key"].lower() for o in q["options"]]
            v = ask("Your answer (" + "/".join(o["key"] for o in q["options"]) + ", s=skip, q=submit exam)").lower()
            if v in ("q", "quit", "submit"):
                raise EarlySubmit()
            if v in ("s", "skip", ""):
                return None
            if v in letters:
                return [v.upper()]
            print(RED("  Not a valid option — counted as skipped."))
            return None

        if q["type"] == "multi":
            n = q.get("select", 2)
            letters = [o["key"].lower() for o in q["options"]]
            v = ask(f"Your answers ({n} letters, e.g. 'bd', s=skip, q=submit)").lower().replace(",", "").replace(" ", "")
            if v in ("q", "quit", "submit"):
                raise EarlySubmit()
            if v in ("s", "skip", ""):
                return None
            picks = sorted(set(ch.upper() for ch in v))
            if all(p.lower() in letters for p in picks) and len(picks) == n:
                return picks
            print(RED(f"  Enter exactly {n} valid letters — counted as skipped."))
            return None

        if q["type"] == "matching":
            answers = []
            n_opts = len(q["options"])
            for i, item in enumerate(q["items"], 1):
                while True:
                    v = ask(f"  Match item {i} of {len(q['items'])} (1-{n_opts}, s=skip, q=submit)").lower()
                    if v in ("q", "quit", "submit"):
                        raise EarlySubmit()
                    if v in ("s", "skip"):
                        return None
                    if v.isdigit() and 1 <= int(v) <= n_opts:
                        answers.append(q["options"][int(v) - 1])
                        break
                    print(RED(f"  Enter a number 1-{n_opts}."))
            return answers
    except EOFError:
        return None

def grade(q, ans):
    if ans is None:
        return False
    if q["type"] == "matching":
        return list(ans) == list(q["answer"])
    return sorted(a.upper() for a in ans) == sorted(a.upper() for a in q["answer"])

def show_feedback(q, ans, correct):
    if ans is None:
        print(YELLOW("  Skipped."))
    elif correct:
        print(GREEN(BOLD("  ✔ Correct")))
    else:
        print(RED(BOLD("  ✘ Incorrect")))
        if q["type"] == "matching":
            print("  Correct matches:")
            for item, a in zip(q["items"], q["answer"]):
                print(f"    • {item[:70]} → {BOLD(a)}")
        else:
            print(f"  Correct answer: {BOLD(', '.join(q['answer']))}")
    if q.get("explanation"):
        print()
        print(wrap("Explanation: " + q["explanation"], indent=2))
    hr()

def practice_session(bank, cert):
    clear()
    title = "Foundations" if cert == "foundations" else "Professional"
    print(BOLD(f"\n  {title} — Practice Session\n"))
    doms = bank["foundations_domains"] if cert == "foundations" else bank["professional_domains"]

    choices = [("0", "All domains (mixed)")]
    for k in sorted(doms, key=int):
        choices.append((k, f"Domain {k}: {doms[k]['name']} ({doms[k]['weight']}%)"))
    scens = sorted({q["scenario"] for q in bank["questions"]
                    if q["cert"] == cert and q.get("scenario")})
    scen_pick = None
    if scens:
        choices.append(("s", "Practice by exam scenario…"))
    print("  Focus area:")
    pick = ask_choice("Choose", choices, default="0")
    dom_id = None
    if pick == "s":
        schoices = [(str(i + 1), s) for i, s in enumerate(scens)]
        sp = ask_choice("Scenario", schoices, default="1")
        scen_pick = scens[int(sp) - 1]
    elif pick != "0":
        dom_id = int(pick)

    pool = pick_questions(bank, cert, dom_id=dom_id, scen=scen_pick)
    if not pool:
        print(RED("  No questions available for that selection."))
        pause()
        return
    n = ask(f"How many questions? (1-{len(pool)})", default=str(min(10, len(pool))))
    try:
        count = max(1, min(int(n), len(pool)))
    except ValueError:
        count = min(10, len(pool))
    instant = ask_choice("Feedback mode", [("1", "Instant feedback after each answer"),
                                           ("2", "Exam style — feedback at the end")], default="1")
    qs = pool[:count]
    score = 0
    results = []
    for i, q in enumerate(qs, 1):
        show_question(q, i, len(qs))
        ans = read_answer(q)
        ok = grade(q, ans)
        results.append((q, ans, ok))
        if ok:
            score += 1
        if instant == "1":
            show_feedback(q, ans, ok)
        else:
            print(DIM("  Answer saved."))
    if instant == "2":
        print(BOLD("\n  Review:"))
        for q, ans, ok in results:
            show_feedback(q, ans, ok)
    pct = 100 * score / len(qs) if qs else 0
    print(f"\n  Score: {BOLD(f'{score}/{len(qs)}')} ({pct:.0f}%)")
    focus_label = scen_pick or (doms[str(dom_id)]["name"] if dom_id else "mixed")
    record_result({"ts": datetime.now().isoformat(timespec="seconds"),
                   "cert": cert, "mode": "practice", "score": score,
                   "total": len(qs), "pct": round(pct, 1), "focus": focus_label})
    report = write_review_report(cert, "practice", results, focus=focus_label)
    print(GREEN(f"\n  📄 Performance review saved: {report}"))
    pause()

# ------------------------------------------------------------- mock -------

def fmt_time(secs):
    secs = max(0, int(secs))
    return f"{secs // 60}:{secs % 60:02d}"

def compose_mock(bank, cert, n):
    """Sample n questions for `cert`, weighted by the official domain weights."""
    doms = bank[f"{cert}_domains"]
    by_dom = {int(k): [q for q in bank["questions"]
                       if q["cert"] == cert and q["domain_id"] == int(k)]
              for k in doms}
    plan = {}
    total_w = sum(d["weight"] for d in doms.values())
    assigned = 0
    items = sorted(doms.items(), key=lambda kv: -kv[1]["weight"])
    for i, (k, d) in enumerate(items):
        if i == len(items) - 1:
            plan[int(k)] = n - assigned
        else:
            c = round(n * d["weight"] / total_w)
            plan[int(k)] = c
            assigned += c
    picked, used = [], set()
    for d_id, c in plan.items():
        pool = by_dom[d_id][:]
        random.shuffle(pool)
        take = pool[:c]
        picked.extend(take)
        used.update(q["id"] for q in take)
    # top up from any domain if blueprint domains ran dry
    if len(picked) < n:
        rest = [q for q in bank["questions"]
                if q["cert"] == cert and q["id"] not in used]
        random.shuffle(rest)
        picked.extend(rest[: n - len(picked)])
    random.shuffle(picked)
    return picked, plan

def run_mock(bank, cert):
    clear()
    if cert == "professional":
        default_n = bank.get("professional_plan_total", 70)
        pool = sum(1 for q in bank["questions"] if q["cert"] == "professional")
        n = ask(f"Number of questions? (blueprint default {default_n}, pool of {pool})",
                default=str(default_n))
        try:
            n = max(7, min(int(n), pool))
        except ValueError:
            n = default_n
        qs, plan = compose_mock(bank, "professional", n)
        minutes = bank.get("professional_minutes", 130)
        title = "Professional Mock Exam"
        mix = ", ".join(f"D{k}:{v}" for k, v in sorted(plan.items()))
        info = (f"{len(qs)} questions · {minutes} minutes · 7 domains · "
                f"domain mix weighted to blueprint ({mix})")
    else:
        n = ask("Number of questions?", default=str(bank.get("foundations_plan_total", 60)))
        try:
            n = max(5, int(n))
        except ValueError:
            n = 60
        qs, plan = compose_mock(bank, "foundations", n)
        minutes = bank.get("foundations_minutes", 90)
        title = "Foundations Mock Exam"
        mix = ", ".join(f"D{k}:{v}" for k, v in sorted(plan.items()))
        info = f"{len(qs)} questions · {minutes} minutes · domain mix weighted to blueprint ({mix})"

    env_min = os.environ.get("EXAM_PREP_MINUTES")
    if env_min and env_min.isdigit():
        minutes = int(env_min)
        info += f"  (duration overridden to {minutes} min via EXAM_PREP_MINUTES)"

    print(BOLD(f"\n  {title}"))
    print(DIM("  " + info))
    print(DIM("  Rules: no guessing penalty — answer everything. Timer starts immediately."))
    print(DIM("  Keys: s = skip question · q = submit early · skips can be revisited at the end."))
    if ask("Begin? (y/n)", default="y").lower() not in ("y", "yes"):
        return

    start = time.time()
    deadline = start + minutes * 60
    answers = {}
    order = list(range(len(qs)))
    pending = order[:]
    warned = {10: False, 2: False}

    def remaining():
        return deadline - time.time()

    idx = 0
    try:
        while idx < len(pending):
            i = pending[idx]
            q = qs[i]
            rem = remaining()
            if rem <= 0:
                print(RED(BOLD("\n  ⏰ TIME — the exam is over. Auto-submitting.\n")))
                break
            if rem < 120 and not warned[2]:
                warned[2] = True
                print(YELLOW("  ⚠ Less than 2 minutes remaining!"))
            elif rem < 600 and not warned[10]:
                warned[10] = True
                print(YELLOW("  ⚠ Less than 10 minutes remaining."))
            show_question(q, idx + 1, len(pending),
                          timer_str=MAGENTA(f"[⏱ {fmt_time(rem)}]"))
            ans = read_answer(q)
            answers[i] = ans
            idx += 1
    except EarlySubmit:
        print(YELLOW("\n  Submitting exam early.\n"))

    # revisit unanswered
    unanswered = [i for i in order if answers.get(i) is None]
    while unanswered and remaining() > 0:
        print(f"\n  {YELLOW(f'{len(unanswered)} unanswered')} — revisit them?")
        if ask_choice("", [("y", "Yes, take me through them"), ("n", "No, submit now")], default="y") != "y":
            break
        try:
            for i in list(unanswered):
                if remaining() <= 0:
                    print(RED("  ⏰ TIME — submitting."))
                    break
                q = qs[i]
                show_question(q, unanswered.index(i) + 1, len(unanswered),
                              timer_str=MAGENTA(f"[⏱ {fmt_time(remaining())}]"))
                ans = read_answer(q)
                if ans is not None:
                    answers[i] = ans
                    unanswered.remove(i)
        except EarlySubmit:
            print(YELLOW("\n  Submitting exam early.\n"))
            unanswered = []
        unanswered = [i for i in order if answers.get(i) is None]
        if not unanswered:
            break
        if remaining() <= 0:
            break
        if ask("Continue reviewing answered questions? (y/n)", default="n").lower() != "y":
            break

    elapsed = time.time() - start
    score_exam(bank, cert, qs, answers, elapsed, minutes)
    pause()

def score_exam(bank, cert, qs, answers, elapsed, minutes):
    clear()
    total = len(qs)
    correct = sum(1 for i, q in enumerate(qs) if grade(q, answers.get(i)))
    skipped = sum(1 for i in range(total) if answers.get(i) is None)
    pct = 100 * correct / total if total else 0

    print(BOLD(f"\n  {'Professional' if cert == 'professional' else 'Foundations'} Mock Exam — Results"))
    hr("=")
    print(f"  Score:     {BOLD(f'{correct}/{total}')} ({pct:.1f}%)")
    print(f"  Skipped:   {skipped}")
    print(f"  Time used: {fmt_time(elapsed)} of {minutes}:00")

    # per-domain breakdown
    doms = bank["foundations_domains"] if cert == "foundations" else bank["professional_domains"]
    print()
    print(f"  {'Domain':<58} {'Score':>9}")
    hr()
    by_dom = {}
    for i, q in enumerate(qs):
        by_dom.setdefault(q["domain_id"], [0, 0])
        by_dom[q["domain_id"]][1] += 1
        if grade(q, answers.get(i)):
            by_dom[q["domain_id"]][0] += 1
    weak = []
    for d in sorted(doms, key=int):
        if int(d) not in by_dom:
            continue
        got, tot_d = by_dom[int(d)]
        dp = 100 * got / tot_d
        name = f"D{d} {doms[d]['name']}"[:56]
        mark = GREEN("✔") if dp >= 75 else (YELLOW("~") if dp >= 60 else RED("✘"))
        print(f"  {mark} {name:<56} {got:>3}/{tot_d:<3} {dp:5.1f}%")
        if dp < 75:
            weak.append(f"D{d} {doms[d]['name']} ({dp:.0f}%)")

    print()
    if cert == "professional":
        target = 75
        verdict = GREEN(BOLD("ON TRACK — at/above the ~75% benchmark")) if pct >= target \
            else RED(BOLD(f"BELOW TARGET — aim for ≥{target}% overall and in every domain"))
    else:
        scaled = 100 + 9 * pct  # rough linear mapping onto the 100–1000 scale
        verdict = (GREEN(BOLD("PASS (estimated)")) if scaled >= 720 else RED(BOLD("BELOW PASSING (estimated)")))
        verdict += DIM(f"  — ≈{scaled:.0f}/1000 scaled, passing is 720 (rough estimate)")
    print(f"  Verdict: {verdict}")
    if weak:
        print(YELLOW("  Domains to review: " + "; ".join(weak)))

    # review wrong answers?
    if ask("\n  Review every question with explanations? (y/n)", default="y").lower() in ("y", "yes"):
        for i, q in enumerate(qs):
            ans = answers.get(i)
            show_feedback(q, ans, grade(q, ans))

    record_result({"ts": datetime.now().isoformat(timespec="seconds"),
                   "cert": cert, "mode": "mock", "score": correct, "total": total,
                   "pct": round(pct, 1), "skipped": skipped,
                   "minutes_used": round(elapsed / 60, 1), "minutes_limit": minutes,
                   "domains": {str(d): {"got": by_dom[d][0], "of": by_dom[d][1]} for d in by_dom}})
    all_results = [(qs[i], answers.get(i), grade(qs[i], answers.get(i))) for i in range(total)]
    report = write_review_report(cert, "mock", all_results,
                                 minutes_used=elapsed / 60, minutes_limit=minutes)
    print(GREEN(f"  📄 Performance review saved: {report}"))

# ------------------------------------------------------------- study ------

def study_notes():
    clear()
    if not os.path.exists(NOTES):
        print(YELLOW("  No study notes built yet — run build_data.py after the review agents finish."))
        pause()
        return
    notes = json.load(open(NOTES, encoding="utf-8"))
    print(BOLD("\n  Foundations — Domain Study Notes\n"))
    for d in notes:
        print(CYAN(BOLD(f"  Domain {d['domain_id']}: {d['domain']} ({d['weight']}%)")))
        hr()
        for pt in d["key_points"]:
            print(wrap("• " + pt, indent=2))
        print()
    pause()

EXERCISES = [
    ("Exercise 1: Multi-tool Agent with Escalation Logic",
     "Domains 1, 2, 5",
     ["Define 3–4 MCP tools with detailed descriptions (include two similar tools to test tool selection)",
      "Implement an agent loop checking stop_reason ('tool_use' / 'end_turn')",
      "Add structured error responses: errorCategory, isRetryable, description",
      "Implement an interceptor hook that blocks operations above a threshold and routes to escalation",
      "Test with multi-aspect requests"]),
    ("Exercise 2: Configuring Claude Code for Team Development",
     "Domains 2, 3",
     ["Create a project-level CLAUDE.md with universal standards",
      "Create .claude/rules/ files with YAML frontmatter for different code areas (paths: ['src/api/**/*'], paths: ['**/*.test.*'])",
      "Create a project skill under .claude/skills/ with context: fork and allowed-tools",
      "Configure an MCP server in .mcp.json with environment variables + a personal override in ~/.claude.json",
      "Test planning mode vs direct execution on tasks of different complexity"]),
    ("Exercise 3: Structured Data Extraction Pipeline",
     "Domains 4, 5",
     ["Define an extraction tool with a JSON schema (required/optional fields, enums with 'other', nullable fields)",
      "Build a validation loop: on error, retry with the document, the incorrect extraction, and the specific validation error",
      "Add few-shot examples for documents with different structures",
      "Use batch processing via the Message Batches API: 100 documents, handle failures via custom_id",
      "Route to humans: field-level confidence scores, document-type analysis"]),
    ("Exercise 4: Designing and Debugging a Multi-agent Research Pipeline",
     "Domains 1, 2, 5",
     ["A coordinator with 2+ subagents (allowedTools includes 'Task', context is passed explicitly in prompts)",
      "Run subagents in parallel via multiple Task calls in a single response",
      "Require structured subagent output: claim, quote, source URL, publication date",
      "Simulate a subagent timeout: return structured error context to the coordinator and continue with partial results",
      "Test with conflicting data: preserve both values with attribution; separate confirmed vs disputed findings"]),
]

OUT_OF_SCOPE = [
    "Fine-tuning Claude models or training custom models",
    "Claude API authentication, billing, or account management",
    "Detailed implementation in specific languages/frameworks beyond tool/schema configuration",
    "Deploying or hosting MCP servers (infrastructure, networking, orchestration)",
    "Claude's internal architecture, training process, or model weights",
    "Constitutional AI, RLHF, or safety training methodologies",
    "Embedding models or vector database implementation details",
    "Computer use (browser automation, desktop interaction)",
    "Image analysis capabilities (Vision)",
    "Streaming API or server-sent events",
    "Rate limiting, quotas, or detailed API cost calculations",
    "OAuth, API key rotation, or authentication protocol details",
    "Cloud-provider-specific configurations (AWS, GCP, Azure)",
    "Performance benchmarks or model comparison metrics",
    "Prompt caching implementation details (beyond knowing it exists)",
    "Token counting algorithms or tokenization specifics",
]

PREP_PLAN = [
    "Build an agent with the Claude Agent SDK — full agent loop with tool calling, error handling, session management; practice subagents and explicit context passing.",
    "Configure Claude Code for a real project — CLAUDE.md hierarchy, path-specific rules in .claude/rules/, skills with context: fork and allowed-tools, MCP server integration.",
    "Design and test MCP tools — descriptions that differentiate similar tools, structured errors with categories and retry flags, test against ambiguous requests.",
    "Build a data extraction pipeline — tool_use with JSON schemas, validation/retry loops, optional/nullable fields, batching via the Message Batches API.",
    "Practice prompt engineering — few-shot examples for ambiguous scenarios, explicit review criteria, multi-pass architectures for large code reviews.",
    "Study context management patterns — extract facts from verbose outputs, scratchpad files, delegate discovery to subagents.",
    "Understand escalation and human-in-the-loop — when to escalate (policy gaps, explicit user request, no progress) and confidence-based routing.",
    "Take a practice exam before the real one — same scenarios and format.",
]

OFFICIAL_LINKS = [
    ("Claude API — Messages", "https://platform.claude.com/docs/en/api/messages"),
    ("Claude API — Tool Use", "https://platform.claude.com/docs/en/build-with-claude/tool-use"),
    ("Claude API — Message Batches", "https://platform.claude.com/docs/en/build-with-claude/message-batches"),
    ("Claude Agent SDK — Overview", "https://platform.claude.com/docs/en/agent-sdk/overview"),
    ("Claude Agent SDK — Hooks", "https://platform.claude.com/docs/en/agent-sdk/hooks"),
    ("Claude Agent SDK — Subagents", "https://platform.claude.com/docs/en/agent-sdk/subagents"),
    ("Model Context Protocol", "https://modelcontextprotocol.io/"),
    ("Claude Code — Documentation", "https://code.claude.com/docs/en/overview"),
    ("Claude Code — CLAUDE.md & Memory", "https://code.claude.com/docs/en/memory"),
    ("Claude Code — Skills", "https://code.claude.com/docs/en/skills"),
    ("Claude Code — Hooks", "https://code.claude.com/docs/en/hooks"),
    ("Claude Code — Headless mode", "https://code.claude.com/docs/en/headless"),
    ("Prompt Engineering Guide", "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview"),
    ("Extended Thinking", "https://platform.claude.com/docs/en/build-with-claude/extended-thinking"),
]


def practical_exercises():
    clear()
    print(BOLD("\n  Foundations — Practical Exercises (hands-on rehearsal)\n"))
    print(DIM("  From the official study guide. Work through these in a real project;"))
    print(DIM("  each maps to the domains shown.\n"))
    for title, doms, steps in EXERCISES:
        print(CYAN(BOLD("  " + title)) + DIM(f"   [{doms}]"))
        hr()
        for i, s in enumerate(steps, 1):
            print(wrap(f"{i}. {s}", indent=4))
        print()
    pause()


def exam_info(bank):
    clear()
    f_tot = sum(1 for q in bank["questions"] if q["cert"] == "foundations")
    p_tot = sum(1 for q in bank["questions"] if q["cert"] == "professional")
    print(BOLD("\n  Exam Formats (from the official materials)\n"))
    print(CYAN(BOLD("  CLAUDE CERTIFIED ARCHITECT — FOUNDATIONS")))
    hr()
    print(wrap("""• Question type: multiple choice, 1 correct out of 4 options.
• Scoring: 100–1000 scale — passing score is 720.
• No guessing penalty: answer every question.
• Scenarios: 4 of 8 possible scenarios are randomly selected.
• Five domains: Agent architecture & orchestration 27% · Tool design & MCP 18% · Claude Code configuration & workflows 20% · Prompt engineering & structured output 20% · Context management & reliability 15%.
• This app's mock: 60 questions / 90 minutes (question count is configurable), domain mix weighted to the blueprint.""", indent=2))
    print()
    print(CYAN(BOLD("  CLAUDE CERTIFIED ARCHITECT — PROFESSIONAL")))
    hr()
    print(wrap("""• 63 questions · 120 minutes.
• Formats: single choice (one of four — most common), multiple response (select TWO+), scenario matching (classify several items; options may repeat).
• Aim for roughly 75% or better in every domain.
• Seven blueprint domains: Solution Design & Architecture 17% (11q) · Claude Models, Prompting & Context Engineering 13% (8q) · Integration 19% (12q) · Evaluation, Testing & Optimization 16% (10q) · Governance, Safety & Risk Management 14% (9q) · Stakeholder Communication & Lifecycle 14% (9q) · Developer Productivity & Operational Enablement 7% (4q).""", indent=2))
    print()
    print(CYAN(BOLD("  NOT ON THE FOUNDATIONS EXAM (official out-of-scope list)")))
    hr()
    for t in OUT_OF_SCOPE:
        print(wrap("• " + t, indent=2))
    print()
    print(CYAN(BOLD("  PREPARATION PLAN (official recommendations)")))
    hr()
    for i, t in enumerate(PREP_PLAN, 1):
        print(wrap(f"{i}. {t}", indent=2))
    print()
    print(CYAN(BOLD("  OFFICIAL DOCUMENTATION")))
    hr()
    for name, url in OFFICIAL_LINKS:
        print(f"  • {name:<34} {DIM(url)}")
    print()
    print(DIM(f"  Question bank on file: Foundations {f_tot} · Professional {p_tot}"))
    pause()

def results_history():
    clear()
    hist = load_history()
    print(BOLD("\n  Results History\n"))
    if not hist:
        print(DIM("  No attempts recorded yet."))
        pause()
        return
    print(f"  {'When':<20} {'Cert':<14} {'Mode':<9} {'Score':>12} {'%':>6} {'Time':>8}")
    hr()
    for h in hist[-30:]:
        ts = h.get("ts", "?")[:16].replace("T", " ")
        score = f"{h.get('score')}/{h.get('total')}"
        t = f"{h.get('minutes_used')}m" if h.get("minutes_used") else ""
        pct = h.get("pct", 0)
        colored = GREEN(f"{pct:.0f}%") if pct >= 75 else (YELLOW(f"{pct:.0f}%") if pct >= 60 else RED(f"{pct:.0f}%"))
        print(f"  {ts:<20} {h.get('cert',''):<14} {h.get('mode',''):<9} {score:>12} {colored:>15} {t:>8}")
    print(DIM("\n  (showing last 30 attempts)"))
    if os.path.isdir(REVIEWS_DIR):
        reviews = sorted(os.listdir(REVIEWS_DIR))
        if reviews:
            print(f"\n  {BOLD('Markdown reviews')} ({len(reviews)} saved in results/reviews/):")
            for r in reviews[-5:]:
                print(f"    • {r}")
            if len(reviews) > 5:
                print(DIM(f"    … and {len(reviews) - 5} earlier"))
    if ask("\n  Clear history? (y/n)", default="n").lower() in ("y", "yes"):
        os.remove(HISTORY)
        print(GREEN("  History cleared."))
    pause()

# ---------------------------------------------------------------- main ----

def main():
    bank = load_bank()
    while True:
        try:
            choice = main_menu()
            if choice == "1":
                practice_session(bank, "foundations")
            elif choice == "2":
                practice_session(bank, "professional")
            elif choice == "3":
                run_mock(bank, "foundations")
            elif choice == "4":
                run_mock(bank, "professional")
            elif choice == "5":
                study_notes()
            elif choice == "6":
                practical_exercises()
            elif choice == "7":
                exam_info(bank)
            elif choice == "8":
                results_history()
            elif choice == "0":
                print("\n  Good luck on the exam! 🚀\n")
                return
        except KeyboardInterrupt:
            print(DIM("\n  Interrupted — back to menu."))
            time.sleep(0.3)

if __name__ == "__main__":
    main()
