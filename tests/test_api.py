from fastapi.testclient import TestClient

from personalab.api import create_app


def test_api_run_lifecycle_and_exports(tmp_path):
    with TestClient(create_app(tmp_path / "api.db")) as client:
        assert client.get("/api/health").json()["status"] == "ok"
        assert len(client.get("/api/personas").json()) == 4
        assert len(client.get("/api/scenarios").json()) == 3
        response = client.post("/api/runs", json={"rounds": 1, "repetitions": 1})
        assert response.status_code == 201
        result = response.json()
        assert result["status"] == "completed"
        assert result["metrics"]["completed_decisions"] == 4
        assert client.get("/api/runs/" + result["id"]).json() == result
        assert client.get("/api/runs").json()[0]["id"] == result["id"]
        report = client.get("/api/runs/" + result["id"] + "/report")
        assert report.status_code == 200
        assert "attachment" in report.headers["content-disposition"]
        assert "offline" in report.text
        assert client.get("/api/runs/missing").status_code == 404
        assert client.get("/api/runs/missing/report").status_code == 404
        assert client.post("/api/runs", json={"personas": ["unknown"]}).status_code == 422
        assert client.post("/api/runs", json={"rounds": -1}).status_code == 422
        assert client.post("/api/runs", json={"api_key": "do-not-leak"}).status_code == 422


def test_llm_requires_environment_credentials_without_revealing_them(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with TestClient(create_app(tmp_path / "api.db")) as client:
        response = client.post("/api/runs", json={"provider": "openai", "rounds": 1})
        assert response.status_code == 503
        assert response.json()["detail"] == "llm_credentials_not_configured"


def test_console_and_static_assets_are_served(tmp_path):
    with TestClient(create_app(tmp_path / "api.db")) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "PersonaLab" in response.text
        assert client.get("/static/app.js").status_code == 200
        assert client.get("/static/style.css").status_code == 200
        assert client.get("/docs").status_code == 200


def test_admission_limit_returns_busy_without_starting_run(tmp_path):
    app = create_app(tmp_path / "api.db")
    with TestClient(app) as client:
        app.state.active_runs = 2
        response = client.post("/api/runs", json={"rounds": 1})
        assert response.status_code == 429
        assert response.json()["detail"] == "experiment_capacity_reached"


def test_literature_api_returns_exact_grounded_candidate(tmp_path):
    with TestClient(create_app(tmp_path / "api.db")) as client:
        response = client.post(
            "/api/evidence",
            json={"text": "合作促进共享。风险影响决策。", "source": "note.txt", "keywords": ["合作"]},
        )
        assert response.status_code == 200
        assert response.json()[0]["quote"] == "合作促进共享。"
        assert (
            client.post("/api/evidence", json={"text": "test", "source": "x", "keywords": []}).status_code
            == 422
        )
