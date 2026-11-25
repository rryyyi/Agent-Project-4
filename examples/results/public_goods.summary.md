# PersonaLab · Experiment report

- Run: `c8afea6f-8d70-46b5-8f8f-aed753e794f1`
- Status: **completed**
- Provider: **offline**
- Model: seeded-heuristic-v1
- Created: 2026-11-25T03:34:47.800838+00:00
- Software: 0.1.0
- Config SHA-256: `c9d80124a2eb8a4c3ec0f9bf73d98b1b25962093047f85faef68517e6c7f5d69`

> Synthetic-agent experiment. Offline behavior is a seeded heuristic baseline, not a real LLM evaluation. Neither provider validates predictions about real people. Explanations and confidence are self-reported.

## Metrics

```json
{
  "planned_decisions": 60,
  "completed_decisions": 60,
  "legal_decision_rate": 1.0,
  "valid_attempt_rate": 1.0,
  "input_tokens": 0,
  "output_tokens": 0,
  "action_distribution": {
    "2.95": 1,
    "3.03": 1,
    "3.31": 1,
    "3.47": 1,
    "3.54": 1,
    "3.56": 1,
    "3.59": 1,
    "3.67": 1,
    "3.72": 1,
    "3.74": 1,
    "3.75": 1,
    "3.79": 1,
    "3.95": 3,
    "3.99": 1,
    "4.07": 1,
    "4.29": 1,
    "4.54": 1,
    "4.56": 1,
    "4.63": 1,
    "4.82": 1,
    "4.93": 1,
    "5.02": 1,
    "5.12": 1,
    "5.16": 1,
    "5.25": 1,
    "5.46": 1,
    "5.49": 2,
    "5.51": 2,
    "5.52": 1,
    "5.56": 1,
    "5.7": 1,
    "5.82": 1,
    "5.84": 1,
    "5.91": 1,
    "6.11": 1,
    "6.13": 1,
    "6.38": 1,
    "6.39": 1,
    "6.72": 1,
    "6.86": 1,
    "7.18": 1,
    "7.45": 1,
    "7.6": 1,
    "7.65": 1,
    "8.12": 1,
    "8.14": 1,
    "8.15": 1,
    "8.25": 1,
    "8.32": 1,
    "8.4": 1,
    "8.46": 1,
    "8.74": 1,
    "8.91": 1,
    "9.01": 1,
    "9.02": 1,
    "9.28": 1
  },
  "by_persona": {
    "cautious": {
      "decisions": 15,
      "mean_action": 4.802667,
      "mean_payoff": 14.355467
    },
    "cooperator": {
      "decisions": 15,
      "mean_action": 8.366667,
      "mean_payoff": 10.791467
    },
    "explorer": {
      "decisions": 15,
      "mean_action": 3.66,
      "mean_payoff": 15.498133
    },
    "reciprocator": {
      "decisions": 15,
      "mean_action": 6.066,
      "mean_payoff": 13.092133
    }
  },
  "cooperation_alignment_proxy": 0.945583
}
```

## Configuration

```json
{
  "scenario": "public_goods",
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
| cooperator | 0 | 1 | A/player | 9.01 | 10.486 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 0 | 1 | A/player | 7.18 | 12.316 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 0 | 1 | A/player | 3.99 | 15.506 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 0 | 1 | A/player | 3.56 | 15.936 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 0 | 2 | A/player | 8.14 | 11.008 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 0 | 2 | A/player | 5.82 | 13.328 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 0 | 2 | A/player | 5.16 | 13.988 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 0 | 2 | A/player | 3.75 | 15.398 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 0 | 3 | A/player | 8.46 | 10.96 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 0 | 3 | A/player | 5.84 | 13.58 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 0 | 3 | A/player | 5.51 | 13.91 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 0 | 3 | A/player | 3.74 | 15.68 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 0 | 4 | A/player | 9.02 | 10.288 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 0 | 4 | A/player | 5.51 | 13.798 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 0 | 4 | A/player | 5.02 | 14.288 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 0 | 4 | A/player | 3.72 | 15.588 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 0 | 5 | A/player | 8.91 | 10.418 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 0 | 5 | A/player | 5.49 | 13.838 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 0 | 5 | A/player | 4.63 | 14.698 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 0 | 5 | A/player | 4.29 | 15.038 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 1 | 1 | A/player | 8.4 | 11.144 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 1 | 1 | A/player | 6.86 | 12.684 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 1 | 1 | A/player | 4.93 | 14.614 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 1 | 1 | A/player | 3.67 | 15.874 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 1 | 2 | A/player | 7.65 | 10.87 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 1 | 2 | A/player | 6.11 | 12.41 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 1 | 2 | A/player | 4.07 | 14.45 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 1 | 2 | A/player | 3.47 | 15.05 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 1 | 3 | A/player | 7.45 | 10.874 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 1 | 3 | A/player | 6.38 | 11.944 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 1 | 3 | A/player | 3.95 | 14.374 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 1 | 3 | A/player | 3.03 | 15.294 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 1 | 4 | A/player | 8.12 | 10.072 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 1 | 4 | A/player | 5.46 | 12.732 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 1 | 4 | A/player | 3.95 | 14.242 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 1 | 4 | A/player | 2.95 | 15.242 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cooperator | 1 | 5 | A/player | 8.74 | 10.82 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| reciprocator | 1 | 5 | A/player | 6.39 | 13.17 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| cautious | 1 | 5 | A/player | 4.82 | 14.74 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |
| explorer | 1 | 5 | A/player | 3.95 | 15.61 | Offline synthetic policy: seeded action from social.cooperation, social.reciprocity. |

## Interpretation limits

- Persona parameters are hand-authored assumptions. Big Five is a parameter vocabulary, not a validated psychometric instrument here.
- Cooperation alignment is a declared proxy; offline policies directly use those parameters, so this is an implementation check, not scientific validation.
- A/B uses matched synthetic units. Its normal-approximation interval is descriptive; repeated interactions and small samples limit inference.
- Trust-role means mix transfer amounts and return fractions; inspect role-level traces rather than comparing the aggregate as a common unit.
- Token usage is provider-reported; unavailable usage is zero. No currency cost is estimated.
- This version persists terminal snapshots; it has no durable job queue or mid-run crash recovery.
- Full decisions, attempts, timings, prompts/context and persona snapshots are available in the JSON export.
