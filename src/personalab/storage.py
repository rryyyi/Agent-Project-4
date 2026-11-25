"""Atomic terminal-run snapshots in SQLite; one connection per operation."""

import json
import sqlite3
from pathlib import Path


class Store:
    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path, timeout=10) as conn:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL)')

    def save(self, run: dict) -> None:
        with sqlite3.connect(self.path, timeout=10) as conn:
            conn.execute('INSERT INTO runs(id, created_at, payload) VALUES (?, ?, ?)', (run['id'], run['created_at'], json.dumps(run, ensure_ascii=False, allow_nan=False)))

    def get(self, run_id: str) -> dict | None:
        with sqlite3.connect(self.path, timeout=10) as conn:
            row = conn.execute('SELECT payload FROM runs WHERE id = ?', (run_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list(self, limit: int = 20) -> list[dict]:
        with sqlite3.connect(self.path, timeout=10) as conn:
            rows = conn.execute('SELECT payload FROM runs ORDER BY created_at DESC LIMIT ?', (min(max(limit, 1), 100),)).fetchall()
        return [{k: r[k] for k in ('id', 'created_at', 'status', 'config', 'metrics')} for r in (json.loads(row[0]) for row in rows)]
