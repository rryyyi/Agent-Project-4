"""Load packaged, explicitly synthetic persona configurations."""

import json
from importlib.resources import files
from pathlib import Path

from .schemas import Persona


def load_personas(path: str | Path | None = None) -> dict[str, Persona]:
    source = Path(path) if path else files("personalab").joinpath("data/personas.json")
    data = json.loads(source.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list) or not 1 <= len(data) <= 100:
        raise ValueError("persona registry must be a nonempty array of at most 100 entries")
    personas = [Persona.model_validate(item) for item in data]
    registry = {persona.id: persona for persona in personas}
    if len(registry) != len(personas):
        raise ValueError("duplicate persona IDs in registry")
    return registry
