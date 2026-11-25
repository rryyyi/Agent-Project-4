"use strict";
let personas = [];
let currentRun = null;
const $ = (id) => document.getElementById(id);
const descriptions = {
  public_goods: "同时贡献，观察个体利益与共同收益的权衡。",
  trust_game: "投资者先转账，受托者观察三倍金额后决定返还比例。",
  product_ab: "使用匹配人格和种子，比较两种产品描述下的模拟选择。",
};
const symbols = ["◈", "◎", "◇", "✳"];
async function api(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    const detail =
      typeof data.detail === "string" ? data.detail : "invalid_input";
    throw new Error(detail);
  }
  return response.json();
}
function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function updateEstimate() {
  const count = document.querySelectorAll(".persona-checkbox:checked").length;
  const factor = $("scenario").value === "public_goods" ? 1 : 2;
  const planned =
    count * Number($("rounds").value) * Number($("repetitions").value) * factor;
  $("run-hint").textContent =
    `预计 ${planned} 次决策 · ${$("provider").value === "offline" ? "Offline 无需 API 密钥" : "LLM 调用可能产生费用"}`;
  $("scenario-description").textContent = descriptions[$("scenario").value];
  $("variants").hidden = $("scenario").value !== "product_ab";
  $("model-field").hidden = $("provider").value !== "openai";
}
function renderPersonas() {
  const options = $("persona-options");
  const cards = $("persona-cards");
  options.replaceChildren();
  cards.replaceChildren();
  personas.forEach((p, index) => {
    const label = node("label", undefined, "persona-option");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "persona-checkbox";
    checkbox.value = p.id;
    checkbox.checked = true;
    checkbox.addEventListener("change", updateEstimate);
    label.append(checkbox, node("span", p.name.split(" · ")[0]));
    options.append(label);
    const card = node("article", undefined, "persona-card");
    card.append(
      node("div", symbols[index], "persona-symbol"),
      node("h3", p.name),
      node("p", p.description),
    );
    [
      ["Cooperation", p.social.cooperation],
      ["Risk tolerance", p.preferences.risk_tolerance],
      ["Reciprocity", p.social.reciprocity],
    ].forEach(([name, value]) => {
      const row = node("div", undefined, "trait-row");
      const progress = document.createElement("progress");
      progress.max = 1;
      progress.value = value;
      progress.setAttribute("aria-label", `${name}: ${value}`);
      row.append(node("span", name), progress, node("span", value.toFixed(2)));
      card.append(row);
    });
    cards.append(card);
  });
}
function setStatus(status) {
  $("run-status").textContent = status.toUpperCase();
  $("run-status").className = "badge " + status;
}
function renderRun(run) {
  currentRun = run;
  setStatus(run.status);
  $("empty-state").hidden = true;
  $("result-content").hidden = false;
  $("trace-section").hidden = false;
  $("run-id").textContent =
    `RUN ${run.id.slice(0, 8)} · SEED ${run.config.seed}`;
  $("provider-label").textContent =
    run.provenance.provider === "offline"
      ? "OFFLINE · SYNTHETIC"
      : `LLM · ${run.provenance.model}`;
  $("metric-decisions").textContent = run.metrics.completed_decisions;
  $("metric-valid").textContent =
    `${(run.metrics.legal_decision_rate * 100).toFixed(0)}%`;
  $("metric-calls").textContent = run.calls_used;
  $("metric-elapsed").textContent =
    run.elapsed_ms >= 1000
      ? `${(run.elapsed_ms / 1000).toFixed(1)}s`
      : `${Math.round(run.elapsed_ms)}ms`;
  $("usage-label").textContent =
    `TOKENS ${run.metrics.input_tokens} IN / ${run.metrics.output_tokens} OUT`;
  $("chart-unit").textContent =
    run.config.scenario === "public_goods"
      ? "贡献数量 / 10"
      : run.config.scenario === "trust_game"
        ? "转账金额与返还比例混合 · 请查看轨迹"
        : "选择比例 / 1";
  const chart = $("chart");
  chart.replaceChildren();
  Object.entries(run.metrics.by_persona).forEach(([id, group]) => {
    const row = node("div", undefined, "bar-row");
    const p = personas.find((item) => item.id === id);
    const track = node("div", undefined, "bar-track");
    const fill = node("div", undefined, "bar-fill");
    fill.style.width = `${Math.max(0, Math.min(100, (group.mean_action / (run.config.scenario === "product_ab" ? 1 : 10)) * 100))}%`;
    track.append(fill);
    row.append(
      node("span", p ? p.name.split(" · ")[0] : id, "bar-label"),
      track,
      node("span", group.mean_action.toFixed(2), "bar-value"),
    );
    chart.append(row);
  });
  const ab = run.metrics.ab_comparison;
  $("ab-summary").hidden = !ab;
  if (ab) {
    const pct = (value) =>
      value === null ? "N/A" : `${(value * 100).toFixed(1)}%`;
    const interval = ab.ci95_normal_approx
      ? ab.ci95_normal_approx.map(pct).join(" to ")
      : "insufficient units";
    $("ab-summary").textContent =
      `A ${pct(ab.rate_a)} → B ${pct(ab.rate_b)} · Δ ${pct(ab.difference_b_minus_a)}\n${ab.paired_units} matched synthetic units · 95% normal approximation: ${interval}\n仅描述合成群体，不代表真实用户转化率或因果效应。`;
  }
  $("report-download").href = `/api/runs/${encodeURIComponent(run.id)}/report`;
  const body = $("trace-body");
  body.replaceChildren();
  run.decisions.slice(0, 100).forEach((d) => {
    const tr = node("tr");
    [
      d.persona_id,
      `${d.repetition + 1} / ${d.round}`,
      `${d.variant} · ${d.role}`,
      d.action,
      d.payoff,
      d.explanation,
    ].forEach((value) => tr.append(node("td", String(value))));
    body.append(tr);
  });
  $("error").hidden = !run.error;
  if (run.error)
    $("error").textContent =
      `实验终止：${run.error}。有效的已结算回合保留在 JSON；调用轨迹包含失败分类。`;
}
async function refreshHistory() {
  const runs = await api("/api/runs?limit=8");
  const list = $("history-list");
  list.replaceChildren();
  if (!runs.length) {
    list.textContent = "No runs yet. Run your first experiment above.";
    return;
  }
  runs.forEach((run) => {
    const button = node("button", undefined, "history-item");
    button.type = "button";
    button.append(
      node(
        "span",
        descriptions[run.config.scenario] ? run.config.scenario : "experiment",
      ),
      node(
        "span",
        `${run.config.provider} · ${run.metrics.completed_decisions} decisions`,
      ),
      node("span", run.id.slice(0, 8), "history-id"),
      node("span", `${run.status} ↗`),
    );
    button.addEventListener("click", async () => {
      try {
        renderRun(await api(`/api/runs/${run.id}`));
        $("studio").scrollIntoView({ behavior: "smooth" });
      } catch (error) {
        showError(error);
      }
    });
    list.append(button);
  });
}
function showError(error) {
  const messages = {
    llm_credentials_not_configured:
      "服务端尚未配置 OPENAI_API_KEY。请先配置环境变量，或选择 Offline 演示。",
    experiment_capacity_reached: "实验并发已满，请稍后再试。",
    invalid_input: "请检查实验参数、角色选择和输入范围。",
  };
  $("error").textContent =
    messages[error.message] || `请求失败：${error.message}`;
  $("error").hidden = false;
}
$("run-form").addEventListener("change", updateEstimate);
$("run-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const selected = [
    ...document.querySelectorAll(".persona-checkbox:checked"),
  ].map((el) => el.value);
  if (!selected.length) {
    showError(new Error("invalid_input"));
    return;
  }
  const config = {
    scenario: $("scenario").value,
    provider: $("provider").value,
    personas: selected,
    rounds: Number($("rounds").value),
    repetitions: Number($("repetitions").value),
    seed: Number($("seed").value),
    max_calls: Number($("max-calls").value),
    max_retries: Number($("retries").value),
    model: $("model").value,
    variant_a: $("variant-a").value,
    variant_b: $("variant-b").value,
  };
  $("run-button").disabled = true;
  $("sample-button").disabled = true;
  $("error").hidden = true;
  setStatus("running");
  try {
    const run = await api("/api/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config),
    });
    renderRun(run);
    await refreshHistory();
  } catch (error) {
    setStatus("failed");
    showError(error);
  } finally {
    $("run-button").disabled = false;
    $("sample-button").disabled = false;
  }
});
$("sample-button").addEventListener("click", () => {
  $("scenario").value = "product_ab";
  $("provider").value = "offline";
  updateEstimate();
  $("run-form").requestSubmit();
});
$("refresh-history").addEventListener("click", () =>
  refreshHistory().catch(showError),
);
$("json-download").addEventListener("click", () => {
  if (!currentRun) return;
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(currentRun, null, 2)], {
      type: "application/json",
    }),
  );
  const link = node("a");
  link.href = url;
  link.download = `personalab-${currentRun.id}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
async function initialize() {
  try {
    const [health, registry] = await Promise.all([
      api("/api/health"),
      api("/api/personas"),
    ]);
    personas = registry;
    renderPersonas();
    updateEstimate();
    $("connection-text").textContent = `Connected · v${health.version}`;
    await refreshHistory();
  } catch (error) {
    $("connection-text").textContent = "Disconnected";
    showError(error);
  }
}
initialize();
