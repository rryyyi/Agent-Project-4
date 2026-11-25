import math

import pytest
from pydantic import ValidationError

from personalab.personas import load_personas
from personalab.scenarios import context_for, settle, validate_action
from personalab.schemas import Decision, ExperimentConfig, Persona


def test_custom_registry_is_loadable_and_rejects_duplicate_ids(tmp_path):
    import json

    persona = load_personas()["cooperator"].model_dump()
    path = tmp_path / "personas.json"
    path.write_text(json.dumps([persona]), encoding="utf-8")
    assert list(load_personas(path)) == ["cooperator"]
    path.write_text(json.dumps([persona, persona]), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        load_personas(path)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        load_personas(path)


def test_registry_has_distinct_valid_personas():
    registry = load_personas()
    assert len(registry) == 4
    assert registry["cooperator"].social.cooperation > registry["explorer"].social.cooperation
    assert all(p.schema_version == "1.0" for p in registry.values())


@pytest.mark.parametrize("value", [-0.1, 1.1, math.nan, math.inf])
def test_persona_rejects_invalid_traits(value):
    data = load_personas()["cooperator"].model_dump()
    data["traits"]["openness"] = value
    with pytest.raises(ValidationError):
        Persona.model_validate(data)


@pytest.mark.parametrize(
    "patch",
    [
        {"unknown": True},
        {"personas": ["cooperator", "cooperator"]},
        {"personas": []},
        {"rounds": 101},
        {"repetitions": 51},
        {"scenario": "invented"},
        {"max_calls": 0},
        {"seed": -1},
    ],
)
def test_config_rejects_unsafe_or_ambiguous_inputs(patch):
    with pytest.raises(ValidationError):
        ExperimentConfig.model_validate(patch)


@pytest.mark.parametrize(
    ("scenario", "actions", "expected"),
    [
        ("public_goods", [0, 10], [18, 8]),
        ("trust_game", [4, 0.5], [12, 6]),
        ("product_ab", [0, 1], [0, 1]),
    ],
)
def test_payoffs_are_environment_computed(scenario, actions, expected):
    assert settle(scenario, actions) == expected


@pytest.mark.parametrize(
    ("scenario", "action"),
    [
        ("public_goods", 11),
        ("public_goods", -1),
        ("trust_game", 1.1),
        ("product_ab", 0.5),
        ("product_ab", True),
        ("product_ab", math.nan),
    ],
)
def test_action_validation_rejects_out_of_space_values(scenario, action):
    with pytest.raises(ValueError):
        validate_action(scenario, action)


def test_context_caps_history_and_exposes_scenario_rules():
    config = ExperimentConfig(rounds=20, history_window=2)
    context = context_for(config, load_personas()["cooperator"], [{"round": i} for i in range(10)], "A")
    assert context["history"] == [{"round": 8}, {"round": 9}]
    assert context["rules"]["endowment"] == 10
    assert context["variant"] == "A"


def test_decision_rejects_unbounded_explanation_and_nan_confidence():
    with pytest.raises(ValidationError):
        Decision(action=1, explanation="x" * 1001, confidence=0.5, parameter_refs=[])
    with pytest.raises(ValidationError):
        Decision(action=1, explanation="test", confidence=math.nan, parameter_refs=[])
