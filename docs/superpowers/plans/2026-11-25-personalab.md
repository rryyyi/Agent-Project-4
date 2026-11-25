# PersonaLab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Deliver a runnable, reproducible persona-driven behavioral simulation platform and publish it to the requested GitHub repository.

**Architecture:** Pydantic contracts and pure scenario functions feed a bounded asynchronous experiment engine. Providers return validated JSON decisions; SQLite stores final runs and per-attempt traces. FastAPI, a bundled browser console, and a CLI expose the same services.

**Tech Stack:** Python >=3.11, FastAPI, Pydantic v2, httpx, SQLite, pytest, Ruff, HTML/CSS/JavaScript.

**Spec:** `docs/superpowers/specs/2026-11-25-personalab-design.md` (approved by user: “按这个做”).

## Global Constraints

- Public repository excludes resume and personal contact information; dates are real.
- Offline demonstrations and actual LLM runs are explicitly distinguished.
- Same offline config/seed reproduces decisions and metrics, not IDs/timestamps.
- Bounded rounds, agents, concurrent calls, timeout, retries and total call budget.
- No real model performance or production deployment claims without evidence.
- Local single-user deployment; no account system or distributed infrastructure.
- A/B outcomes describe synthetic populations, not causal effects on real people.
- No subagent tool available: execute inline and conduct a separate self-review.

## Review Focus

- NaN, extra fields and duplicate persona IDs must fail validation (Task 1).
- Malformed model output, timeouts and exhausted budgets must terminate with diagnostic traces, without hidden offline fallback (Task 2).
- Provider errors may contain secrets; public runs must expose sanitized error categories only (Tasks 2, 4).
- Literature excerpts must be grounded in a verifiable source location, including Unicode/PDF text; no invented citations (Task 3).
- HTML-like model explanations must display as text and unknown runs must return 404 (Task 4).

## File Structure

