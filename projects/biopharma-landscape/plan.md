# Biopharma AI Observatory — Project Plan & Working Contract

**Project path:** `ai-scientist-lab/projects/biopharma-landscape/`  
**Status:** Milestone 1 in progress; initial OpenAlex → SQLite → Streamlit flow implemented locally and reported working  
**Plan established:** 2026-10-17  
**Purpose of this file:** Persistent source of truth for subsequent coding sessions. Read it before proposing architectural changes, implementing new components, or altering the milestone sequence.

## 1. Non-negotiable outcomes

Build **both**, rather than optimising for only one:

1. **Working, showcase-quality, continuously maintained public utility:** A *Biopharma AI Observatory* that visitors can use to explore the AI activities of pharmaceutical companies, research papers, AI-native biotech/startups, technology platforms, scientific leaders, and industry partnerships. It must have a usable website, browsable source-backed data, comparative intelligence, an AI research assistant, and linked living reports. The public product must be neutral and **must not mention or appear tailored to Pfizer**.
2. **Hands-on agent engineering learning system:** Implement, instrument, exercise, and evaluate all of the key agentic AI and systems concepts below. The goal is to understand their mechanics through code, trade-offs, failure cases and reproducible experiments, not simply integrate a large framework.

**Secondary future capability:** Reuse the general-purpose code in a separately approved enterprise deployment, with organization-specific agents, R&D targets, access controls and internal data. The public project will never ingest or reveal confidential employer information. Internal enterprise use must comply with employer IP, security and open-source policies. Do not add Pfizer-specific logic or positioning to the public observatory.

**Workflow instruction:** The user writes/runs code locally with interactive guidance. **Do not push, commit, or otherwise modify GitHub repositories or blog content unless the user later explicitly requests this.** Do not make blog updates during the build by default.

**Software Engineering Excellence** All code must meet high production engineering standards. Every milestone should include consistent automated formatting and linting, appropriate type annotations, modular design, meaningful unit and integration tests, robust error handling, secure configuration, and reproducible development workflows.

Use Ruff for formatting and linting, pytest for tests, and introduce static type checking, pre-commit hooks and CI as the project matures.

Features are not complete merely because they execute successfully. Engineering quality must be validated alongside functional correctness. Code quality improvements must be applied incrementally rather than postponed until the end.

## 2. Public product requirements

The site should ultimately have these **six visible capabilities**:

| Surface | Minimum useful output |
|---|---|
| Company landscape | Searchable company profiles; AI leadership; scientific initiatives; systems; model work; partnerships; dated updates; sources |
| Paper radar | Recent papers by topic, author, institution and organisation; abstracts/metadata; why interesting; source links; new-since-last-run tracking |
| Startup/technology radar | Profiles of emerging biotechs, university spinouts, scientific labs, models, platform vendors and technology capabilities |
| Research assistant | Ask cross-document/company questions; hybrid retrieval; grounded answers with explicit citations, uncertainty and traceable evidence |
| Living updates | Incremental discovery; event and entity changes; timelines; freshness indicators; operational status |
| Reports | Browse and share dated reports, comparisons and evidence-backed research briefs with links from the site |

### Initial coverage

Start narrow and expand through the pipeline. Track large pharma including Pfizer, Lilly, Merck/MSD, GSK, AstraZeneca, Roche/Genentech, Novartis, Sanofi, BMS, J&J, Amgen, AbbVie, Novo Nordisk, Takeda and additional companies. Follow relevant AI/biology startups, university spinouts, research teams and partnerships. Follow published papers, conference output, preprints, models, benchmarks and selected patents where feasible.

**Evidence rule:** Distinguish (a) announced intentions or company claims, (b) published technical evidence, (c) independently validated outcomes, and (d) our own inference. Every substantive derived claim needs provenance, date checked and uncertainty where appropriate. Never invent partnerships, scientific outcomes, leaders, model benchmarks or financial figures.

## 3. Engineering coverage: every topic must be touched, tested, and demonstrated

