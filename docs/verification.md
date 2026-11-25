# Verification record

Date: 2026-11-25. All numbers below describe actual checks of this repository, not product adoption or real-model quality.

## Local checks

| Check | Actual outcome |
| --- | --- |
| Platform | Windows, Python 3.14.4 |
| Editable installation | `python -m pip install -e ".[dev]"` succeeded |
| Regression suite | 56 tests passed, no warnings in final run |
| Ruff lint | `python -m ruff check src tests scripts` passed |
| Ruff format | `python -m ruff format --check src tests scripts` passed |
| Offline reproduction | Public goods: 60; trust: 48; product A/B: 120 settled decisions; deterministic expected results matched |
| HTTP integration | Real Uvicorn process on loopback; health, console and experiment API checked |
| Browser | System Microsoft Edge Chromium; desktop 1512×1100 and mobile 390×844 |
| Browser flow | 120-decision A/B run, first 100 trace rows, JSON download, no page errors |
| Untrusted explanation | HTML-like explanation displayed as literal text, no injected image element |
| Mobile | No horizontal document overflow at 390px |
| Packaging | sdist + wheel built; isolated wheel installation loaded personas/static assets and completed an offline HTTP experiment |
| Python coverage | 83% in-process statement coverage; CLI tests execute real subprocesses, which are not counted in this coverage measurement |

Exact command suite:

```bash
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m pytest -q --cov=personalab --cov-report=term-missing
python scripts/reproduce.py
python scripts/verify_browser.py
python -m build
```

The browser script requires optional Playwright plus system Edge; it is separate from the default suite. It writes screenshots and a downloaded actual run under ignored `artifacts/browser/`. README screenshot is cropped from that actual console.

## Findings resolved before release

- Partial-round successful candidates were not retained when the round failed. A regression test first demonstrated the missing trace output; validated decisions are now retained per attempt without assigning a fabricated payoff.
- SQLite connection context managers committed/rolled back but did not close connections. A regression test tracked connection closure, including a duplicate-insert failure. Explicit contextlib.closing now releases every connection; final coverage run emitted no ResourceWarning.
- Packaged personas initially lacked an external JSON loading entry point. A custom-registry test demonstrated the missing interface; CLI/API now use `PERSONALAB_PERSONAS` and reject empty/duplicate registries.

## Review

The author performed a separate whole-project review using the approved design, implementation plan and review checklist. No subagent/reviewer tool was available; this is **self-review, not an independent review**. Focus included nonfinite/unknown inputs, output validation, failure budgets, secrets in exception text, exact evidence anchors, unknown IDs, and HTML rendering.

## External verification boundaries

- No paid or real-provider LLM experiment was run. The OpenAI-compatible adapter was tested at the real HTTP contract boundary using httpx MockTransport, including usage and failure classification.
- Local Docker client exists, but Docker Desktop's Linux engine was not running. No local container-build success is claimed. GitHub Actions successfully built the container, started it, verified health and completed an offline API experiment on Linux.
- GitHub Actions run [45541460247](https://github.com/rryyyi/Agent-Project-4/actions/runs/45541460247) completed successfully for commit `4492f02`: Python 3.11, 3.12, 3.13 and 3.14 on Linux; Python 3.12 on Windows; and Container smoke. Each Python job passed lint, format, tests, offline reproduction and package build. Subsequent maintenance commits are tracked by the current CI badge.
- No human behavioral calibration, large-scale load test, production deployment or durable crash recovery validation is included.

Current CI status and logs: https://github.com/rryyyi/Agent-Project-4/actions/workflows/ci.yml
