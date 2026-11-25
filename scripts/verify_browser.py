"""Optional real-browser smoke check. Requires pip install playwright and Chrome/Edge."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'artifacts' / 'browser'
OUTPUT.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PERSONALAB_DB=str(OUTPUT / 'smoke.db'))
server = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'personalab.api:create_app', '--factory', '--port', '8765'], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            with urlopen('http://127.0.0.1:8765/api/health', timeout=1) as response:
                assert json.load(response)['status'] == 'ok'
            break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError('server failed to start')
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1512, 'height': 1100}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto('http://127.0.0.1:8765')
        page.wait_for_selector('.persona-card')
        assert page.locator('.persona-card').count() == 4
        page.screenshot(path=str(OUTPUT / 'studio-desktop.png'), full_page=True)
        page.click('#sample-button')
        page.wait_for_function("document.getElementById('run-status').textContent === 'COMPLETED'")
        assert page.locator('#metric-decisions').inner_text() == '120'
        assert page.locator('#trace-body tr').count() == 100
        assert 'matched synthetic units' in page.locator('#ab-summary').inner_text()
        page.screenshot(path=str(OUTPUT / 'results-desktop.png'), full_page=True)
        with page.expect_download() as download_info:
            page.click('#json-download')
        download = download_info.value
        download.save_as(str(OUTPUT / 'downloaded-run.json'))
        downloaded = json.loads((OUTPUT / 'downloaded-run.json').read_text(encoding='utf-8'))
        assert downloaded['status'] == 'completed'
        # Model-provided HTML is rendered literally; it cannot create DOM nodes.
        page.evaluate("""() => {
          currentRun.decisions[0].explanation = '<img src=x onerror=alert(1)>';
          renderRun(currentRun);
        }""")
        assert page.locator('#trace-body img').count() == 0
        assert '<img' in page.locator('#trace-body tr').first.inner_text()
        page.set_viewport_size({'width': 390, 'height': 844})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        page.screenshot(path=str(OUTPUT / 'studio-mobile.png'), full_page=True)
        assert not errors, errors
        browser.close()
    print(json.dumps({'http': 'ok', 'browser': 'Edge Chromium', 'desktop': '1512x1100', 'mobile': '390x844', 'decisions': 120, 'download': 'verified', 'html_explanation': 'rendered_as_text', 'page_errors': errors}))
finally:
    server.terminate()
    server.wait(timeout=10)
