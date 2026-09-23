# Conversational Data Intelligence Agent
## Project Source of Truth (SOT)

**Document purpose:** This file is the authoritative, living implementation roadmap for the project. Update it as phases progress — flip statuses, log decisions, append dated notes. Do not let it drift out of sync with the code.
**Audience:** Claude Code, ChatGPT, Gemini, other coding agents, and the developer building the system.
**Revision note:** This is a resequenced version of the original plan. Content is preserved; phase order and a few phase boundaries changed to fix two structural risks: evaluation was scheduled too late to catch a stalled project, and RAG/LangGraph were scheduled as automatic builds rather than justified decisions. See "Resequencing rationale" below.

---

## 0. Status Snapshot

Update this table as work happens. This is the first thing to read to know where the project stands.

| Phase | Name | Status | Notes |
|---|---|---|---|
| 1 | Working SQL Assistant + Standing Eval Loop | Not started | |
| 2 | SQL Validation & Guardrails + Red-Team Suite | Not started | |
| 3 | Tool-Calling Agent | Not started | |
| 4 | Schema RAG + Semantic Layer | Not started | |
| 5 | Orchestration Decision Point | Not started | |
| 6 | Evaluation & Observability (deepened) | Not started | |
| 7 | Frontend + Demo | Not started | |
| 8 | Production Backend (optional/stretch) | Not started | |
| 9 | Deployment & CI/CD (optional/stretch) | Not started | |

Status values: `Not started` / `In progress` / `Blocked: <reason>` / `Done`.

---

## 0.1 Resequencing rationale

The original plan (Phases: Assistant → Tool-Calling → RAG → Guardrails → LangGraph → Production Backend → Evaluation → Enterprise/Deploy) had two structural risks:

1. **Evaluation was Phase 7, at the end.** If the project stalled anywhere before that (a real risk given the total scope), there would be no measured proof the system works — the exact failure the plan's own "measured, honest evaluation" pillar warns against. Fix: a minimal eval loop now starts in Phase 1 and every later phase re-runs and extends it, so there's always a number to quote.
2. **Guardrails were Phase 4, RAG was Phase 3, LangGraph was Phase 5 — all scheduled as automatic builds.** Guardrails protect every SQL-producing phase after it, so it should sit underneath tool-calling and RAG, not after them. RAG's own success criteria admit it needs a 20+ table schema to matter, which the 4-table Olist Phase-1 schema doesn't satisfy — left unresolved this phase would get faked or skipped. LangGraph's justification ("explicit stateful orchestration") is thinner than the plan's other tech justifications, so it's reframed as a decision gate: adopt it only if the hand-rolled agent loop's pain is real and documented.

Net effect: core path is now 1→2→3→4→5→6→7, each phase leaving a measured, defensible artifact behind instead of a single high-stakes eval phase at the end.

---

# 1. Project Vision

Build a production-oriented **Conversational Data Intelligence Agent** that allows users to ask questions about structured business data in natural language.

Example:

> "Which city has the most customers?"

The system should understand the question, determine the relevant database context, generate and validate SQL, execute it through a controlled database tool, validate the result, and return a natural-language answer.

The final system should demonstrate real AI engineering rather than being only a chatbot or a simple text-to-SQL demo.

The project should progressively introduce:

- Python engineering
- FastAPI
- SQL/database engineering
- LLM integration
- Tool calling
- Agent loops
- Schema retrieval / RAG
- SQL validation and guardrails
- LangGraph orchestration (if justified — see Phase 5)
- PostgreSQL
- Redis
- Authentication and authorization
- Async processing
- Evaluation
- Observability
- Frontend
- Docker
- Deployment

---

# 2. Core Product

## Product name

**Conversational Data Intelligence Agent**

The product is an AI-powered interface over structured business databases.

### User experience

The user asks:

> "Show me the top 10 customers by revenue this year."

The system should eventually:

