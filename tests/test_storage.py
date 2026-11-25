import sqlite3

from personalab.storage import Store


def test_store_closes_connections_after_success_and_failure(tmp_path, monkeypatch):
    original_connect = sqlite3.connect
    opened = []

    class TrackedConnection(sqlite3.Connection):
        def close(self):
            self.was_closed = True
            super().close()

    def connect(*args, **kwargs):
        conn = original_connect(*args, **kwargs, factory=TrackedConnection)
        conn.was_closed = False
        opened.append(conn)
        return conn

    monkeypatch.setattr(sqlite3, "connect", connect)
    store = Store(tmp_path / "runs.db")
    assert store.get("missing") is None
    assert store.list() == []
    run = {"id": "one", "created_at": "2026-11-25", "status": "completed", "config": {}, "metrics": {}}
    store.save(run)
    try:
        store.save(run)
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("duplicate insert must fail")
    assert len(opened) == 5
    assert all(conn.was_closed for conn in opened)
