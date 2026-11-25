"""Bounded asynchronous agent harness with round barriers and inspectable attempts."""

import asyncio
import hashlib
import json
import platform
import time
import uuid
from datetime import datetime, timezone

from pydantic import ValidationError

from . import __version__
from .evaluation import evaluate
from .providers import Provider, ProviderError
from .schemas import Decision, ExperimentConfig, Persona
from .scenarios import context_for, settle, validate_action


class RunFailure(Exception):
    pass


def unit_seed(seed: int, repetition: int, round_number: int, persona_id: str, role: str) -> int:
    key = f'{seed}:{repetition}:{round_number}:{persona_id}:{role}'.encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:4], 'big')


async def run_experiment(config: ExperimentConfig, registry: dict[str, Persona], provider: Provider) -> dict:
    unknown = set(config.personas) - registry.keys()
    if unknown:
        raise ValueError('unknown persona IDs: ' + ', '.join(sorted(unknown)))
    started = time.perf_counter()
    config_data = config.model_dump(mode='json')
    config_hash = hashlib.sha256(json.dumps(config_data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    run = {
        'id': str(uuid.uuid4()),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'status': 'running', 'error': None,
        'config': config_data,
        'persona_snapshot': {key: registry[key].model_dump(mode='json') for key in config.personas},
        'provenance': {
            'version': __version__, 'python': platform.python_version(),
            'provider': config.provider,
            'model': 'seeded-heuristic-v1' if config.provider == 'offline' else config.model,
            'config_sha256': config_hash,
        },
        'calls_used': 0, 'attempts': [], 'decisions': [],
    }
    semaphore = asyncio.Semaphore(config.concurrency)
    allowed_refs = {f'{group}.{key}' for group in ('traits', 'social', 'preferences') for key in registry[config.personas[0]].model_dump()[group]}

    async def decide(persona, history, variant, rep, rnd, role='player', extra=None):
        context = context_for(config, persona, history, variant)
        context.update({'role': role, 'round': rnd, 'repetition': rep})
        if role == 'investor':
            context['rules'] = dict(context['rules'], action_max=10)
        if extra:
            context.update(extra)
        seed = unit_seed(config.seed, rep, rnd, persona.id, role)
        request = {'context': context, 'seed': seed}
        for retry in range(config.max_retries + 1):
            async with semaphore:
                if run['calls_used'] >= config.max_calls:
                    raise RunFailure('call_budget_exhausted')
                run['calls_used'] += 1
                trace = {
                    'call_index': run['calls_used'], 'persona_id': persona.id, 'repetition': rep,
                    'round': rnd, 'variant': variant, 'role': role, 'retry': retry,
                    'request': request, 'input_tokens': 0, 'output_tokens': 0,
                }
                attempt_start = time.perf_counter()
                try:
                    response = await asyncio.wait_for(provider.decide(request), timeout=config.timeout_seconds)
                    trace['input_tokens'] = response.input_tokens
                    trace['output_tokens'] = response.output_tokens
                    decision = Decision.model_validate_json(response.content)
                    validate_action('trust_investor' if role == 'investor' else config.scenario, decision.action)
                    if not set(decision.parameter_refs).issubset(allowed_refs):
                        raise ValueError('unknown parameter reference')
                    trace['status'] = 'ok'
                except TimeoutError:
                    trace['status'] = 'timeout'
                except ProviderError as exc:
                    trace['status'] = exc.category
                except (ValidationError, ValueError):
                    trace['status'] = 'invalid_output'
                except Exception:
                    # Exception text can contain API keys or upstream request bodies.
                    trace['status'] = 'provider_error'
                trace['elapsed_ms'] = round((time.perf_counter() - attempt_start) * 1000, 3)
                run['attempts'].append(trace)
                if trace['status'] == 'ok':
                    return {
                        'persona_id': persona.id, 'repetition': rep, 'round': rnd,
                        'variant': variant, 'role': role, 'seed': seed,
                        'cooperation_parameter': persona.social.cooperation,
                        **decision.model_dump(mode='json'),
                    }
                if retry == config.max_retries or trace['status'] in {'authentication_failed', 'upstream_rejected'}:
                    raise RunFailure(trace['status'])
            # Backoff is bounded, outside the concurrency slot; retries consume call budget.
            await asyncio.sleep(min(0.1 * 2**retry, 0.8))
        raise RunFailure('provider_error')

    async def barrier(jobs):
        results = await asyncio.gather(*jobs, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                raise RunFailure(str(result) if isinstance(result, RunFailure) else 'provider_error')
        return results

    factor = 2 if config.scenario in {'trust_game', 'product_ab'} else 1
    planned = len(config.personas) * config.rounds * config.repetitions * factor
    try:
        for rep in range(config.repetitions):
            for variant in (('A', 'B') if config.scenario == 'product_ab' else ('A',)):
                history = []
                for rnd in range(1, config.rounds + 1):
                    personas = [registry[key] for key in config.personas]
                    if config.scenario == 'trust_game':
                        # Each persona invests once; the next persona acts as trustee (cyclic pairing).
                        # For a one-person run this is explicitly self-play.
                        transfers = await barrier([decide(p, history, variant, rep, rnd, 'investor') for p in personas])
                        trustees = personas[1:] + personas[:1]
                        returns = await barrier([
                            decide(p, history, variant, rep, rnd, 'trustee', {'received': transfer['action'] * 3, 'transfer': transfer['action'], 'partner_id': transfer['persona_id']})
                            for p, transfer in zip(trustees, transfers, strict=True)
                        ])
                        rows = []
                        for transfer, returned in zip(transfers, returns, strict=True):
                            payoffs = settle('trust_game', [transfer['action'], returned['action']])
                            pair_id = f"{rep}:{rnd}:{transfer['persona_id']}"
                            rows.extend([dict(transfer, payoff=payoffs[0], pair_id=pair_id), dict(returned, payoff=payoffs[1], pair_id=pair_id)])
                    else:
                        choices = await barrier([decide(p, history, variant, rep, rnd) for p in personas])
                        payoffs = settle(config.scenario, [choice['action'] for choice in choices])
                        rows = [dict(choice, payoff=payoff) for choice, payoff in zip(choices, payoffs, strict=True)]
                    run['decisions'].extend(rows)
                    history.append({
                        'round': rnd,
                        'mean_action': sum(row['action'] for row in rows if row['role'] != 'trustee') / len(personas),
                        'observed': [{'persona_id': row['persona_id'], 'role': row['role'], 'action': row['action'], 'payoff': row['payoff']} for row in rows],
                    })
        run['status'] = 'completed'
    except RunFailure as exc:
        run['status'] = 'failed'
        run['error'] = str(exc)
    run['attempts'].sort(key=lambda row: row['call_index'])
    run['metrics'] = evaluate(run['decisions'], run['attempts'], planned, config.scenario)
    run['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 3)
    return run
