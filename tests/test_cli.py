import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cli(*args):
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, "-m", "personalab.cli", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=15,
    )


def test_cli_runs_config_and_writes_reports(tmp_path):
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"scenario": "product_ab", "rounds": 1, "repetitions": 2}), encoding="utf-8")
    result = cli(
        "run", "--config", str(config), "--output", str(tmp_path / "out"), "--db", str(tmp_path / "cli.db")
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["status"] == "completed"
    run = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert run["config"]["scenario"] == "product_ab"
    assert (tmp_path / "out" / "report.md").is_file()


def test_cli_extract_and_invalid_config(tmp_path):
    source = tmp_path / "note.txt"
    source.write_text("Cooperation helps groups. Risk affects choices.", encoding="utf-8")
    result = cli("extract", str(source), "--keywords", "cooperation")
    assert result.returncode == 0
    assert json.loads(result.stdout)[0]["quote"] == "Cooperation helps groups."
    config = tmp_path / "bad.json"
    config.write_text('{"rounds":0}', encoding="utf-8")
    result = cli("run", "--config", str(config))
    assert result.returncode == 2
    assert "invalid_input" in result.stderr


def test_cli_help_is_usable():
    result = cli("--help")
    assert result.returncode == 0
    assert "serve" in result.stdout
    assert "extract" in result.stdout