| Topic | Required implementation/exercise | Proof/acceptance evidence |
|---|---|---|
| Agent loops | Custom plan → tool call → observation → reflection/replan → stop cycle; bounded budgets | Inspectable multi-step trace with termination conditions |
| Memory | Durable tasks, entity knowledge, event history, versioned facts / evolving beliefs | Knowledge persists across restarts and updates without erasing history |
| RAG / embeddings | Document parsing, chunking, embeddings, hybrid lexical/vector search, optional reranking | Retrieval benchmark (e.g. recall@k), citations trace to chunks |
| Evaluation | Grounded claims, source coverage, freshness, completeness, latency/cost and human review | Repeatable test set, scorecard and regression baseline |
| Self-healing | Tool timeouts/retries, idempotency, leases/checkpoints, crash recovery, dead-letter/error handling | Inject failures and demonstrate recovery without duplicates |
| Multi-agent systems | Specialist discovery/research/analyst/verifier and explicit handoffs | Quantitative/qualitative comparison with a single-agent baseline |
| Model routing | Local open-weight model and optional hosted or GPU-served models; route by quality/privacy/cost | Recorded routing decisions and quality/latency/cost comparison |
| Enterprise architecture | Pluggable tools/agents, environment separation, permissions, isolation, provenance and auditability | Separate deployment configs; tests for boundary enforcement |
| Observability | Run IDs, execution traces, tool invocations, token and cost accounting | Run history and traces inspectable from logs/UI |
| Living workflows | Scheduled discovery, checkpoints, watermark/overlap logic, deduplication and change detection | Repeated updates ingest new evidence without duplicating old items |
| Scientific intelligence | Papers, models, pharma initiatives, relationships and partnerships | Source-backed company comparisons and relevant research reports |

Additional necessary foundations: structured extraction and schema validation, secure secrets management, local data storage, retrieval evaluation, human-in-the-loop review, and reproducible environment setup.

**Coverage constraint:** Do not quietly drop a topic for speed. It may be implemented minimally first and expanded later, but must have a working demonstration before the project is called complete.

## 3A. Software engineering excellence — non-negotiable

Code quality is a project outcome, not a final cleanup task. For every increment:

- Run Ruff formatting and linting; keep imports and code style consistent.
- Use precise type annotations and mypy checks on the backend, with clear interfaces and responsibilities.
- Write isolated unit and integration tests, including negative paths and failure scenarios; never treat an unrun test as passing.
- Manage database connections, transactions, configuration, logging, API failures and secrets correctly.
- Prefer small, maintainable modules and explicit abstractions over premature complexity.
- Document reproducible run/test commands; verify clean-install and restart behaviour.
- Before calling a feature complete, run `ruff format --check .`, `ruff check .`, `mypy src/biopharma` and `python -m pytest -v`, plus the app smoke test. Record results in `PROGRESS.md`.

## 4. Recommended technical stack (starting defaults, not dogma)

- **Language / packaging:** Python with `pyproject.toml`, modular `src/` package, pytest.
- **Local app / API:** Streamlit for fast usable UI; FastAPI API. Later consider Next.js for polished public presentation.
- **Structured storage:** SQLite initially; source documents on local disk; optional PostgreSQL when concurrency/deployment needs justify it.
- **Retrieval:** SQLite FTS5 + Sentence Transformers embeddings; initially simple local vector storage, then FAISS/Qdrant/pgvector and reranking as justified.
- **LLM:** Locally served open-weight Qwen through Ollama initially; test vLLM/rented GPUs or hosted models and model routing later.
- **Harness:** Custom Python loop first. Compare LangGraph or another framework after gaining a working baseline.
- **Jobs:** SQLite-backed durable work queue first; add Redis/distributed workers only to learn scaling or when measured requirements demand it.
- **Observability:** Structured JSON execution traces, run history, then OpenTelemetry when practical.
- **Ingestion:** Prefer stable APIs such as OpenAlex/arXiv for papers; official company/partner sources for announcements; persist source metadata and raw artefacts.

**Architecture rule:** Keep public shared platform logic separate from future private enterprise deployment layers. No internal data flows to the public instance.

## 5. Proposed repository structure

```text
ai-scientist-lab/
└── projects/
    └── biopharma-landscape/
        ├── PROJECT_PLAN.md               # This file: canonical project contract
        ├── README.md
        ├── pyproject.toml
        ├── apps/
        │   ├── api/
        │   └── web/
        ├── src/
        │   └── biopharma/
        │       ├── agents/
        │       ├── harness/
        │       ├── ingestion/
        │       ├── retrieval/
        │       ├── models/
        │       ├── storage/
        │       ├── evaluation/
        │       └── reporting/
        ├── config/
        ├── data/                         # Gitignored where appropriate
        ├── tests/
        ├── experiments/
        └── docs/
```

