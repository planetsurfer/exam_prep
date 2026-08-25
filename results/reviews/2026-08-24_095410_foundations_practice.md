# Performance Review — Foundations Practice Session

- **Date:** 2026-08-24 09:54
- **Mode:** Practice session · focus: Claude Code configuration and workflows
- **Score:** **10/17 (58.8%)** · skipped: 0
- **Scaled estimate:** ≈629/1000 (passing = 720) — **below passing (estimated)**

## Domain breakdown

| Domain | Score | % | Status |
|---|---|---|---|
| D3 Claude Code configuration and workflows | 10/17 | 59% | ❌ weak |

## Areas to read up on

Prioritise these domains (weakest first):

### 3. Claude Code configuration and workflows — 10/17 (59%)

- What to revisit: Study guide Part I — Ch. 5 (CLAUDE.md hierarchy, rules, commands, skills, planning mode, /compact, /memory, CI/CD headless mode, sessions) and Ch. 13 (built-in tools); then Part II Domain 3 notes.
- Your missed questions: found-39, found-26, found-43, found-38, found-40, found-35, found-31


## Missed & skipped questions — walkthrough

### found-39 · Claude Code configuration and workflows

> Your team created a `/migration` skill that generates database migration files. It takes the migration name via `$ARGUMENTS`. In production you observe three issues: (1) developers often run the skill without arguments, causing poorly named files, (2) the skill sometimes uses database schema details from unrelated prior conversations, and (3) a developer accidentally ran destructive test cleanup when the skill had broad tool access.
> Which configuration approach fixes all three problems?

- **Your answer:** C
- **Correct answer:** B
- **Explanation:** This uses three separate configuration features to address each problem: `argument-hint` improves argument entry and reduces missing arguments, `context: fork` prevents context leakage from prior conversations, and `allowed-tools` constrains the skill to safe file-writing operations, preventing destructive actions.

### found-26 · Claude Code configuration and workflows

> Your pipeline script runs `claude "Analyze this pull request for security issues"`, but the job hangs indefinitely. Logs show Claude Code is waiting for interactive input. What is the correct approach to run Claude Code in an automated pipeline?
> What is the correct approach?

- **Your answer:** D
- **Correct answer:** B
- **Explanation:** The `-p` (or `--print`) flag is the documented way to run Claude Code non-interactively. It processes the prompt, prints the result to stdout, and exits without waiting for user input—ideal for CI/CD pipelines.

### found-43 · Claude Code configuration and workflows

> You create a custom skill `/explore-alternatives` that your team uses to brainstorm and evaluate implementation approaches before choosing one. Developers report that after running the skill, subsequent Claude responses are influenced by the alternatives discussion—sometimes referencing rejected approaches or retaining exploration context that interferes with actual implementation.
> How should you most effectively configure this skill?

- **Your answer:** A
- **Correct answer:** B
- **Explanation:** `context: fork` runs the skill in an isolated subagent context so exploration discussions do not pollute the main conversation history. This prevents rejected approaches and brainstorming context from influencing subsequent implementation work.

### found-38 · Claude Code configuration and workflows

> You find that including 2–3 full endpoint implementation examples as context significantly improves consistency when generating new API endpoints. However, this context is useful only when creating new endpoints—not when debugging, reviewing code, or other work in the API directory.
> Which configuration approach is most effective?

- **Your answer:** C
- **Correct answer:** D
- **Explanation:** A skill invoked on demand loads the example context only when generating new endpoints, not during unrelated tasks like debugging or review. This keeps the main context clean while preserving high-quality generation when needed.

### found-40 · Claude Code configuration and workflows

> Your codebase contains areas with different coding conventions: React components use functional style with hooks, API handlers use async/await with specific error handling, and database models follow the repository pattern. Test files are distributed across the codebase next to the code under test (e.g., `Button.test.tsx` next to `Button.tsx`), and you want all tests to follow the same conventions regardless of location.
> What is the most supported way to ensure Claude automatically applies the correct conventions when generating code?

- **Your answer:** C
- **Correct answer:** D
- **Explanation:** `.claude/rules/` files with YAML frontmatter and glob patterns (e.g., `**/*.test.tsx`, `src/api/**/*.ts`) enable deterministic, path-based convention application regardless of directory structure. This is the most supported approach for cross-cutting patterns like distributed test files.

### found-35 · Claude Code configuration and workflows

> Your team created a `/analyze-codebase` skill that performs deep code analysis—dependency scanning, test coverage counts, and code quality metrics. After running the command, team members report Claude becomes less responsive in the session and loses the context of the original task.
> How do you most effectively fix this while keeping full analysis capabilities?

- **Your answer:** C
- **Correct answer:** A
- **Explanation:** `context: fork` runs the analysis in an isolated subagent context so the large output does not pollute the main session’s context window and Claude does not lose track of the original task. It preserves full analysis capability while keeping the main session responsive.

### found-31 · Claude Code configuration and workflows

> You asked Claude Code to implement a function that transforms API responses into an internal normalized format. After two iterations, the output structure still doesn’t match expectations—some fields are nested differently and timestamps are formatted incorrectly. You described requirements in prose, but Claude interprets them differently each time.
> Which approach is most effective for the next iteration?

- **Your answer:** A
- **Correct answer:** B
- **Explanation:** Concrete input-output examples remove ambiguity inherent in prose descriptions by showing Claude the exact expected transformation results. This directly addresses the root cause—misinterpretation of textual requirements—by providing unambiguous patterns for field nesting and timestamp formatting.

---
*Generated by exam_prep.py · 2026-08-24T09:54:10*
