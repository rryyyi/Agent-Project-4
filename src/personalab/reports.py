"""Portable reports with explicit provenance and modeling limitations."""

import html
import json


def markdown_report(run: dict) -> str:
    def safe(value):
        return html.escape(str(value)).replace('|', '&#124;').replace('\n', ' ')

    lines = [
        '# PersonaLab · Experiment report', '',
        f"- Run: `{run['id']}`",
        f"- Status: **{safe(run['status'])}**",
        f"- Provider: **{safe(run['provenance']['provider'])}**",
        f"- Model: {safe(run['provenance']['model'])}",
        f"- Created: {safe(run['created_at'])}",
        f"- Software: {safe(run['provenance']['version'])}",
        f"- Config SHA-256: `{run['provenance']['config_sha256']}`", '',
        '> Synthetic-agent experiment. Offline behavior is a seeded heuristic baseline, not a real LLM evaluation. Neither provider validates predictions about real people. Explanations and confidence are self-reported.', '',
        '## Metrics', '', '```json', json.dumps(run['metrics'], indent=2, ensure_ascii=False), '```', '',
        '## Configuration', '', '```json', json.dumps(run['config'], indent=2, ensure_ascii=False), '```', '',
        '## Decision sample (first 40)', '',
        '| Persona | Rep | Round | Variant / Role | Action | Payoff | Explanation |',
        '| --- | --- | --- | --- | --- | --- | --- |',
    ]
    for d in run['decisions'][:40]:
        lines.append('| ' + ' | '.join(safe(v) for v in [d['persona_id'], d['repetition'], d['round'], d['variant'] + '/' + d['role'], d['action'], d['payoff'], d['explanation']]) + ' |')
    lines += ['', '## Interpretation limits', '',
        '- Persona parameters are hand-authored assumptions. Big Five is a parameter vocabulary, not a validated psychometric instrument here.',
        '- Cooperation alignment is a declared proxy; offline policies directly use those parameters, so this is an implementation check, not scientific validation.',
        '- A/B uses matched synthetic units. Its normal-approximation interval is descriptive; repeated interactions and small samples limit inference.',
        '- Trust-role means mix transfer amounts and return fractions; inspect role-level traces rather than comparing the aggregate as a common unit.',
        '- Token usage is provider-reported; unavailable usage is zero. No currency cost is estimated.',
        '- This version persists terminal snapshots; it has no durable job queue or mid-run crash recovery.',
        '- Full decisions, attempts, timings, prompts/context and persona snapshots are available in the JSON export.', '',
    ]
    return '\n'.join(lines)
