# Performance Review — Foundations Practice Session

- **Date:** 2026-08-24 09:29
- **Mode:** Practice session · focus: Tool design and MCP integration
- **Score:** **10/17 (58.8%)** · skipped: 0
- **Scaled estimate:** ≈629/1000 (passing = 720) — **below passing (estimated)**

## Domain breakdown

| Domain | Score | % | Status |
|---|---|---|---|
| D2 Tool design and MCP integration | 10/17 | 59% | ❌ weak |

## Areas to read up on

Prioritise these domains (weakest first):

### 2. Tool design and MCP integration — 10/17 (59%)

- What to revisit: Study guide Part I — Ch. 2 (tool_use, tool_choice, tool descriptions, JSON schemas) and Ch. 4 (MCP servers, isError, resources, .mcp.json); then Part II Domain 2 notes.
- Your missed questions: found-new-8, found-ex-2, found-new-1, found-7, found-56, found-new-3, found-10


## Missed & skipped questions — walkthrough

### found-new-8 · Tool design and MCP integration

> Claude Code is updating a logging call that appears identically in several functions of one large file. The Edit tool keeps failing because the old string matches multiple locations, and retrying with the same string does not help.
> What is the recommended fallback?

- **Your answer:** D
- **Correct answer:** C
- **Explanation:** The guide's guidance for built-in tools: when Edit fails due to non-unique matches, fall back to Read + Write — read the file, apply the changes, and write the full updated content. A shorter match string makes uniqueness worse, not better; a blind sed replace risks unintended changes; and restructuring the file is an out-of-scope workaround for a tool-usage problem.

### found-ex-2 · Tool design and MCP integration

> Production monitoring shows your `search_catalog` tool fails 12% of the time: 8% are network timeouts that succeed when retried, and 4% are query syntax errors that never succeed regardless of retries. Currently both error types are returned identically, causing wasted retries.
> How should you modify the tool's error handling?

- **Your answer:** B
- **Correct answer:** C
- **Explanation:** Handling retries at the tool level for transient errors is the correct abstraction boundary—the tool has definitive knowledge of the error type and can implement deterministic retry logic without relying on the agent to interpret a flag (D) or follow prompt-level instructions (A). Uniform backoff (B) wastes time on syntax errors that will never succeed.

### found-new-1 · Tool design and MCP integration

> A document pipeline calls Claude with three extraction tools defined (one each for invoices, contracts, and receipts). Compliance requires every document to yield structured JSON from one of these tools, but which tool applies depends on the document type. Currently, the model occasionally replies with a plain-text summary instead of calling any tool at all. You need to guarantee structured output while still letting the model pick the right extractor.
> Which configuration is most appropriate?

- **Your answer:** D
- **Correct answer:** B
- **Explanation:** `tool_choice: "any"` forces the model to call some tool — guaranteeing schema-based structured output — while leaving the choice among the three extraction tools to the model, which is exactly what a mixed document stream needs. `auto` permits the observed text-only failure mode; forcing `extract_invoice` would be wrong for contracts and receipts; prompt-only formatting instructions cannot guarantee syntactically valid JSON the way tool_use with a schema does.

### found-7 · Tool design and MCP integration

> Production logs show a persistent pattern: requests like “analyze the uploaded quarterly report” are routed to the web-search agent 45% of the time instead of the document analysis agent. Reviewing tool definitions, you find that the web-search agent has a tool `analyze_content` described as “analyzes content and extracts key information,” while the document analysis agent has a tool `analyze_document` described as “analyzes documents and extracts key information.” How should you fix the misrouting problem?
> How should you fix the misrouting problem?

- **Your answer:** A
- **Correct answer:** B
- **Explanation:** Renaming the web-search tool to `extract_web_results` and updating its description to explicitly reference web search and URLs directly removes the root cause by eliminating semantic overlap between the two tool names and descriptions. This makes each tool’s purpose unambiguous, enabling the coordinator to reliably distinguish document analysis from web search.

### found-56 · Tool design and MCP integration

> Production logs show a consistent pattern: when customers include the word “account” in their message (e.g., “I want to check my account for an order I made yesterday”), the agent calls `get_customer` first 78% of the time. When customers phrase similar requests without “account” (e.g., “I want to check an order I made yesterday”), it calls `lookup_order` first 93% of the time. Tool descriptions are clear and unambiguous. What is the most likely root cause of this discrepancy?
> What is the most likely root cause?

- **Your answer:** D
- **Correct answer:** A
- **Explanation:** The systematic keyword-driven pattern (78% vs 93%) strongly indicates explicit routing logic in the system prompt reacting to the word “account” and steering the agent toward customer-related tools. Since tool descriptions are already clear, the discrepancy points to prompt-level instructions creating unintended behavioral steering.

### found-new-3 · Tool design and MCP integration

> An agent using a Jira MCP server spends many exploratory tool calls at the start of every task — listing projects, then boards, then issue types — just to learn what exists. You want the agent to have an immediate 'map' of the available work items without taking actions. The MCP server supports all three primary resource types.
> Which MCP primitive best addresses this?

- **Your answer:** D
- **Correct answer:** A
- **Explanation:** Resources are data the agent reads for context without taking actions; the guide highlights that a resource provides an immediate 'map' of what exists, eliminating exploratory tool-call chains. Adding more tools widens the selection surface rather than supplying catalog knowledge; richer descriptions change how tools are used but still require calls to learn state; a prompt template steering a tool call still costs the exploratory calls.

### found-10 · Tool design and MCP integration

> In your system design, you gave the document analysis agent access to a general-purpose tool `fetch_url` so it could download documents by URL. Production logs show this agent now frequently downloads search engine results pages to perform ad hoc web search—behavior that should be routed through the web-search agent—causing inconsistent results. Which fix is most effective?
> Which fix is most effective?

- **Your answer:** D
- **Correct answer:** A
- **Explanation:** Replacing a general-purpose tool with a document-specific tool that validates URLs against document formats fixes the root cause by constraining capability at the interface level. This follows the principle of least privilege, making undesired search behavior impossible rather than merely discouraged.

---
*Generated by exam_prep.py · 2026-08-24T09:29:35*
