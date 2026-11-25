"""Local single-user REST service and bundled experiment console."""

import asyncio
import os
from importlib.resources import files
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import Field

from . import __version__
from .engine import run_experiment
from .literature import extract_evidence
from .personas import load_personas
from .providers import OfflineProvider, OpenAIProvider
from .reports import markdown_report
from .scenarios import SCENARIOS
from .schemas import ExperimentConfig, StrictModel
from .storage import Store


class EvidenceRequest(StrictModel):
    text: str = Field(min_length=1, max_length=200000)
    source: str = Field(min_length=1, max_length=500)
    keywords: list[str] = Field(min_length=1, max_length=20)


def create_app(db_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(
        title="PersonaLab",
        version=__version__,
        description="Persona-driven synthetic behavioral experiments. Local single-user deployment.",
    )
    registry = load_personas()
    store = Store(db_path or os.getenv("PERSONALAB_DB", "artifacts/personalab.db"))
    static = Path(str(files("personalab").joinpath("static")))
    app.mount("/static", StaticFiles(directory=static), name="static")
    app.state.active_runs = 0

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(static / "index.html")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": __version__, "mode": "local_single_user"}

    @app.get("/api/personas")
    def personas():
        return [p.model_dump(mode="json") for p in registry.values()]

    @app.get("/api/scenarios")
    def scenarios():
        return SCENARIOS

    @app.post("/api/runs", status_code=201)
    async def create_run(config: ExperimentConfig):
        if set(config.personas) - registry.keys():
            raise HTTPException(422, "unknown_persona_id")
        if config.provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(503, "llm_credentials_not_configured")
        # No await between checking and incrementing: atomic within this event loop.
        if app.state.active_runs >= 2:
            raise HTTPException(429, "experiment_capacity_reached")
        app.state.active_runs += 1
        try:
            if config.provider == "offline":
                result = await run_experiment(config, registry, OfflineProvider())
            else:
                async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
                    provider = OpenAIProvider(
                        os.environ["OPENAI_API_KEY"],
                        os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                        config.model,
                        client,
                    )
                    result = await run_experiment(config, registry, provider)
            await asyncio.to_thread(store.save, result)
            return result
        finally:
            app.state.active_runs -= 1

    @app.get("/api/runs")
    def list_runs(limit: int = Query(default=20, ge=1, le=100)):
        return store.list(limit)

    def require_run(run_id):
        result = store.get(run_id)
        if result is None:
            raise HTTPException(404, "run_not_found")
        return result

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str):
        return require_run(run_id)

    @app.get("/api/runs/{run_id}/report", response_class=PlainTextResponse)
    def report(run_id: str):
        result = require_run(run_id)
        return PlainTextResponse(
            markdown_report(result),
            headers={"Content-Disposition": f'attachment; filename="personalab-{result["id"]}.md"'},
        )

    @app.post("/api/evidence")
    def evidence(request: EvidenceRequest):
        try:
            return extract_evidence(request.text, request.source, request.keywords)
        except ValueError:
            raise HTTPException(422, "invalid_evidence_input") from None

    return app
