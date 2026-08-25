# Claude Certified Architect — Terminal Exam Prep

A menu-driven terminal study app covering **both** certifications, built entirely
from the material in the two sibling folders:

- `../claude-certified-architect-main/` — Foundations study guide, 76-question practice test, practical exercises
- `../resources/1783837911603.pdf` — Professional (CCAR-P) full practice set, 63 questions, exam-guide v1.0 blueprint
- `~/Downloads/CCAR-P.pdf` — CCAR-P Mock Exam, 70 questions with detailed answer rationale, current 70Q/130-min blueprint

## Run

```bash
python3 exam_prep.py
```

No dependencies — pure Python 3 standard library.

## Menu

| # | What it does |
|---|---|
| 1 | **Foundations practice session** — by domain, by exam scenario, or mixed; instant or end-of-set feedback |
| 2 | **Professional practice session** — same modes; includes multi-select and scenario-matching questions |
| 3 | **Foundations mock exam** — timed (90 min default), questions sampled to the 5-domain blueprint weights |
| 4 | **Professional mock exam** — 70 questions sampled to the official blueprint weights from a 133-question pool, 130-minute timer, real exam format |
| 5 | Domain study notes (high-yield key points per domain) |
| 6 | Practical exercises (the 4 hands-on drills from the guide) |
| 7 | Exam formats, out-of-scope list, prep plan, official doc links |
| 8 | Results history + saved review files |

Exam keys: `s` skip · `q` submit early · skips are revisited at the end · timer auto-submits at 0:00.

## Question bank (233 questions)

| Source | Count |
|---|---|
| Foundations practice test (scenarios 1–4) | 60 |
| Foundations practice test Q61–76 (Conversational AI scenario) | 16 |
| Foundations, authored from guide chapters (domains 2/4/5) | 24 |
| Professional practice set (extracted verbatim from PDF, all 3 formats) | 63 |
| Professional CCAR-P Mock Exam (`pro_ccarp70.json`, verbatim, 9 Select-TWO) | 70 |

## Performance reviews

After **every** practice session and mock exam a Markdown review is written to
`results/reviews/<timestamp>_<cert>_<mode>.md` containing:

- score, %, time used, pass/benchmark verdict
- per-domain breakdown with ✅/⚠️/❌ status
- **areas to read up on** — weak domains with exactly which guide chapters to revisit
- walkthrough of every missed/skipped question with the correct answer and explanation

Attempt history is appended to `results/history.jsonl`.

## Speed drills

Override the mock-exam clock (e.g. a 10-minute sprint):

```bash
EXAM_PREP_MINUTES=10 python3 exam_prep.py
```

## Rebuilding the bank

Agent-generated sources live in `data_src/`; the app reads `data/questions.json`.
To rebuild after editing sources: `python3 build_data.py`.

## Study-loop prompt

See the bottom of this README's git history / ask Claude to "run my exam-prep loop" —
the canonical prompt is kept in `LOOP_PROMPT.md`.
