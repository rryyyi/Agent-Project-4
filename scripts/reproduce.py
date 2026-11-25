"""Re-run offline examples; compare deterministic results without masking mismatches."""

import argparse
import asyncio
import json
from pathlib import Path

from personalab.engine import run_experiment
from personalab.personas import load_personas
from personalab.providers import OfflineProvider
from personalab.reports import markdown_report
from personalab.schemas import ExperimentConfig

ROOT = Path(__file__).resolve().parents[1]


def normalize(run: dict) -> dict:
    return {
        key: run[key]
        for key in ("config", "persona_snapshot", "status", "error", "calls_used", "metrics", "decisions")
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update", action="store_true", help="Intentionally regenerate committed expected summaries/reports"
    )
    args = parser.parse_args()
    for name in ("public_goods", "trust_game", "product_ab"):
        config = ExperimentConfig.model_validate_json(
            (ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")
        )
        result = asyncio.run(run_experiment(config, load_personas(), OfflineProvider()))
        assert result["status"] == "completed", result["error"]
        output = ROOT / "artifacts" / "reproduction" / name
        output.mkdir(parents=True, exist_ok=True)
        (output / "run.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output / "report.md").write_text(markdown_report(result), encoding="utf-8")
        expected = ROOT / "examples" / "results" / f"{name}.summary.json"
        actual = normalize(result)
        if args.update:
            expected.parent.mkdir(parents=True, exist_ok=True)
            expected.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            expected.with_suffix(".md").write_text(markdown_report(result), encoding="utf-8")
        else:
            assert expected.is_file(), f"Missing expected result: {expected}. Maintainers may use --update."
            assert json.loads(expected.read_text(encoding="utf-8")) == actual, (
                f"Reproduction mismatch: {name}. Inspect policy/config/version differences before updating expected results."
            )
        print(
            json.dumps(
                {
                    "scenario": name,
                    "status": result["status"],
                    "decisions": len(result["decisions"]),
                    "matched_expected": not args.update,
                    "config_sha256": result["provenance"]["config_sha256"],
                }
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
