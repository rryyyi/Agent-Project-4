"""Load packaged, explicitly synthetic persona configurations."""

import json
from importlib.resources import files

from .schemas import Persona


def load_personas() -> dict[str, Persona]:
    data = json.loads(files("personalab").joinpath("data/personas.json").read_text(encoding="utf-8"))
    personas = [Persona.model_validate(item) for item in data]
    registry = {persona.id: persona for persona in personas}
    if len(registry) != len(personas):
        raise ValueError("duplicate persona IDs in registry")
    return registry