1. Understand the request.
2. Retrieve relevant database schema/context.
3. Decide which tool(s) are needed.
4. Generate SQL.
5. Validate the SQL.
6. Execute it through a controlled database interface.
7. Validate the result.
8. Generate a grounded natural-language response.
9. Optionally generate a visualization.
10. Show useful execution metadata such as SQL, tables used, latency, and confidence/evaluation information.

---

# 3. Target Final Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │ API / Auth / Limits  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │      Agent Orchestrator     │
                    │   (hand-rolled or LangGraph)│
                    └─────────────┬───────────────┘
                                  │
                ┌─────────────────┼──────────────────┐
                ▼                 ▼                  ▼
        Schema Retrieval     SQL Generation      Tool Router
                │                 │                  │
                ▼                 ▼                  ▼
        Vector / Hybrid       LLM Provider      Tool Layer
          Retrieval                                │
                                                    ▼
                                          SQL Validation /
                                             Guardrails
                                                    │
                                                    ▼
                                            Read-only DB
                                                    │
                                                    ▼
                                           Result Validation
                                                    │
                                                    ▼
                                            Answer Generation
                                                    │
                           ┌────────────────────────┼──────────────┐
                           ▼                        ▼              ▼
                      Response                  Tracing        Metrics
                                                / Eval
                           │
                           ▼
                      React UI
