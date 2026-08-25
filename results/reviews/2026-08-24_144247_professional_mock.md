# Performance Review — Professional Mock Exam

- **Date:** 2026-08-24 14:42
- **Mode:** Timed mock exam
- **Score:** **57/63 (90.5%)** · skipped: 0
- **Time used:** 30.4 min of 120 min
- **Benchmark:** ≥75% overall and in every domain — **NEEDS WORK in the domains below**

## Domain breakdown

| Domain | Score | % | Status |
|---|---|---|---|
| D1 Solution Design & Architecture | 8/11 | 73% | ⚠️ borderline |
| D2 Claude Models, Prompting & Context Engineering | 7/8 | 88% | ✅ solid |
| D3 Integration | 10/12 | 83% | ✅ solid |
| D4 Evaluation, Testing & Optimization | 10/10 | 100% | ✅ solid |
| D5 Governance, Safety & Risk Management | 9/9 | 100% | ✅ solid |
| D6 Stakeholder Communication & Lifecycle Management | 9/9 | 100% | ✅ solid |
| D7 Developer Productivity & Operational Enablement | 4/4 | 100% | ✅ solid |

## Areas to read up on

Prioritise these domains (weakest first):

### 1. Solution Design & Architecture — 8/11 (73%)

- What to revisit: Revisit solution design trade-offs: fixed workflows vs autonomous agents vs multi-agent systems, when to decompose, routing/supervisor patterns, build-vs-buy decisions.
- Your missed questions: pro-1.10, pro-1.11, pro-1.1


## Missed & skipped questions — walkthrough

### pro-3.3 · Integration

> A Claude-based assistant queries an HR system on behalf of employees. It authenticates using a single service account with organisation-wide read access, and the system prompt instructs the model to only return data belonging to the requesting employee. A security review flags this design. What is the core problem?

- **Your answer:** D
- **Correct answer:** A
- **Explanation:** The prompt is doing authorisation's job. Instructions are not a security boundary — access control must be enforced by the system layer (per-user scoped credentials or pass-through auth) so the model can't return what it can't retrieve. Why not the others: B is not a real compliance rule; C expands the blast radius; D is a credential-handling anti-pattern.

### pro-1.10 · Solution Design & Architecture

> A team is assessing whether a complex due-diligence task justifies a multi-agent design instead of a single augmented agent. Which TWO characteristics of the task most strongly indicate that multiple agents are warranted?

- **Your answer:** C, D
- **Correct answer:** C, E
- **Explanation:** Multi-agent designs earn their complexity when sub-tasks need genuinely different specialisations, tools, and context, and when independent sub-tasks can run in parallel. High request volume is a scaling concern solvable within any pattern, a large budget is a budget fact, not an architectural driver, and stakeholder demand for the most sophisticated architecture is prestige, not an architectural driver.

### pro-3.12 · Integration

> For each integration need, identify the most suitable connection mechanism. Choose from: MCP server, direct API integration, or agent-to-agent protocol.

- **Your matches:** 1:direct API integration, 2:direct API integration, 3:agent-to-agent protocol, 4:MCP server, 5:MCP server
- **Correct matches:** 1:MCP server, 2:direct API integration, 3:agent-to-agent protocol, 4:MCP server, 5:direct API integration
- **Explanation:** Items 1 and 4 need standardised, reusable, discoverable access for many present and future consumers — MCP. Items 2 and 5 are deterministic, tightly scoped calls inside owned pipelines — direct integration, with no discovery layer needed. Item 3 crosses an organisational trust boundary between autonomous agents — agent-to-agent.

### pro-2.7 · Claude Models, Prompting & Context Engineering

> A high-volume application has a large, mostly static prompt and rising per-request costs. Which TWO techniques most directly reduce per-request cost while preserving capability?

- **Your answer:** C, D
- **Correct answer:** A, D
- **Explanation:** A cacheable static prefix cuts the cost of repeated content, and on-demand loading means each request pays only for the instructions it needs. Increasing max output tokens increases token usage, adding more few-shot examples increases token usage on every request, and moving all static content into the user message just relocates the same tokens.

### pro-1.11 · Solution Design & Architecture

> For each scenario, identify the most appropriate architectural pattern. Choose from: single augmented LLM call, fixed workflow, autonomous agent, or multi-agent system.

- **Your matches:** 1:single augmented LLM call, 2:autonomous agent, 3:autonomous agent, 4:multi-agent system, 5:single augmented LLM call
- **Correct matches:** 1:single augmented LLM call, 2:fixed workflow, 3:autonomous agent, 4:multi-agent system, 5:single augmented LLM call
- **Explanation:** Scenarios 1 and 5 are single transformations with supplied context — one augmented call each. Scenario 2 is a stable, repeating sequence — a workflow. Scenario 3's path depends on what each step reveals — an autonomous agent. Scenario 4 needs distinct specialists coordinated into one output — multi-agent.

### pro-1.1 · Solution Design & Architecture

> A logistics company wants Claude to process inbound freight quotes. Every request follows the same steps: extract shipment details from an email, validate them against a rate card, and generate a quote document. Requirements are stable and the steps never vary. Which architectural pattern is most appropriate?

- **Your answer:** C
- **Correct answer:** B
- **Explanation:** The task is stable, repeatable, and fully known in advance — the textbook case for a fixed workflow, which gives predictability, per-step auditability, and easy debugging. The multi-agent option adds coordination overhead the problem doesn't need, the autonomous agent adds planning overhead the problem doesn't need, and the monolithic prompt sacrifices step-level control and validation.

---
*Generated by exam_prep.py · 2026-08-24T14:42:47*
