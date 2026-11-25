"""Descriptive metrics. Synthetic-agent statistics do not validate human behavior."""

import statistics
from collections import Counter, defaultdict


def evaluate(decisions: list[dict], attempts: list[dict], planned: int, scenario: str) -> dict:
    groups = defaultdict(list)
    for d in decisions:
        groups[d['persona_id']].append(d)
    by_persona = {}
    for name, rows in sorted(groups.items()):
        by_persona[name] = {
            'decisions': len(rows),
            'mean_action': round(statistics.mean(d['action'] for d in rows), 6),
            'mean_payoff': round(statistics.mean(d['payoff'] for d in rows), 6),
        }
    metrics = {
        'planned_decisions': planned,
        'completed_decisions': len(decisions),
        'legal_decision_rate': round(len(decisions) / planned, 6) if planned else 0,
        'valid_attempt_rate': round(sum(a['status'] == 'ok' for a in attempts) / len(attempts), 6) if attempts else 0,
        'input_tokens': sum(a['input_tokens'] for a in attempts),
        'output_tokens': sum(a['output_tokens'] for a in attempts),
        'action_distribution': dict(sorted(Counter(str(d['action']) for d in decisions).items())),
        'by_persona': by_persona,
    }
    if scenario == 'public_goods' and decisions:
        # Alignment is a declared engineering proxy, not independent psychological validation.
        metrics['cooperation_alignment_proxy'] = round(statistics.mean(
            1 - abs(d['action'] / 10 - d['cooperation_parameter']) for d in decisions
        ), 6)
    if scenario == 'product_ab':
        units = defaultdict(lambda: defaultdict(list))
        for d in decisions:
            units[(d['persona_id'], d['repetition'])][d['variant']].append(d['action'])
        differences = [statistics.mean(v['B']) - statistics.mean(v['A']) for v in units.values() if len(v['A']) == len(v['B']) and v['A']]
        n = len(differences)
        delta = statistics.mean(differences) if n else None
        half_width = 1.96 * statistics.stdev(differences) / n**0.5 if n > 1 else None
        rates = {v: [d['action'] for d in decisions if d['variant'] == v] for v in ('A', 'B')}
        metrics['ab_comparison'] = {
            'paired_units': n,
            'unit': 'persona_id × repetition; rounds averaged within unit',
            'rate_a': round(statistics.mean(rates['A']), 6) if rates['A'] else None,
            'rate_b': round(statistics.mean(rates['B']), 6) if rates['B'] else None,
            'difference_b_minus_a': round(delta, 6) if delta is not None else None,
            'ci95_normal_approx': [round(delta - half_width, 6), round(delta + half_width, 6)] if half_width is not None else None,
            'caveat': 'Descriptive normal approximation over synthetic paired units; small samples and interacting agents violate population inference assumptions. Not a real-user causal effect.',
        }
    return metrics
