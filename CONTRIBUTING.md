# Contributing

Thank you for helping make behavioral experiments easier to inspect and reproduce.

## Development

```bash
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -e ".[dev]"
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m pytest -q
python scripts/reproduce.py
python -m build
```

Use a focused branch and open a pull request describing the problem, resulting behavior and verification. Add behavioral tests for logic changes, especially payoff calculations, invalid outputs, retries, seeds and partial failures. Tests must not call paid providers; use httpx MockTransport at the network boundary.

## Changing experiments

Document changes to action spaces, payoffs, seed derivation, persona assumptions and metric denominators. Increment relevant versions when behavior changes. Regenerate expected examples only intentionally with `python scripts/reproduce.py --update`, and explain the result diff in the PR. Never overwrite evidence to hide a failed comparison.

A new scenario needs explicit rules, action validation, environment-owned settlement, engine integration, tests, example configuration and interpretation limits. A new provider must honor timeouts/cancellation and preserve the trace/usage contract. No automatic fallback that changes method identity.

## Data and claims

Do not submit API keys, resumes, private source papers, personal data, or vendor response bodies containing secrets. Include a license/source for contributed example text. Mark simulated populations and offline policies clearly. Avoid claims about real people or product outcomes without independently reviewable evidence.

## Review

CI checks Python versions, static analysis, regression tests, reproduction and packaging/container viability. A green build is required evidence, not proof of behavioral science validity. Maintainers review API compatibility and interpretation of reported results.