```

This is the **target architecture**, not the architecture to build on day one. It must evolve incrementally, and the Orchestrator box is intentionally either/or — see Phase 5.

---

# 4. Engineering Principles

## 4.1 Build before abstracting

Build working behavior → understand it → refactor when complexity appears. Do not create abstractions before there is a real use case.

## 4.2 Understand every component

The developer must be able to explain: what the component does, why it exists, what calls it, what it calls, what data enters/leaves it, and why the architecture uses it. No black-box implementation is accepted simply because an AI coding agent generated it.

## 4.3 Phase boundaries are hard gates

Do not implement Phase N+1 until Phase N has: working code, tests, manual verification, clear understanding of the data flow, and documentation of important design decisions.

## 4.4 Do not add technology for resume decoration

Every technology must have a concrete reason (Redis → caching/state/rate limiting; RAG → retrieving relevant schema context; LangGraph → explicit stateful workflow *if the hand-rolled loop's pain is documented*; PostgreSQL → realistic relational production database; LangSmith → tracing/evaluation; Docker → reproducible deployment). Do not add a technology simply because it appears in job descriptions.

## 4.5 Security is part of the design

The LLM must never be treated as a trusted database administrator. Database access must be controlled by application-side policies — this is why guardrails now sit in Phase 2, ahead of every phase that generates SQL.

## 4.6 Differentiation strategy (what makes this project non-generic)

A generic "chat with a demo database" project is common. This project must stand out through practical depth. Six mandatory pillars:

1. **Real, messy, multi-table data.** Use a real public dataset with many tables and cryptic column names (see Section 14). Never demo on a toy customers/orders schema alone.
2. **Semantic layer.** Business metrics ("revenue", "active customer", "churned") are defined once in a YAML file and used by the agent instead of being guessed by the LLM (Phase 4).
3. **Clarify, don't guess.** Ambiguous questions trigger a clarifying question or an explicitly stated assumption (Phase 5).
4. **Evidence with every answer.** Each response exposes the SQL, tables used, assumptions, and result sanity checks (row count, NULLs, suspicious magnitudes) so the user can decide whether to trust it.
5. **Measured, honest evaluation.** A hand-written eval set (started Phase 1, extended every phase), ablation comparisons, and a published failure analysis including failures that were not fixed (Phase 6).
6. **Visible security story.** A red-team test suite with a published block rate (Phase 2).

Also required: a live demo link or a short demo GIF in the README. Reviewers rarely clone repositories.

## 4.7 Scope: core vs optional

- **Core (resume-ready):** Phases 1–7.
- **Optional / stretch:** Phase 8 (Redis, async workers, auth) and Phase 9 (Docker/CI/cloud deploy). These are generic backend work and must not delay the core phases.
- Do not add Kubernetes or multi-agent architectures.

## 4.8 Prompt versioning (cross-cutting, applies from Phase 1 onward)

Every eval run and ablation entry must record which prompt-template version produced it (a git tag, a hash, or a version string logged alongside results). Without this, the Phase 6 ablation table isn't reproducible — a score change could be retrieval quality or silent prompt drift, and you won't be able to tell which.

---

# 5. Phase Roadmap

---

# PHASE 1 — Working SQL Assistant + Standing Eval Loop

## Objective

Build the smallest complete end-to-end system, and start measuring it immediately — not in Phase 6.

The goal is NOT to build an agent yet. The goal is to understand the fundamental request flow, and to have a standing regression check from day one.

## Target flow

```text
User → FastAPI → LLM → SQL → Database → Query Result → LLM → Natural Language Answer
```

## Technology

Python, FastAPI, SQLite, LLM API, simple React frontend (stub is fine here), Pydantic, pytest.

Use a real public business dataset, not a hand-made toy database (see Section 14).

Recommended primary dataset: **Olist Brazilian E-Commerce**, loaded into SQLite.

Phase 1 uses only its four core tables: `customers`, `orders`, `order_items`, `products`. The remaining tables (payments, reviews, sellers, geolocation, category translation) are added in later phases.

## Backend responsibilities

### API

```http
POST /api/v1/query
```

Request:
```json
{ "question": "Which city has the most customers?" }
```

Response:
```json
{
  "question": "Which city has the most customers?",
  "sql": "...",
  "result": "...",
  "answer": "..."
}
```

### Database layer
Connecting to SQLite, reading schema, executing SQL, returning results — with column names attached to rows, not bare tuples, so downstream answer generation has field labels to work with.

### LLM layer
Receiving the question and schema, generating SQL, converting query results into a natural-language answer.

### Standing eval loop (new in this resequencing)
A small hand-written question set (8–15 questions covering simple lookups, aggregations, and one date filter) with a `pytest`-runnable script that executes each question end-to-end and reports:
- SQL execution success rate (did it run without error)
- Manual/LLM-graded answer correctness (rough is fine at this stage)

This script gets re-run and extended after every subsequent phase. It is the single most important artifact in the whole roadmap for proving the system works — do not defer it.

### Frontend
Minimal UI: question input, ask button, answer, optional SQL display.

## Phase 1 success criteria

These must work and pass through the eval script:
```text
"What city has the most customers?"
"What are the top 5 products by sales?"
"How many orders were placed last month?"
```

## What must be understood

Python classes, `__init__`, object creation, dependency injection basics, FastAPI routes, Pydantic models, database connections, SQL execution, LLM API calls, request/response lifecycle, frontend↔backend↔database data flow.

## Do NOT introduce yet

LangGraph, Redis, vector database, RAG, multi-agent architecture, Kubernetes, complex event queues, microservices.

---

# PHASE 2 — SQL Validation & Guardrails + Red-Team Suite

*(Moved ahead of tool-calling and RAG — see Resequencing rationale. Everything generated by an LLM downstream of this point is untrusted, so the guardrail layer needs to exist before the agent gets more sophisticated ways to produce SQL.)*

## Objective

Treat generated SQL as untrusted output, and prove it with a published block rate before building anything more complex on top.

## Target flow

```text
Generated SQL → SQL Parser / Validator → Policy Checks → Valid?
  ├── NO → Repair / Reject
  └── YES → Execute
