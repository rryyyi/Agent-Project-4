# PersonaLab · Experiment report

- Run: `76ac96b8-af85-424d-a2e1-b57b876b1b6f`
- Status: **completed**
- Provider: **offline**
- Model: seeded-heuristic-v1
- Created: 2026-11-25T03:34:47.849538+00:00
- Software: 0.1.0
- Config SHA-256: `41da646b57ebb5d7de1198201b0aaa81d6945239ed1d7132c1d9e65b9d57021c`

> Synthetic-agent experiment. Offline behavior is a seeded heuristic baseline, not a real LLM evaluation. Neither provider validates predictions about real people. Explanations and confidence are self-reported.

## Metrics

```json
{
  "planned_decisions": 120,
  "completed_decisions": 120,
  "legal_decision_rate": 1.0,
  "valid_attempt_rate": 1.0,
  "input_tokens": 0,
  "output_tokens": 0,
  "action_distribution": {
    "0.0": 60,
    "1.0": 60
  },
  "by_persona": {
    "cautious": {
      "decisions": 30,
      "mean_action": 0.366667,
      "mean_payoff": 0.366667
    },
    "cooperator": {
      "decisions": 30,
      "mean_action": 0.533333,
      "mean_payoff": 0.533333
    },
    "explorer": {
      "decisions": 30,
      "mean_action": 0.733333,
      "mean_payoff": 0.733333
    },
    "reciprocator": {
      "decisions": 30,
      "mean_action": 0.366667,
      "mean_payoff": 0.366667
    }
  },
  "ab_comparison": {
    "paired_units": 12,
    "unit": "persona_id × repetition; rounds averaged within unit",
    "rate_a": 0.466667,
    "rate_b": 0.533333,
    "difference_b_minus_a": 0.066667,
    "ci95_normal_approx": [
      -0.007039,
      0.140373
    ],
    "caveat": "Descriptive normal approximation over synthetic paired units; small samples and interacting agents violate population inference assumptions. Not a real-user causal effect."
  }
}
```

## Configuration

```json
{
  "scenario": "product_ab",
  "personas": [
    "cooperator",
    "reciprocator",
    "cautious",
    "explorer"
  ],
  "provider": "offline",
  "model": "gpt-4o-mini",
  "rounds": 5,
  "repetitions": 3,
  "seed": 42,
  "concurrency": 4,
  "max_calls": 1000,
  "max_retries": 2,
  "timeout_seconds": 30.0,
  "history_window": 4,
  "variant_a": "Standard plan: clear price, basic benefits.",
  "variant_b": "Same price, transparent privacy controls and a free trial."
}
```

## Decision sample (first 40)

| Persona | Rep | Round | Variant / Role | Action | Payoff | Explanation |
| --- | --- | --- | --- | --- | --- | --- |
| cooperator | 0 | 1 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 1 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 1 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 1 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 2 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 2 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 2 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 2 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 3 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 3 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 3 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 3 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 4 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 4 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 4 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 4 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 5 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 5 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 5 | A/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 5 | A/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 1 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 1 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 1 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 1 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 2 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 2 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 2 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 2 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 3 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 3 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 3 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 3 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 4 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 4 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 4 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 4 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 5 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 5 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 5 | B/player | 1.0 | 1.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 5 | B/player | 0.0 | 0.0 | Offline synthetic policy: seeded action from traits.openness, preferences.risk_tolerance, preferences.loss_aversion. |

## Interpretation limits

- Persona parameters are hand-authored assumptions. Big Five is a parameter vocabulary, not a validated psychometric instrument here.
- Cooperation alignment is a declared proxy; offline policies directly use those parameters, so this is an implementation check, not scientific validation.
- A/B uses matched synthetic units. Its normal-approximation interval is descriptive; repeated interactions and small samples limit inference.
- Trust-role means mix transfer amounts and return fractions; inspect role-level traces rather than comparing the aggregate as a common unit.
- Token usage is provider-reported; unavailable usage is zero. No currency cost is estimated.
- This version persists terminal snapshots; it has no durable job queue or mid-run crash recovery.
- Full decisions, attempts, timings, prompts/context and persona snapshots are available in the JSON export.
