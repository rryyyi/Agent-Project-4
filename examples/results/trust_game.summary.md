# PersonaLab · Experiment report

- Run: `595cca33-9544-44ff-a054-2953571d9fee`
- Status: **completed**
- Provider: **offline**
- Model: seeded-heuristic-v1
- Created: 2026-11-25T03:34:47.824205+00:00
- Software: 0.1.0
- Config SHA-256: `e6ecc5d80b91657fb3047d6a7f6f482b74021e4a50ae3f50b4c44d5e5cec9bf6`

> Synthetic-agent experiment. Offline behavior is a seeded heuristic baseline, not a real LLM evaluation. Neither provider validates predictions about real people. Explanations and confidence are self-reported.

## Metrics

```json
{
  "planned_decisions": 48,
  "completed_decisions": 48,
  "legal_decision_rate": 1.0,
  "valid_attempt_rate": 1.0,
  "input_tokens": 0,
  "output_tokens": 0,
  "action_distribution": {
    "0.294": 1,
    "0.295": 1,
    "0.301": 1,
    "0.342": 1,
    "0.346": 1,
    "0.362": 1,
    "0.44": 1,
    "0.453": 1,
    "0.457": 1,
    "0.47": 1,
    "0.479": 1,
    "0.512": 1,
    "0.515": 1,
    "0.538": 1,
    "0.539": 1,
    "0.553": 1,
    "0.57": 1,
    "0.573": 1,
    "0.601": 1,
    "0.608": 1,
    "0.62": 1,
    "0.642": 1,
    "0.693": 1,
    "0.71": 1,
    "0.725": 1,
    "0.77": 1,
    "0.84": 1,
    "1.04": 1,
    "1.37": 1,
    "1.83": 1,
    "3.33": 1,
    "3.36": 1,
    "3.73": 1,
    "3.91": 1,
    "4.35": 1,
    "4.43": 1,
    "4.44": 1,
    "4.46": 1,
    "4.47": 1,
    "4.73": 1,
    "4.95": 1,
    "5.32": 1,
    "5.59": 1,
    "5.84": 1,
    "5.86": 1,
    "6.74": 1,
    "6.77": 1,
    "6.86": 1
  },
  "by_persona": {
    "cautious": {
      "decisions": 12,
      "mean_action": 0.755917,
      "mean_payoff": 7.893978
    },
    "cooperator": {
      "decisions": 12,
      "mean_action": 3.39225,
      "mean_payoff": 11.584219
    },
    "explorer": {
      "decisions": 12,
      "mean_action": 2.545,
      "mean_payoff": 7.592772
    },
    "reciprocator": {
      "decisions": 12,
      "mean_action": 2.275833,
      "mean_payoff": 8.800698
    }
  }
}
```

## Configuration

```json
{
  "scenario": "trust_game",
  "personas": [
    "cooperator",
    "reciprocator",
    "cautious",
    "explorer"
  ],
  "provider": "offline",
  "model": "gpt-4o-mini",
  "rounds": 3,
  "repetitions": 2,
  "seed": 42,
  "concurrency": 4,
  "max_calls": 1000,
  "max_retries": 2,
  "timeout_seconds": 30.0,
  "history_window": 2,
  "variant_a": "Standard plan: clear price, basic benefits.",
  "variant_b": "Same price, transparent privacy controls and a free trial."
}
```

## Decision sample (first 40)

| Persona | Rep | Round | Variant / Role | Action | Payoff | Explanation |
| --- | --- | --- | --- | --- | --- | --- |
| cooperator | 0 | 1 | A/investor | 5.84 | 16.862 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 1 | A/trustee | 0.725 | 4.818 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| reciprocator | 0 | 1 | A/investor | 4.35 | 12.37075 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 1 | A/trustee | 0.515 | 6.32925 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cautious | 0 | 1 | A/investor | 1.37 | 9.86711 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 1 | A/trustee | 0.301 | 2.87289 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| explorer | 0 | 1 | A/investor | 5.59 | 12.99624 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 1 | A/trustee | 0.512 | 8.18376 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cooperator | 0 | 2 | A/investor | 5.32 | 14.5752 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 2 | A/trustee | 0.62 | 6.0648 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| reciprocator | 0 | 2 | A/investor | 3.73 | 11.38383 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 2 | A/trustee | 0.457 | 6.07617 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cautious | 0 | 2 | A/investor | 0.57 | 10.04902 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 2 | A/trustee | 0.362 | 1.09098 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| explorer | 0 | 2 | A/investor | 4.44 | 11.8204 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 2 | A/trustee | 0.47 | 7.0596 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cooperator | 0 | 3 | A/investor | 6.77 | 18.8687 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 0 | 3 | A/trustee | 0.77 | 4.6713 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| reciprocator | 0 | 3 | A/investor | 3.91 | 11.40369 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 0 | 3 | A/trustee | 0.453 | 6.41631 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cautious | 0 | 3 | A/investor | 0.84 | 9.90088 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 0 | 3 | A/trustee | 0.294 | 1.77912 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| explorer | 0 | 3 | A/investor | 4.46 | 13.67504 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 0 | 3 | A/trustee | 0.608 | 5.24496 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cooperator | 1 | 1 | A/investor | 5.86 | 16.32294 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 1 | 1 | A/trustee | 0.693 | 5.39706 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| reciprocator | 1 | 1 | A/investor | 3.36 | 11.46832 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 1 | 1 | A/trustee | 0.479 | 5.25168 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cautious | 1 | 1 | A/investor | 1.04 | 10.03952 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 1 | 1 | A/trustee | 0.346 | 2.04048 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| explorer | 1 | 1 | A/investor | 4.43 | 12.91937 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 1 | 1 | A/trustee | 0.553 | 5.94063 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cooperator | 1 | 2 | A/investor | 6.86 | 16.35236 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| reciprocator | 1 | 2 | A/trustee | 0.642 | 7.36764 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| reciprocator | 1 | 2 | A/investor | 4.47 | 12.74458 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cautious | 1 | 2 | A/trustee | 0.538 | 6.19542 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| cautious | 1 | 2 | A/investor | 1.83 | 10.04758 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| explorer | 1 | 2 | A/trustee | 0.342 | 3.61242 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |
| explorer | 1 | 2 | A/investor | 4.73 | 13.40087 | Offline synthetic policy: seeded action from social.cooperation, preferences.risk_tolerance, preferences.loss_aversion. |
| cooperator | 1 | 2 | A/trustee | 0.573 | 6.05913 | Offline synthetic policy: seeded action from social.reciprocity, social.fairness. |

## Interpretation limits

- Persona parameters are hand-authored assumptions. Big Five is a parameter vocabulary, not a validated psychometric instrument here.
- Cooperation alignment is a declared proxy; offline policies directly use those parameters, so this is an implementation check, not scientific validation.
- A/B uses matched synthetic units. Its normal-approximation interval is descriptive; repeated interactions and small samples limit inference.
- Trust-role means mix transfer amounts and return fractions; inspect role-level traces rather than comparing the aggregate as a common unit.
- Token usage is provider-reported; unavailable usage is zero. No currency cost is estimated.
- This version persists terminal snapshots; it has no durable job queue or mid-run crash recovery.
- Full decisions, attempts, timings, prompts/context and persona snapshots are available in the JSON export.