Implementation code belongs in `src/`; experimental notebooks/benchmarks belong in `experiments/`; user-facing app in `apps/`. Keep package imports and runtime configuration consistent. This directory sketch can evolve if a specific technical reason is documented.

## 6. Build milestones and deliverables

Time windows below assume approximately 1–2 hours a day and are **planning estimates, not deadlines**. At the end of every milestone, the app should become more useful. Do not build many disconnected tutorials instead of one evolving product.

### M1 — Working Observatory (Weeks 1–2)

- Scaffold Python project and reproducible local environment.
- Fetch actual papers using OpenAlex or arXiv, preserving stable IDs, publication dates and source links.
- SQLite schema for papers, company registry and ingestion metadata.
- Build minimal FastAPI endpoints and Streamlit UI to browse/filter papers and organisations.
- Re-run ingestion and prove deduplication and persistence across restart.

**Demo:** A browser shows real persisted papers and company records, and refreshing does not create duplicates.

### M2 — Intelligent Research Assistant (Weeks 3–4)

- Download/extract allowed documents with provenance; create chunks and embeddings.
- Hybrid retrieval (keyword + vector) and evaluation cases.
- Serve an open-weight LLM locally; implement a custom bounded tool-using agent loop.
- Citation-grounded answers, source inspection and tool/model traces.

**Demo:** Ask a research question; get an answer supported by real stored sources, with an inspectable retrieval and agent trace.

### M3 — Living, Reliable Agents (Weeks 5–6)

- Durable run state, scheduled updates, watermarks, incremental refresh and change history.
- Retries, timeouts, checkpoints, task claiming, idempotency, crash/restart recovery.
- Eval set for correctness, evidence support, coverage and freshness.

**Demo:** After a simulated retrieval failure or worker crash, the system resumes safely; new papers and events appear without duplicates.

### M4 — Multi-Agent Intelligence (Weeks 7–8)

- Separate discovery, specialist research, analysis and verification roles.
- Agent handoffs and explicit stop criteria; route between model choices.
- Compare results against single-agent baseline; produce company comparisons, technology assessments and reports.

**Demo:** A cited report can be generated reproducibly; multi-agent quality, cost and latency are compared to the baseline.

### M5 — Showcase and Enterprise Readiness (Weeks 9–10)

- Polish navigation, profiles, paper/startup radar, assistant, updates and report links.
- Deploy a public site with an actual data refresh process and operational visibility.
- Add access/configuration separation, auditability, privacy controls and documentation.
- Prepare reproducible demos and record architectural tradeoffs and technical learnings.

**Demo:** A visitor can use a public, neutral, dated and source-backed observatory; developer documentation demonstrates core agentic mechanics and evaluations.

## 7. Immediate first coding session — vertical slice

**Do next:** Implement the smallest end-to-end path from paper API → normalization → SQLite → Streamlit browser → second run without duplicates. Specifically:

1. Scaffold `pyproject.toml` and folders; create Python environment.
2. Query OpenAlex for biological foundation-model papers.
3. Normalize paper ID, title, abstract (if available), authors, date, URL, source and ingestion time.
4. Persist to SQLite, with unique constraint based on stable ID and a sensible fallback.
5. Expose and filter papers in a minimal Streamlit app (and a thin FastAPI endpoint if practical).
6. Test restart persistence and duplicate-free re-ingestion.

**Defer intentionally:** sophisticated agent loops, multi-agent orchestration, distributed queues and polish until this first working slice exists. This is a sequencing choice, **not** a reduction of scope.

## 8. Working rules / deviation control