```

## Required protections

SELECT-only policy, read-only database credentials, dangerous SQL detection (parse-based, not naive substring matching), SQL syntax validation, table allowlists, column restrictions, query timeout, result-size limits, maximum execution time, prompt-injection-aware handling, sensitive/PII column protection.

## Self-correction

```text
Generate SQL → Validate → Invalid → Send structured error to LLM → Repair SQL → Validate again → Execute
```

Hard retry limit required.

## Red-team suite

Automated adversarial test set (aim for 30+ cases) covering:
- Destructive SQL (DROP, DELETE, UPDATE, multi-statement)
- Prompt injection in the question ("ignore previous instructions...")
- Prompt injection hidden in data values returned by the database
- Requests for PII or restricted columns
- Requests for unauthorized tables
- Oversized or runaway queries

Report the block rate in the README. Target 100% for destructive SQL and unauthorized access. Document any case that gets through.

## Phase 2 success criteria

- Rejects destructive SQL.
- Rejects unauthorized tables/columns.
- Detects invalid SQL.
- Repairs recoverable SQL errors.
- Stops after a bounded number of retries.
- Never relies solely on the LLM to enforce safety.
- Published red-team block rate.
- Phase 1 eval script still passes (guardrails shouldn't break valid questions).

## What must be understood

Why LLM output cannot be trusted, defense in depth, SQL parsing, allowlisting, read-only database users, prompt injection, retry loops, failure handling.

---

# PHASE 3 — Tool-Calling Agent

*(Content unchanged from original plan; now sits atop a validated execution path from Phase 2.)*

## Objective

Transform the SQL assistant into a real tool-using agent instead of a single "generate SQL" prompt.

## Initial tools

```text
get_database_schema()
execute_sql(sql)
```

Potential future tools: `explain_sql(sql)`, `get_table_metadata(table)`.

## Target flow

```text
User → LLM/Agent → Tool decision → get_database_schema() → LLM → execute_sql(sql) → Database → Result → LLM → Final answer
```

## Tool calling requirements

The LLM produces structured tool calls, not arbitrary text:
```json
{ "tool": "execute_sql", "arguments": { "sql": "SELECT ..." } }
```
Python is responsible for actually executing the tool — it goes through the Phase 2 validator, not around it.

## Implement

Tool definitions, tool registry, tool router, structured arguments, tool execution, agent loop, tool errors, maximum iteration limit, final answer generation.

## Phase 3 success criteria

Receives a question, decides whether a tool is required, invokes it, receives tool output, continues reasoning, returns a final answer. Eval script re-run and extended with a tool-selection-accuracy check.

## What must be understood

What makes this different from a normal chatbot, what a tool call is, why the LLM should not execute Python itself, how structured arguments are validated, how tool results get back to the LLM, what happens when a tool fails, why an iteration limit is required.

---

# PHASE 4 — Schema RAG + Semantic Layer

*(The original plan's own success criteria admit RAG "adds no value" on a 4-table schema. This resequencing forces that decision here, explicitly, instead of leaving it unresolved.)*

## Objective

Make schema handling scalable, and prove retrieval actually helps — on a schema where it can.

## Schema-scale decision (resolve before starting this phase)

Olist (4–9 tables) is not large enough for retrieval to matter. Before writing retrieval code, decide and record here:
- [ ] Introducing a second, larger schema (TPC-DS via DuckDB, or a BIRD subset) specifically to demonstrate retrieval quality, alongside Olist for the semantic layer, **or**
- [ ] Some other resolution — document it.

## Schema ingestion

Extract table names, column names, data types, primary keys, foreign keys, relationships, descriptions/metadata where available.

## Schema documents

```text
Table: orders
Columns:
- order_id: integer, primary key
- customer_id: integer, foreign key → customers.customer_id
- order_date: date
- total_amount: decimal
```

## Retrieval

Given "Which customers haven't ordered anything recently?", retrieve `customers`, `orders`, `customer_id`, `order_date` — not the entire schema. Start with vector retrieval; later consider lexical, hybrid, metadata filtering, reranking.

## Semantic layer (business metrics)

A small YAML file defining business concepts once:

```yaml
metrics:
  revenue:
    definition: SUM(order_items.price)
    filters: orders.order_status != 'canceled'
  active_customer:
    definition: customer with at least one order in the last 90 days
  delivery_delay_days:
    definition: julianday(order_delivered_customer_date) - julianday(order_estimated_delivery_date)
