"""Provider boundary; offline policies are explicit synthetic baselines, not LLMs."""

import json
import math
import random
from dataclasses import dataclass
from typing import Protocol

import httpx

from .prompts import compile_messages


@dataclass(frozen=True)
class ProviderResponse:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0


class Provider(Protocol):
    async def decide(self, request: dict) -> ProviderResponse: ...


class ProviderError(Exception):
    def __init__(self, category: str):
        self.category = category
        super().__init__(category)


class OfflineProvider:
    """Seeded heuristic policy: parameter sensitivity is built in, not empirical validation."""

    async def decide(self, request: dict) -> ProviderResponse:
        c = request["context"]
        p = c["persona"]
        social, pref = p["social"], p["preferences"]
        rng = random.Random(request["seed"])
        noise = rng.uniform(-0.08, 0.08)
        if c["scenario"] == "public_goods":
            base = social["cooperation"]
            if c["history"]:
                observed = c["history"][-1]["mean_action"] / 10
                base = (1 - 0.35 * social["reciprocity"]) * base + 0.35 * social["reciprocity"] * observed
            action = round(10 * min(1, max(0, base + noise)), 2)
            refs = ["social.cooperation", "social.reciprocity"]
        elif c["scenario"] == "trust_game":
            if c["role"] == "investor":
                base = (
                    0.5 * social["cooperation"] + 0.4 * pref["risk_tolerance"] - 0.2 * pref["loss_aversion"]
                )
                action = round(10 * min(1, max(0, base + noise)), 2)
                refs = ["social.cooperation", "preferences.risk_tolerance", "preferences.loss_aversion"]
            else:
                action = round(
                    min(1, max(0, 0.45 * social["reciprocity"] + 0.3 * social["fairness"] + noise)), 3
                )
                refs = ["social.reciprocity", "social.fairness"]
        else:
            # Transparent token features for a teaching baseline; no semantic offer understanding.
            offer = c["offer"].lower()
            transparency = any(word in offer for word in ["privacy", "transparent", "隐私", "透明"])
            trial = any(word in offer for word in ["trial", "试用"])
            score = (
                -0.5
                + p["traits"]["openness"] * 0.6
                + pref["risk_tolerance"] * 0.45
                - pref["loss_aversion"] * 0.4
            )
            score += transparency * 0.35 * pref["loss_aversion"] + trial * 0.25
            probability = 1 / (1 + math.exp(-score))
            action = float(rng.random() < probability)
            refs = ["traits.openness", "preferences.risk_tolerance", "preferences.loss_aversion"]
        return ProviderResponse(
            json.dumps(
                {
                    "action": action,
                    "explanation": "Offline synthetic policy: seeded action from " + ", ".join(refs) + ".",
                    "confidence": 0.7,
                    "parameter_refs": refs,
                }
            )
        )


class OpenAIProvider:
    """OpenAI-compatible chat completion adapter; retry policy belongs to the engine."""

    def __init__(self, api_key: str, base_url: str, model: str, client: httpx.AsyncClient):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self.model = model
        self.client = client

    async def decide(self, request: dict) -> ProviderResponse:
        try:
            response = await self.client.post(
                self._base_url + "/chat/completions",
                headers={"Authorization": "Bearer " + self._api_key},
                json={
                    "model": self.model,
                    "messages": compile_messages(request),
                    "response_format": {"type": "json_object"},
                    "temperature": 0.2,
                    "seed": request["seed"],
                    "max_tokens": 500,
                },
            )
            if response.status_code == 429:
                raise ProviderError("rate_limited")
            if response.status_code >= 500:
                raise ProviderError("upstream_unavailable")
            if response.status_code in (401, 403):
                raise ProviderError("authentication_failed")
            if response.status_code >= 400:
                raise ProviderError("upstream_rejected")
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if not isinstance(content, str) or len(content) > 20000:
                raise ProviderError("invalid_response")
            usage = data.get("usage") or {}
            return ProviderResponse(
                content,
                max(0, int(usage.get("prompt_tokens", 0))),
                max(0, int(usage.get("completion_tokens", 0))),
            )
        except httpx.TimeoutException as exc:
            raise ProviderError("timeout") from exc
        except httpx.RequestError as exc:
            raise ProviderError("network_error") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError("invalid_response") from exc