1. **One integrated product:** Every exercise contributes to the same working observatory, unless clearly marked as a controlled benchmark in `experiments/`.
2. **Two progress lenses:** Always track **product capability** and **engineering concepts validated**.
3. **Milestone gates:** Do not mark milestones done without a runnable demo, reproducible command, and tests or evaluation output.
4. **No scope dropping:** All topics in §3 remain on the checklist. If sequencing changes, explicitly state why and update this file only with user approval.
5. **Evidence before conclusions:** Distinguish sourced claims from extrapolation; show uncertainty, limitations and publication/check dates.
6. **Local-first:** Code locally with user guidance. **No unsolicited GitHub pushes, commits, edits, or blog publishing.**
7. **Neutral public positioning:** No employer-specific framing in the public website. Keep any future internal deployment separate and appropriately approved.
8. **Keep the system living:** Persist state, history, job progress and change tracking. A static scraped report is not completion.
9. **Understand before abstracting:** Implement simple harness mechanics first; use large frameworks only after measuring the trade-offs.
10. **Showcase quality matters:** Every major step should support a demonstrable user experience; do not build only invisible infrastructure.
11. **Controlled changes:** When suggesting a scope or architecture change, label it **proposed deviation**, articulate benefits/costs, and seek user agreement before revising this working contract.
12. **Session continuity:** At the start of future project sessions, read `PROJECT_PLAN.md` and any `PROGRESS.md` before deciding what to implement next. If the file isn't available in conversation context, ask for the current copy rather than assuming it can be accessed automatically.

## 8A. Implementation checkpoint — 2026-10-17

**Reported working (user-confirmed locally):**
- Project scaffold and editable Python packaging were started.
- OpenAlex client fetches and normalizes publication metadata to a typed `Paper` record.
- SQLite persistence and ID-based duplicate suppression are implemented.
- Streamlit Paper Radar was exercised successfully, and the work was checked in to GitHub.
- Ruff / VS Code formatting was configured; `mypy` and `pytest` dependencies and test files were added.

**Verification status:** These are implementation / user reports, not a completed M1 gate. The reviewed GitHub files reveal corrections required before quality checks can be treated as passing. Test commands have **not** been independently executed; do not assume they pass.

**Code-review corrections to make before moving forward:**
1. In `src/biopharma/storage/database.py`, `save_papers()` and `get_papers()` must call `connect_db(db_path)`, not `connect_db()`, to respect test and deployment database isolation.
2. In `tests/test_database.py`, import and use `initialize_db()` (the actual function), instead of `initialize()`.
3. In `pyproject.toml`, fix the build metadata to use `[build-system]` and `build-backend = "setuptools.build_meta"`. The checked-in file currently has `build_backend` as an incorrect top-level key.
4. In `apps/web/app.py`, call `initialize_db()` during initial setup, so a clean installation can open the app with no pre-existing database.
5. Re-run the entire app and check `ruff format --check .`, `ruff check .`, `mypy src/biopharma`, `python -m pytest -v`. Fix any newly surfaced problems before closing the checkpoint.

**Next session:**
- First resolve the four code-review issues above and record actual test output in `PROGRESS.md`.
- Then resume M1 with the company registry and minimal FastAPI endpoint as planned, or explicitly document any agreed sequencing change.
- After the M1 acceptance gate, start the durable stateful research-execution harness: task lifecycle, atomic claiming, retries, checkpoints, idempotency and crash recovery. These are the foundations for living paper, company and startup agents.
- No public website/blog changes are required yet. Future enterprise use remains separate from the public project.

**Milestone state:** M1 **in progress**, not complete. No requirements or engineering learning topics have been removed.

## 9. Progress log format (maintain in `PROGRESS.md` once coding starts)

```markdown
# Progress

## Current milestone
M1 — Working Observatory

## Product capabilities working
- [ ] Real paper ingestion into persistent DB
- [ ] Company registry
- [ ] Local website browsing and search

## Engineering demonstrations completed
- [ ] Idempotent ingestion
- [ ] Persistence across restart

## Tests / evidence
- Command:
- Result:

## Next smallest runnable step
- ...

## Decisions and tradeoffs
- ...

## Proposed deviations (require agreement)
- None
```

## 10. Completion checklist

- [ ] Publicly usable, neutral observatory website
- [ ] Company profiles, paper radar, startup radar, partnerships, reports
- [ ] Evidence-backed AI research assistant with hybrid RAG and local model inference
- [ ] Scheduled incremental updates and durable state/history
- [ ] Agent loop planning/tool calling/reflection/termination demo
- [ ] Memory and evolving evidence demo
- [ ] Retrieval and claim-level evaluation suite
- [ ] Crash/retry/self-healing demonstration
- [ ] Multi-agent comparison to baseline
- [ ] Model routing comparison and traces
- [ ] Enterprise-ready separation/permissions/auditability demonstration
- [ ] Reproducible docs, tests, benchmarks and deployment instructions

**Project principle:** Build a useful, living biopharma intelligence product **and** learn the complete agentic systems stack by implementing, testing and showcasing each core capability.