- `pyproject.toml`, `.gitignore`, `.env.example`: packaging and local configuration.
- `src/personalab/schemas.py`, `personas.py`, `scenarios.py`: validated models, registry and payoff rules.
- `src/personalab/data/personas.json`: versioned synthetic persona examples.
- `src/personalab/prompts.py`, `providers.py`: prompt boundary and provider protocol/adapters.
- `src/personalab/engine.py`, `evaluation.py`, `storage.py`, `reports.py`: execution, metrics, persistence and exports.
- `src/personalab/literature.py`: source-grounded extraction and PDF/text loading.
- `src/personalab/api.py`, `cli.py`, `static/*`: service, command-line and UI.
- `tests/test_domain.py`, `test_engine.py`, `test_literature.py`, `test_api.py`, `test_cli.py`: behavior regression suites.
- `README.md`, `README.en.md`, `docs/*`, `examples/*`: onboarding, reproducibility and engineering explanations.
- `.github/*`, `Dockerfile`, `compose.yaml`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`: delivery and maintenance.

### Task 1: Validated personas and scenario mechanics

**Files:** `pyproject.toml`, `.gitignore`, `src/personalab/{__init__,schemas,personas,scenarios}.py`, `src/personalab/data/personas.json`, `tests/test_domain.py`.

**Interfaces:** `Persona`, `ExperimentConfig`, `Decision`; `load_personas() -> dict[str, Persona]`; `context_for(config, persona, history, variant) -> dict`; `validate_action(scenario, action) -> float`; `settle(scenario, actions) -> list[float]`.

- [x] Write tests rejecting nonfinite traits, unknown fields, duplicate IDs, too-large workloads, and invalid scenario actions; assert public-goods payoffs `[18, 8]` for contributions `[0, 10]` with multiplier 1.6 and endowment 10; trust transfer 4 and return fraction .5 yields investor 12 and trustee 6.
- [x] Run `python -m pytest tests/test_domain.py -q`; expect missing module/feature failure.
- [x] Implement strict models, four synthetic personas, JSON registry, three scenarios (public_goods, trust_game, product_ab). Trust interaction uses investor transfer and trustee return, represented as paired scenario stages.
- [x] Run `python -m pytest -q`; expect all domain tests pass.
- [x] Commit `feat: model personas and behavioral experiment environments`.

### Task 2: Bounded execution, provider adapters, metrics and storage

**Files:** `src/personalab/{prompts,providers,engine,evaluation,storage,reports}.py`, `tests/test_engine.py`.

**Interfaces:** async `Provider.decide(request: dict) -> ProviderResponse`; `OfflineProvider`, `OpenAIProvider`; async `run_experiment(config, registry, provider) -> dict`; `Store.save(run)`, `Store.get(run_id)`, `Store.list(limit)`; `markdown_report(run) -> str`.

- [x] Test deterministic complete offline runs for all scenarios; bounded history; independent repetitions; simultaneous public-goods observations; product A/B matching and paired confidence interval; invalid JSON retry recovery; unrecoverable and timeout failures; call-budget cap; sanitized errors; SQLite reload and report provenance. Use httpx MockTransport only at network boundary to check real adapter request/response contracts, 429 handling and usage.
- [x] Run `python -m pytest tests/test_engine.py -q`; expect missing engine/provider feature failure.
- [x] Implement deterministic per-unit RNG, persona-based offline policies, structured prompt compiler, JSON-validating real adapter, bounded retry/concurrency, two-stage trust game, attempt ledger and terminal statuses. Derive output schema in prompt; usage includes failed validation attempts. Never switch providers after failure.
- [x] Compute legal decision rate, action distributions, per-persona summaries, cooperative alignment proxy, A/B paired unit means and Student-t/normal approximation interval clearly labeled; tokens and elapsed statistics.
- [x] Persist complete terminal run JSON atomically using SQLite; emit escaped/safe Markdown summaries with provenance, config and limits.
- [x] Run `python -m pytest -q`; expect green; commit `feat: add reproducible agent execution and experiment observability`.

### Task 3: Grounded literature extraction

**Files:** `src/personalab/literature.py`, `tests/test_literature.py`, `examples/literature/*`.

**Interfaces:** `read_document(path: Path) -> str`; `extract_evidence(text, source, keywords) -> list[dict]`; `validate_evidence(text, start, end, quote) -> bool`.

- [x] Test Unicode source offsets, sentence extraction, exact quote validation, oversized document and unsupported extension rejection; load a generated text PDF with page anchors.
- [x] Run `python -m pytest tests/test_literature.py -q`; expect missing extraction feature failure.
- [x] Implement bounded local text/PDF extraction, SHA-256 and exact character/page anchors, keyword candidate extraction (explicitly deterministic, not a claim of semantic LLM extraction). Candidate output requires human review before Persona editing.
- [x] Run full suite and commit `feat: extract source-grounded persona evidence from local documents`.

### Task 4: API, console and CLI

**Files:** `src/personalab/{api,cli}.py`, `src/personalab/static/{index.html,style.css,app.js}`, `tests/test_api.py`, `tests/test_cli.py`.

**Interfaces:** `create_app(db_path=None) -> FastAPI`; `personalab serve`, `personalab run`, `personalab extract`; REST `/api/health`, `/api/personas`, `/api/scenarios`, `/api/runs`, `/api/runs/{id}`, `/api/runs/{id}/report`.

- [x] Test offline create/read/list/export lifecycle with isolated DB, absent ID 404, bad config 422, missing LLM credentials 503, no secrets in errors, static console served and CLI subprocess output/config override/extraction.
- [x] Run API/CLI tests; expect missing module/entry point failure.
- [x] Implement factory-based app, per-request clients, thread-offloaded SQLite and bounded API admission; synchronous response for small runs, documented request-bound lifecycle. Serve safe static UI; use textContent for all dynamic content.
- [x] Build responsive dark/light-accent console with setup form, clear offline label, sample experiment, group chart, aggregate metrics, round table and exports; cap default sample size.
- [x] Implement argparse CLI, JSON config and reports, graceful diagnostic exit codes; bind server to loopback by default.
- [x] Run full suite, actual loopback HTTP smoke and browser verification if tooling is available; commit `feat: ship experiment console REST API and CLI`.

### Task 5: Documentation, reproducible artifacts and publication

**Files:** README files, docs, examples, CI, container, repository templates and policy files.

**Interfaces:** documented quickstarts must execute against installed package; Python 3.11–3.14 CI runs Ruff and pytest; release v0.1.0.

- [x] Write detailed Chinese README and English overview with architecture, real commands, data contracts, metrics formulas, limitations, agent engineering rationale, provider setup, interview walkthrough and future roadmap; no unsupported results.
- [x] Add MIT license, contributor and security policies, issue/PR templates, Dependabot, CI, Docker/Compose and environment example.
- [x] Generate small offline JSON/Markdown reports and comparison artifact with commands and checksum-verifiable inputs. Validate README quickstart and wheel package content, Ruff and full tests.
- [x] Conduct separate whole-branch self-review against review focus. Add RED→GREEN regression coverage for material findings before release. Record test totals, local HTTP evidence and untested real-LLM/container limitations.
- [x] Commit final artifacts; merge feature branch fast-forward into local main; push main and annotated v0.1.0 tag (user explicitly authorized push). Use existing Git credential manager privately, never print credentials.
- [x] Set concise repository description/topics and create real release through GitHub API when permissions permit; verify remote head, CI and repository metadata. Report any external blockers precisely.

## Execution Notes

Implementation will use a feature branch in the user-designated empty project folder. No separate worktree is needed for protection of pre-existing product changes (there are none); this keeps all deliverables in the folder requested by the user. The design is user-approved; plan is an implementation detail and execution continues under that authorization.
