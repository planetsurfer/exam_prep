# Exam-Prep Loop Prompt

Paste this into Claude Code (optionally via `/loop`, e.g. `/loop 30m`) to run a
recurring study cycle against this prep system. Each pass is one complete cycle.

---

## The prompt

```
Run one exam-prep study cycle for the Claude Certified Architect certifications
in /Volumes/ExternalOne/ClaudeArchitextExam. Work silently through steps 1-4,
then interact with me for step 5:

1. DIAGNOSE — Read exam_prep/results/history.jsonl (if present) and the latest
   files in exam_prep/results/reviews/. Identify my weakest domains (lowest %,
   fewest attempts, or oldest attempt). If no history exists, start with
   Foundations Domain 1 and ask me which certification I'm targeting first.

2. TEACH — From the source material, produce a concise refresher ONLY for the
   weakest 1-2 domains:
   - Foundations: claude-certified-architect-main/guide_en.md (PART I chapters +
     PART II domain notes for that domain).
   - Professional: rationales in exam_prep/data_src/pro_*.json for that domain.
   Keep it under ~40 lines: key facts, named parameters/flags, decision rules,
   common traps.

3. DRILL — Quiz me interactively on 5 NEW questions for those domains. Use
   questions from exam_prep/data/questions.json that I have not been asked
   before in this conversation; if the pool for a domain is exhausted, author
   new exam-style questions grounded in the guide and add them to the bank by
   appending to the appropriate exam_prep/data_src file and re-running
   `python3 exam_prep/build_data.py`.

4. RECORD — Write my results for this cycle as a Markdown review in
   exam_prep/results/reviews/ using the same format as exam_prep.py's
   write_review_report (score, domain breakdown, areas to read up on with
   specific chapter references, missed-question walkthrough). Also append one
   JSON line to exam_prep/results/history.jsonl with: ts, cert, mode:"loop",
   score, total, pct, focus.

5. REPORT — Show me: this cycle's score vs my previous cycles, my current
   weakest domain, exactly what to read before the next cycle, and a
   recommendation (keep drilling / take a mock exam / ready to book).

Rules: never reveal answer letters before I answer; always show the explanation
after each answer; match real exam formats (Foundations: 1-of-4; Professional:
single / select-TWO / scenario-matching).
```

---

## Notes

- Run it manually any time: paste the block above into a fresh Claude Code
  session in this folder.
- As a scheduled loop: `/loop 30m` + the prompt runs one cycle every 30 minutes
  (good for a study afternoon); omit the interval to let Claude self-pace.
- The loop deliberately favors *your* weak areas: the more attempts you log in
  the app (`python3 exam_prep/exam_prep.py`), the sharper its targeting gets.