```

The agent retrieves relevant metric definitions alongside schema context and must use them instead of inventing its own meaning of "revenue" or "active."

## Phase 4 success criteria

- Agent answers questions using only dynamically retrieved relevant schema context.
- Demonstrated on the larger schema chosen above (20+ tables) — not claimed as a feature on Olist alone.
- Metric definitions retrieved as part of context construction; generated SQL for metric questions matches the definition.
- **Ablation #1 recorded** (see Phase 6 table): full-schema-in-prompt vs. RAG vs. RAG+semantic-layer, measured against the standing eval set, not deferred to the end.

## What must be understood

Why RAG is useful here, what is being embedded, what is being retrieved, chunking strategy, embeddings, vector similarity, metadata, retrieval quality, context construction.

---

# PHASE 5 — Orchestration Decision Point

*(Reframed from "adopt LangGraph" to "decide whether to adopt LangGraph." Do not introduce LangGraph before understanding the workflow manually, and do not introduce it without a documented reason — see 4.4 and 4.8.)*

## Objective

Decide, with evidence, whether the hand-rolled agent loop from Phases 2–4 needs to become an explicit stateful graph.

## Decision gate

Before writing LangGraph code, document:
- What specific pain exists in the current hand-rolled loop (state threading across retries? conditional branching getting unreadable? repair-loop logic tangled with tool-calling logic?)
- Whether that pain is real enough to justify a new dependency, per 4.4.

If yes → implement the graph below. If no → keep the hand-rolled loop, document why, and move the saved time to Phase 6 or 7.

## Target graph (if adopted)

```text
START → Understand Question → Retrieve Schema → Generate SQL → Validate SQL
  ├── Invalid → Repair SQL → Validate
  └── Valid → Execute SQL → Validate Result → Generate Answer → END
```

## State

```python
class AgentState:
    question
    schema_context
    generated_sql
    validation_result
    query_result
    errors
    retry_count
    final_answer
```

## Clarification and assumptions

*(Applies regardless of whether LangGraph is adopted — this is a behavior requirement, not a LangGraph feature.)*

```text
Question analysis
 ├── Clear      → continue
 ├── Ambiguous  → ask a clarifying question OR proceed with a stated assumption
 └── Unanswerable / out of scope → explain why, do not generate SQL
