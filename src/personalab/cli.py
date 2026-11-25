"""Run experiments, inspect source evidence, or serve the console."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import httpx

from .engine import run_experiment
from .literature import extract_evidence, read_document
from .personas import load_personas
from .providers import OfflineProvider, OpenAIProvider
from .reports import markdown_report
from .schemas import ExperimentConfig
from .storage import Store


async def execute(config: ExperimentConfig) -> dict:
    registry = load_personas(os.getenv("PERSONALAB_PERSONAS"))
    if config.provider == "offline":
        return await run_experiment(config, registry, OfflineProvider())
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("llm_credentials_not_configured")
    async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
        return await run_experiment(
            config,
            registry,
            OpenAIProvider(
                key, os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"), config.model, client
            ),
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="personalab", description="Reproducible persona-driven agent experiments"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Execute an experiment and export JSON/Markdown")
    run.add_argument("--config", type=Path)
    run.add_argument("--scenario", choices=["public_goods", "trust_game", "product_ab"])
    run.add_argument("--seed", type=int)
    run.add_argument("--output", type=Path, default=Path("artifacts/latest"))
    run.add_argument("--db", type=Path, default=Path("artifacts/personalab.db"))
    serve = sub.add_parser("serve", help="Serve local console and REST API")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    extract = sub.add_parser("extract", help="Extract exact source-grounded keyword candidates")
    extract.add_argument("path", type=Path)
    extract.add_argument("--keywords", required=True, help="Comma-separated keywords")
    args = parser.parse_args()
    try:
        if args.command == "serve":
            import uvicorn

            uvicorn.run("personalab.api:create_app", factory=True, host=args.host, port=args.port)
            return 0
        if args.command == "extract":
            rows = extract_evidence(read_document(args.path), args.path.name, args.keywords.split(","))
            print(json.dumps(rows, indent=2, ensure_ascii=False))
            return 0
        data = json.loads(args.config.read_text(encoding="utf-8-sig")) if args.config else {}
        if args.scenario is not None:
            data["scenario"] = args.scenario
        if args.seed is not None:
            data["seed"] = args.seed
        config = ExperimentConfig.model_validate(data)
        result = asyncio.run(execute(config))
        Store(args.db).save(result)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "run.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8"
        )
        (args.output / "report.md").write_text(markdown_report(result), encoding="utf-8")
        print(
            json.dumps(
                {
                    "id": result["id"],
                    "status": result["status"],
                    "output": str(args.output),
                    "error": result["error"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if result["status"] == "completed" else 1
    except (ValueError, OSError):
        print("invalid_input: check config, paths and required environment variables", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
