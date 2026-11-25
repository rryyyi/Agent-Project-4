"""Scenario mechanics are computed by the environment, never by the model."""

import math

from .schemas import ExperimentConfig, Persona

SCENARIOS = {
    'public_goods': {'name': '公共物品博弈', 'endowment': 10, 'multiplier': 1.6, 'action_min': 0, 'action_max': 10, 'rule': 'All players contribute simultaneously. Payoff = 10 - own contribution + 1.6 * total contribution / players.'},
    'trust_game': {'name': '信任博弈', 'endowment': 10, 'multiplier': 3, 'action_min': 0, 'action_max': 1, 'rule': 'Investor sends 0..10; trustee observes received amount and returns fraction 0..1 of tripled transfer. Investor payoff = 10 - transfer + returned; trustee payoff = 3 * transfer - returned.'},
    'product_ab': {'name': '产品策略 A/B 模拟', 'action_min': 0, 'action_max': 1, 'rule': 'Choose 1 (accept) or 0 (decline). Each variant is observed in isolation, with matched persona/repetition seeds. Only synthetic preferences are measured.'},
}


def context_for(config: ExperimentConfig, persona: Persona, history: list, variant: str) -> dict:
    return {
        'scenario': config.scenario,
        'rules': SCENARIOS[config.scenario],
        'persona': persona.model_dump(mode='json'),
        'history': history[-config.history_window:] if config.history_window else [],
        'variant': variant,
        'offer': config.variant_a if variant == 'A' else config.variant_b,
    }


def validate_action(scenario: str, action: float) -> float:
    if isinstance(action, bool) or not isinstance(action, (float, int)) or not math.isfinite(action):
        raise ValueError('action must be finite numeric value')
    maximum = 10 if scenario in {'public_goods', 'trust_investor'} else 1
    if not 0 <= action <= maximum:
        raise ValueError('action outside legal range')
    if scenario == 'product_ab' and action not in (0, 1):
        raise ValueError('product choice must be binary')
    return float(action)


def settle(scenario: str, actions: list[float]) -> list[float]:
    if not actions:
        raise ValueError('cannot settle empty group')
    if scenario == 'public_goods':
        for action in actions:
            validate_action(scenario, action)
        common = 1.6 * sum(actions) / len(actions)
        return [round(10 - action + common, 6) for action in actions]
    if scenario == 'trust_game':
        if len(actions) != 2:
            raise ValueError('trust game requires transfer and return fraction')
        transfer = validate_action('trust_investor', actions[0])
        fraction = validate_action('trust_game', actions[1])
        returned = transfer * 3 * fraction
        return [round(10 - transfer + returned, 6), round(transfer * 3 - returned, 6)]
    return [validate_action('product_ab', action) for action in actions]