```

Example: "top customers" is ambiguous (by revenue? by order count?). The agent must either ask or state "Assuming top = highest total revenue." Stated assumptions are stored in state and returned in the response.

## Evidence in the response

Every final response includes: generated SQL, tables and metrics used, assumptions made, result sanity checks (empty result, unexpectedly large values, NULLs from joins), latency.

## Phase 5 success criteria

Either: a documented, justified LangGraph adoption with explicit state/nodes/conditional routing/retry logic/failure paths — or a documented decision to keep the hand-rolled loop, with the same behavioral guarantees (clarify/assume routing, evidence in response). Both outcomes are acceptable and defensible; an undocumented default is not.

## What must be understood

State, nodes, edges, conditional edges, graph execution, state mutation, retry loops — and, regardless of the decision, why (or why not) LangGraph earns its place for this specific workflow.

---

# PHASE 6 — Evaluation & Observability (deepened)

*(Was the original Phase 7. Because the eval loop has been running and growing since Phase 1, this phase is a finishing/deepening pass, not a from-scratch build under deadline pressure.)*

## Objective

Turn the incremental eval numbers gathered since Phase 1 into a complete, honest measurement story.

## Evaluation dataset

Extend the Phase 1 set into a curated dataset with: question, expected tables, expected SQL characteristics, expected result, expected answer, difficulty. Include ambiguous questions, multi-table joins, aggregations, date filtering, nested queries, invalid requests, unauthorized requests.

## Metrics

SQL execution success rate, SQL correctness, answer correctness, schema retrieval accuracy, tool-call accuracy, retry rate, failure rate, latency, token usage, cost, query execution time.

## Ablation table

Publish in the README (Phase 4's ablation should already be filled in by this point):

| Configuration | Execution success | Answer correctness |
|---|---|---|
| Full schema in prompt | | |
| Schema RAG | | |
| Schema RAG + semantic layer | | |
| Schema RAG + semantic layer + repair loop | | |

Publish a failure analysis: categorize remaining wrong answers (ambiguity, wrong join, wrong metric, retrieval miss) and state which were not fixed. Optionally benchmark a subset of BIRD or Spider dev questions.

## Observability

Introduce tracing (LangSmith or equivalent) across: request → agent → schema retrieval → LLM call → SQL validation → SQL execution → retry → final answer.

## Phase 6 success criteria

The project can answer "How do you know your agent works?" with measurements, not "I tested it manually."

---

# PHASE 7 — Frontend + Demo

*(Pulled forward from the end of the original Phase 8 — this is what makes the project reviewable by someone who won't clone the repo, so it should land before any optional backend infra.)*

## Objective

Turn the engineering system into something a reviewer can look at in under a minute.

## Frontend

Chat/query interface, conversation history, SQL viewer, result table, charts, query explanation, tables used, execution time, loading states, error states, feedback mechanism.

```text
┌─────────────────────────────────────────────┐
│ Conversational Data Intelligence            │
├─────────────────────────────────────────────┤
│ Ask your data...                            │
│ "Revenue by region this quarter"            │
│                              [Ask Agent]    │
├─────────────────────────────────────────────┤
│ Answer                                      │
│ North: ₹12.4M   South: ₹9.8M                │
├─────────────────────────────────────────────┤
│ Generated SQL                               │
│ SELECT region, SUM(revenue)...              │
├─────────────────────────────────────────────┤
│ Data Sources: orders • customers            │
├─────────────────────────────────────────────┤
│ Visualization              [Chart]          │
└─────────────────────────────────────────────┘
```

## Phase 7 success criteria

A live demo link or a short demo GIF exists in the README (required per 4.6 — reviewers rarely clone repositories).

---

# PHASE 8 — Production Backend (optional / stretch)

> Start only after Phases 1–7 are complete and measured.

## Objective

Turn the prototype into a production-oriented backend.

## Database

SQLite → PostgreSQL.

## Redis

Concrete use cases only: caching repeated/semantically-equivalent queries, short-lived conversation state, rate limiting. Do not use Redis merely because it is popular.

## Authentication

```text
User → Authentication → Authorization → Agent
```
Potential model: User / Role / Permissions / Data Access Policy.

## Async execution

```text
FastAPI → Job creation → Queue → Worker → Agent → Database
```
The API should not block indefinitely on expensive work.

## Phase 8 success criteria

PostgreSQL, authentication, authorization, rate limiting, caching, conversation state, async jobs where needed, structured error handling, configuration management, environment-based secrets.

---

# PHASE 9 — Deployment & CI/CD (optional / stretch)

> Docker Compose, CI/CD, and cloud deployment are stretch goals.

## Containerize

FastAPI, Worker, React, PostgreSQL, Redis. Docker Compose initially; optionally deploy to cloud.

## CI/CD

Linting, formatting, unit tests, integration tests, evaluation tests, build checks.

## Phase 9 success criteria

A new developer can: clone repository → configure environment → run Docker Compose → open application → ask questions → observe the agent.

---

# 6. Testing Strategy

Testing must grow with the project.

**Unit tests:** SQL validator, schema parser, retrieval functions, tool functions, database layer, authentication, utility functions.

**Integration tests:** `API → Agent → Tool → Database`.

**Agent tests:** correct tool selection, SQL generation, retry behavior, failure handling, invalid questions.

**Security tests:** destructive SQL, unauthorized tables, unauthorized columns, prompt injection attempts, oversized queries, rate limits.

**Evaluation tests:** against the curated question dataset (standing since Phase 1).

---

# 7. Repository Evolution

## Phase 1 shape

```text
project/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── database/
│   ├── models/
│   └── llm/
├── frontend/
├── tests/
├── data/
├── .env.example
├── pyproject.toml
├── README.md
└── SOT.md
```

## Later phases — possible final structure

```text
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── agents/
│   │   ├── graph/
│   │   ├── tools/
│   │   ├── retrieval/
│   │   ├── database/
│   │   ├── guardrails/
│   │   ├── auth/
│   │   ├── services/
│   │   ├── workers/
│   │   └── models/
│   └── tests/
├── frontend/
├── data/
├── evaluation/
│   ├── datasets/
│   ├── evaluators/
│   └── reports/
├── scripts/
├── docker/
├── docs/
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── README.md
└── SOT.md
```

This is a target, not a requirement to create everything immediately.

---

# 8. Definition of Done

**Functionality:** natural-language database questions work; SQL is generated, validated, executed through controlled tools; results are validated; answers are grounded in database results.

**Agent:** structured tool calling; explicit state; handles failures; bounded retries; schema retrieval; a documented orchestration decision (hand-rolled or LangGraph, per Phase 5).

**Security:** database access controlled; destructive queries blocked; unauthorized data access blocked; sensitive data policies exist; rate limiting exists.

**Engineering:** PostgreSQL, Redis, FastAPI, automated tests, Docker, configuration management, structured logging, error handling. *(Stretch — Phases 8–9.)*

**AI Engineering:** Schema RAG, tool calling, agent orchestration, SQL validation, self-correction, evaluation, tracing, cost/latency measurement.

**Differentiation:** real multi-table dataset; semantic layer with measured impact; clarification/stated-assumption behavior; evidence shown with every answer; ablation table and failure analysis in the README; red-team suite with published block rate; public demo link or GIF.

**Product:** professional frontend, query history, SQL visibility, results visualization, error handling, deployment instructions. *(Frontend/demo — Phase 7 core; deployment instructions — Phase 9 stretch.)*

---

# 9. Interview Readiness

**Python:** classes, constructors, dependency injection, async programming, error handling, type hints, project structure.

**FastAPI:** routes, Pydantic, dependencies, middleware, authentication, async endpoints.

**Databases:** SQL, joins, indexes, transactions, PostgreSQL, connection pooling, query optimization.

**GenAI:** LLM APIs, prompt design, structured output, tool calling, context management, embeddings, RAG, hallucination mitigation.

**Agents:** agent loops, tool selection, state, LangGraph (if adopted — and why, if not), conditional routing, retry/recovery.

**Production AI:** evaluation, observability, latency, token cost, guardrails, security, rate limiting, caching.

---

# 10. Rules for AI Coding Agents

This section is specifically for Claude Code, Codex, Gemini, or other coding agents working on this repository.

**Rule 1 — Read this file first.** Before modifying the project, read this document. It is the project's source of truth.

**Rule 2 — Determine the current phase.** Inspect the repository, check the Status Snapshot (Section 0), identify the next incomplete phase. Do not implement future-phase features unless explicitly requested.

**Rule 3 — Explain before major changes.** For significant architectural changes: what is changing, why it is needed now, which files will change, how request/data flow will change, what new dependency is being introduced.

**Rule 4 — Do not rewrite working code unnecessarily.** Preserve working functionality. Prefer incremental changes.

**Rule 5 — Do not over-engineer.** If the current phase can be solved with 1 service, do not create 7 microservices.

**Rule 6 — Write tests with features.** Every meaningful backend feature should have tests.

**Rule 7 — Keep the developer involved.** After implementing a significant component, explain in practical terms: who calls this, why does it exist, what goes in, what comes out, what happens when it fails.

**Rule 8 — Never hide implementation behind abstractions.** If a framework performs important work, explain what it is doing conceptually.

**Rule 9 — Preserve the learning objective.** This project is simultaneously a portfolio project, an interview project, a Python learning project, an AI engineering learning project, and a production architecture exercise. The implementation must support all five.

**Rule 10 — Keep this file current.** After completing meaningful work on a phase, update Section 0's status and append an entry to Section 15 (Progress Log). This file is only useful as a source of truth if it reflects reality.

---

# 11. Current Execution Rule

At the beginning of the project, work ONLY on **Phase 1**: build a minimal working Conversational SQL Assistant with a standing eval loop.

Do not implement RAG, LangGraph, Redis, PostgreSQL, multi-agent systems, complex queues, Kubernetes, or advanced observability until the appropriate phase.

The project should grow naturally, and this section should be updated to point at whichever phase is currently active as the project progresses.

---

# 12. Final Project Narrative

> "I built a conversational data intelligence system that allows users to query structured business data using natural language. I evaluated the system from the first working version onward, not just at the end — every phase re-ran a standing eval set so I always had a measured accuracy number. The system uses schema retrieval to provide relevant database context to an LLM, structured tool calling to interact with the database, and SQL validation and guardrails — built before the agent got more sophisticated, not after — with a published red-team block rate to prevent unsafe execution. I made a deliberate, documented decision about whether a stateful graph orchestrator was worth the complexity over a hand-rolled agent loop. I measured the impact of retrieval and a semantic layer with an ablation table, and published a failure analysis of what still doesn't work. The system is exposed through a FastAPI backend with a frontend demo, and [PostgreSQL, Redis, authentication, async execution, containerization — if built]."

The implementation must support this statement truthfully. Update it if the project's actual shape diverges from it.

---

# 13. Golden Rule

**Do not optimize for the number of technologies. Optimize for depth of understanding and engineering quality.**

A smaller system that the developer can explain line-by-line is more valuable than a huge system generated by an AI coding agent that the developer cannot defend in an interview.

Build it. Understand it. Test it. Measure it. Then make it more sophisticated.

---

# 14. Data Sources

Verify each dataset's license and terms on its own page before use. Do not commit large data files to the repository. Provide a download/load script instead.

## Primary (business domain, semantic layer)

- **Olist Brazilian E-Commerce Public Dataset** (Kaggle). ~100k real orders across 9 relational tables: customers, orders, order items, payments, reviews, products, sellers, geolocation, category translation. Good for revenue, delivery delay, review score, and seller questions.

## Evaluation and schema-scale testing

- **BIRD benchmark** (bird-bench.github.io). Multi-table databases with question/SQL pairs and messy real-world values. Use a subset for external benchmarking.
- **Spider** (yale-lily.github.io/spider). Question/SQL pairs across many small databases.
- **TPC-DS** (generated with DuckDB's `tpcds` extension). ~24 tables with cryptic column names. Use it to stress-test schema retrieval (Phase 4).

## Optional second database (India-specific, multi-database routing)

- **IPL ball-by-ball data from Cricsheet** (cricsheet.org). Free match and delivery data. Supports questions such as "Who has the best strike rate in death overs?". Could be added as a second database to demonstrate database routing.
- **data.gov.in** and NPCI monthly UPI statistics: aggregate open data. Usually single-table, so use only as supplementary data.

## Smoke testing only

- **Chinook** and **Northwind**: small sample databases. Fine for quick tests, not for the resume demo.

## Recommendation

Olist as the primary database, BIRD subset plus TPC-DS for evaluation and schema scale (Phase 4), IPL as an optional second database.

---

# 15. Progress Log

Append a dated entry here every time meaningful work lands. Keep entries short — what changed, what was learned, what's next.

- *(empty — first entry goes here when Phase 1 work begins)*
