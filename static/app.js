const examples = [
  "How do you handle a P1 outage?",
  "AKS pod keeps restarting with CrashLoopBackOff",
  "Kafka consumer lag is increasing",
  "Managed identity cannot read Key Vault secret",
  "A deployment failed in production"
];

const q = document.querySelector("#question");
const mode = document.querySelector("#mode");
const voice = document.querySelector("#voice");
const result = document.querySelector("#result");
const examplesNode = document.querySelector("#examples");

examples.forEach((text) => {
  const chip = document.createElement("button");
  chip.className = "chip";
  chip.type = "button";
  chip.textContent = text;
  chip.addEventListener("click", () => {
    q.value = text;
    ask();
  });
  examplesNode.appendChild(chip);
});

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#039;"
  }[ch]));
}

async function ask() {
  const question = q.value.trim();
  if (!question) return;

  result.className = "empty";
  result.textContent = "Searching local library...";

  try {
    const response = await fetch("/api/answer", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, mode: mode.value, voice: voice.value, limit: 3})
    });
    const payload = await response.json();
    if (!response.ok) {
      result.className = "empty error";
      result.textContent = payload.error || "Request failed.";
      return;
    }
    renderMatches(payload);
  } catch (error) {
    result.className = "empty error";
    result.textContent = "Could not reach the local interview bot server.";
  }
}

function renderMatches(payload) {
  if (!payload.matches.length) {
    result.className = "empty";
    result.textContent = "No local answer found yet. Add this to the library.";
    return;
  }

  result.className = "result";
  result.innerHTML = payload.matches.map((match) => `
    <article class="match">
      <div class="meta">
        <span class="pill">${escapeHtml(match.confidence)} • ${match.score.toFixed(2)}</span>
        <span>${escapeHtml(match.topic)}</span>
        <span>${escapeHtml(match.source_file)}</span>
      </div>
      <strong>${escapeHtml(match.question)}</strong>
      <div class="answer"><strong>Quick:</strong> ${escapeHtml(match.versions.quick)}</div>
      <div class="answer"><strong>Natural:</strong> ${escapeHtml(match.versions.natural)}</div>
      <div class="answer"><strong>Stored:</strong> ${escapeHtml(match.versions.detailed)}</div>
      <div class="keywords">Keywords: ${escapeHtml(match.keywords.slice(0, 8).join(", "))}</div>
      ${match.explanation.needs_review ? `<div class="memory">Review: low confidence. Overlap: ${escapeHtml(match.explanation.overlap.join(", ") || "none")}</div>` : ""}
      ${match.memory.length ? `<div class="memory">Memory: ${match.memory.map((item) => escapeHtml(item.name)).join(", ")}</div>` : ""}
    </article>
  `).join("");
}

document.querySelector("#ask").addEventListener("click", ask);
document.querySelector("#clear").addEventListener("click", () => {
  q.value = "";
  result.className = "empty";
  result.textContent = "Ask a question to pull the closest local answer.";
});
q.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") ask();
});
