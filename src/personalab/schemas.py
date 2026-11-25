"""Versioned public contracts. Unknown fields and nonfinite numbers are rejected."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Unit = Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)]
Identifier = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_-]{0,63}$")]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Traits(StrictModel):
    openness: Unit
    conscientiousness: Unit
    extraversion: Unit
    agreeableness: Unit
    neuroticism: Unit


class SocialPreferences(StrictModel):
    cooperation: Unit
    reciprocity: Unit
    fairness: Unit


class DecisionPreferences(StrictModel):
    risk_tolerance: Unit
    loss_aversion: Unit


class Evidence(StrictModel):
    source: str = Field(min_length=1, max_length=500)
    quote: str = Field(min_length=1, max_length=2000)
    note: str = Field(max_length=1000)


class Persona(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    id: Identifier
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=1000)
    traits: Traits
    social: SocialPreferences
    preferences: DecisionPreferences
    evidence: list[Evidence] = Field(default_factory=list, max_length=20)


class ExperimentConfig(StrictModel):
    scenario: Literal["public_goods", "trust_game", "product_ab"] = "public_goods"
    personas: list[Identifier] = Field(
        default_factory=lambda: ["cooperator", "reciprocator", "cautious", "explorer"],
        min_length=1,
        max_length=12,
    )
    provider: Literal["offline", "openai"] = "offline"
    model: str = Field(default="gpt-4o-mini", min_length=1, max_length=120)
    rounds: int = Field(default=5, ge=1, le=100)
    repetitions: int = Field(default=3, ge=1, le=50)
    seed: int = Field(default=42, ge=0, le=2**32 - 1)
    concurrency: int = Field(default=4, ge=1, le=16)
    max_calls: int = Field(default=1000, ge=1, le=10000)
    max_retries: int = Field(default=2, ge=0, le=3)
    timeout_seconds: float = Field(default=30, ge=0.01, le=120)
    history_window: int = Field(default=4, ge=0, le=20)
    variant_a: str = Field(
        default="Standard plan: clear price, basic benefits.", min_length=1, max_length=1000
    )
    variant_b: str = Field(
        default="Same price, transparent privacy controls and a free trial.", min_length=1, max_length=1000
    )

    @model_validator(mode="after")
    def unique_and_bounded(self):
        if len(set(self.personas)) != len(self.personas):
            raise ValueError("persona IDs must be unique")
        factor = 2 if self.scenario in {"product_ab", "trust_game"} else 1
        if len(self.personas) * self.rounds * self.repetitions * factor > 10000:
            raise ValueError("workload exceeds 10000 planned decisions")
        return self


class Decision(StrictModel):
    action: Annotated[float, Field(strict=True)]
    explanation: str = Field(min_length=1, max_length=1000)
    confidence: Unit
    parameter_refs: list[str] = Field(max_length=10)
