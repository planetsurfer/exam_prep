# Performance Review — Professional Mock Exam

- **Date:** 2026-08-25 19:45
- **Mode:** Timed mock exam
- **Score:** **67/70 (95.7%)** · skipped: 0
- **Time used:** 30.5 min of 130 min
- **Benchmark:** ≥75% overall and in every domain — **ON TRACK**

## Domain breakdown

| Domain | Score | % | Status |
|---|---|---|---|
| D1 Solution Design & Architecture | 11/12 | 92% | ✅ solid |
| D2 Claude Models, Prompting & Context Engineering | 9/9 | 100% | ✅ solid |
| D3 Integration | 12/13 | 92% | ✅ solid |
| D4 Evaluation, Testing & Optimization | 11/11 | 100% | ✅ solid |
| D5 Governance, Safety & Risk Management | 9/10 | 90% | ✅ solid |
| D6 Stakeholder Communication & Lifecycle Management | 10/10 | 100% | ✅ solid |
| D7 Developer Productivity & Operational Enablement | 5/5 | 100% | ✅ solid |

## Areas to read up on

All domains are at or above the 75% target. To consolidate:

- Re-run a mock exam on a different day to confirm retention.
- Skim the explanations of any question you got right but guessed on.

## Missed & skipped questions — walkthrough

### ccarp-49 · Governance, Safety & Risk Management

> An architect is documenting the failure modes of a proposed Claude system for a risk review. Select TWO failure modes that are inherent characteristics of LLM-based systems and must be designed for rather than eliminated.

- **Your answer:** A, E
- **Correct answer:** C, E
- **Explanation:** Correct: C and E. Both are intrinsic to how language models work rather than defects to be patched. Fluent-but-wrong output (C) follows from a system that generates plausible continuations rather than retrieving verified facts; you manage it with grounding, citation, verification, and human review at the points where being wrong is costly. Non-determinism (E) follows from probabilistic sampling; you manage it by designing for tolerance — validating output against schemas, making downstream steps idempotent, and setting expectations that identical inputs need not produce identical text. Naming these honestly in a risk review distinguishes a credible architect from an optimistic one. B (network dependency) is an ordinary distributed-systems concern addressed with retries, timeouts, circuit breakers, and fallbacks — not specific to LLMs. A (budget overrun) is a cost-management issue handled with quotas, alerting, and rate limits — a consequence of usage, not a model behaviour. D (credential requirement) is a normal access-control property, not a failure mode. Blueprint: identify risks, limitations, and failure modes of LLM systems.

### ccarp-30 · Integration

> A fraud-review assistant currently achieves 96% accuracy with a p95 latency of 4.1 seconds by retrieving 20 documents and using an extended reasoning configuration. The business states that reviewers abandon the tool above 2 seconds, and that a 2-point accuracy drop is acceptable if it keeps reviewers in the tool. Which configuration decision is best justified?

- **Your answer:** C
- **Correct answer:** B
- **Explanation:** Correct: B. The business has done the hard part: it stated the trade-off explicitly, giving a latency threshold and an accuracy tolerance. The architect's job is to find the configuration that satisfies both and to verify it — tuning retrieval depth and reasoning budget toward the 2-second target, then validating against the eval set that accuracy stayed at/above the stated 94% floor. The tiered-routing clause is what makes the answer strong: sending only low-confidence cases down the slow, thorough path preserves accuracy where it matters while keeping the common case fast. A tool reviewers abandon has an effective accuracy of zero. D overrides an explicit business decision with a technical preference — accuracy never consumed is not paramount, it's unused. A (single-document retrieval) is an unvalidated overcorrection that will likely breach the 94% floor — the requirement was to hit 2 s, not minimize latency at any cost. C (progress indicator) manages perception, not latency; the threshold came from observed abandonment behaviour. Blueprint: evaluate accuracy-latency trade-offs and justify configuration decisions.

### ccarp-2 · Solution Design & Architecture

> An architect is choosing between a deterministic workflow and an agentic architecture for a new system. Select TWO conditions that most strongly favor the agentic design.

- **Your answer:** B, E
- **Correct answer:** A, C
- **Explanation:** Correct: A and C. Agentic architectures exist to handle an unknown path (A) and adaptive recovery (C) — a control loop that re-evaluates state after each action. D (hard 300 ms p99) argues against agents, since loops multiply model calls and round trips. B (identical per-request cost) requires deterministic token consumption, which agent loops break. E (one classification on a fixed label set) is the canonical single model call — an agent loop is pure overhead. Blueprint: select appropriate architectural patterns; design multi-agent systems and orchestration strategies.

---
*Generated by exam_prep.py · 2026-08-25T19:45:29*
