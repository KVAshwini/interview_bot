const exampleSets = {
  devops: [
    "How do you handle a P1 outage?",
    "AKS pod keeps restarting with CrashLoopBackOff",
    "Kafka consumer lag is increasing",
    "Managed identity cannot read Key Vault secret",
    "A deployment failed in production"
  ],
  professions: [
    "How do you debug a production API issue?",
    "How do you optimize a slow SQL query?",
    "How do you build a REST API in Spring Boot?",
    "How do you manage state in a React application?",
    "How do you handle flaky automated tests?",
    "How do you gather business requirements?",
    "How do you prioritize a product backlog?",
    "How do you troubleshoot a slow database query?"
  ]
};

const uiMode = document.body.dataset.ui || "devops";
const examples = exampleSets[uiMode] || exampleSets.devops;

const q = document.querySelector("#question");
const mode = document.querySelector("#mode");
const voice = document.querySelector("#voice");
const categoryFilter = document.querySelector("#category-filter");
const view = document.querySelector("#view");
const result = document.querySelector("#result");
const examplesNode = document.querySelector("#examples");
const opacityToggle = document.querySelector("#opacity-toggle");
const voiceInput = document.querySelector("#voice-input");
const healthNode = document.querySelector("#health");
const missedNode = document.querySelector("#missed");
const refreshMissed = document.querySelector("#refresh-missed");

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
      body: JSON.stringify({
        question,
        mode: mode.value,
        voice: voice.value,
        category_filter: categoryFilter.value,
        view: view.value,
        limit: view.value === "interview" ? 1 : 3
      })
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
  if (payload.view === "interview") {
    const match = payload.matches[0];
    result.innerHTML = `
      <article class="match interview-match">
        <div class="meta">
          <span class="pill">${escapeHtml(match.confidence)} • ${match.score.toFixed(2)}</span>
          <span>${escapeHtml(match.topic)}</span>
        </div>
        <strong>${escapeHtml(match.question)}</strong>
        <div class="answer primary-answer">${escapeHtml(match.versions.natural || match.versions.quick)}</div>
        <div class="keywords">Keywords: ${escapeHtml(match.keywords.slice(0, 8).join(", "))}</div>
      </article>
    `;
    return;
  }
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

async function loadHealth() {
  try {
    const response = await fetch("/api/health");
    const payload = await response.json();
    healthNode.textContent = payload.ok
      ? `${payload.item_count} local answers ready`
      : "Local database needs rebuild";
    healthNode.className = payload.ok ? "health ok" : "health error";
  } catch (error) {
    healthNode.textContent = "Health check unavailable";
    healthNode.className = "health error";
  }
}

async function loadMissed() {
  try {
    const response = await fetch("/api/missed");
    const payload = await response.json();
    if (!payload.items.length) {
      missedNode.innerHTML = `<div class="empty small-text">No missed questions yet.</div>`;
      return;
    }
    missedNode.innerHTML = payload.items.slice(0, 5).map((item, index) => `
      <div class="missed-item">
        <button class="missed-question" type="button" data-index="${index}">${escapeHtml(item.query)}</button>
        <textarea class="missed-answer" data-index="${index}" placeholder="Add reviewed answer"></textarea>
        <button class="secondary small save-review" type="button" data-index="${index}">Save</button>
      </div>
    `).join("");
    missedNode.querySelectorAll(".missed-question").forEach((button) => {
      button.addEventListener("click", () => {
        q.value = payload.items[Number(button.dataset.index)].query;
      });
    });
    missedNode.querySelectorAll(".save-review").forEach((button) => {
      button.addEventListener("click", async () => {
        const index = Number(button.dataset.index);
        const answer = missedNode.querySelector(`.missed-answer[data-index="${index}"]`).value.trim();
        if (!answer) return;
        await saveReviewedAnswer(payload.items[index].query, answer);
      });
    });
  } catch (error) {
    missedNode.innerHTML = `<div class="empty error small-text">Could not load missed questions.</div>`;
  }
}

async function saveReviewedAnswer(question, answer) {
  const response = await fetch("/api/review-answer", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      question,
      answer,
      topic: "Reviewed Missed Question",
      category: "custom",
      keywords: categoryFilter.value === "all" ? [] : [categoryFilter.value]
    })
  });
  const payload = await response.json();
  if (!response.ok) {
    result.className = "empty error";
    result.textContent = payload.error || "Could not save reviewed answer.";
    return;
  }
  result.className = "empty";
  result.textContent = `Saved reviewed answer: ${payload.id}`;
  loadHealth();
}

function setupVoiceInput() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    voiceInput.disabled = true;
    voiceInput.title = "Speech recognition is not available in this browser.";
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.addEventListener("result", (event) => {
    q.value = event.results[0][0].transcript;
    ask();
  });
  recognition.addEventListener("start", () => {
    voiceInput.textContent = "Listening";
  });
  recognition.addEventListener("end", () => {
    voiceInput.textContent = "Voice";
  });
  voiceInput.addEventListener("click", () => recognition.start());
}

document.querySelector("#ask").addEventListener("click", ask);
document.querySelector("#clear").addEventListener("click", () => {
  q.value = "";
  result.className = "empty";
  result.textContent = "Ask a question to pull the closest local answer.";
});
opacityToggle.addEventListener("click", () => {
  const enabled = document.body.classList.toggle("transparent-mode");
  opacityToggle.setAttribute("aria-pressed", String(enabled));
  opacityToggle.textContent = enabled ? "Solid" : "Transparent";
});
refreshMissed.addEventListener("click", loadMissed);
q.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") ask();
});
setupVoiceInput();
loadHealth();
loadMissed();
