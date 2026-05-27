import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.answer_engine import answer_payload
from app.config import DB_PATH
from app.session_log import log_answer


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Interview Help Bot</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8f5;
      --panel: #ffffff;
      --ink: #1f2933;
      --muted: #64707d;
      --line: #d9ded6;
      --accent: #176b5b;
      --accent-2: #8a4b22;
      --soft: #e8f2ef;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }
    header {
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,.88);
      backdrop-filter: blur(10px);
      position: sticky;
      top: 0;
      z-index: 1;
    }
    .wrap { max-width: 1120px; margin: 0 auto; padding: 18px 20px; }
    .top { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
    h1 { margin: 0; font-size: 22px; font-weight: 720; }
    .status { color: var(--muted); font-size: 13px; }
    main.wrap { display: grid; grid-template-columns: 360px 1fr; gap: 18px; align-items: start; }
    section, aside {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }
    label { display: block; font-size: 13px; color: var(--muted); margin-bottom: 8px; }
    textarea {
      width: 100%;
      min-height: 150px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 12px;
      font: inherit;
      color: var(--ink);
      background: #fbfcfa;
    }
    .controls { display: flex; gap: 8px; margin-top: 12px; align-items: center; flex-wrap: wrap; }
    button, select {
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      font: inherit;
      height: 38px;
      padding: 0 12px;
    }
    button.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
    button.secondary { color: var(--accent); }
    .chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .chip { border: 1px solid var(--line); border-radius: 999px; padding: 6px 10px; font-size: 12px; color: var(--muted); background: #fbfcfa; cursor: pointer; }
    .result { display: grid; gap: 12px; }
    .match { border: 1px solid var(--line); border-radius: 8px; padding: 14px; background: #fff; }
    .meta { display: flex; gap: 8px; flex-wrap: wrap; color: var(--muted); font-size: 13px; margin-bottom: 10px; }
    .pill { background: var(--soft); color: var(--accent); border-radius: 999px; padding: 4px 8px; }
    .answer { white-space: pre-wrap; line-height: 1.5; }
    .keywords { margin-top: 12px; color: var(--muted); font-size: 13px; }
    .memory { margin-top: 12px; border-top: 1px solid var(--line); padding-top: 10px; color: var(--accent-2); font-size: 13px; }
    .empty { color: var(--muted); line-height: 1.5; }
    @media (max-width: 820px) { main.wrap { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header>
    <div class="wrap top">
      <h1>Interview Help Bot</h1>
      <div class="status">Local cache • SQLite • no network required</div>
    </div>
  </header>
  <main class="wrap">
    <aside>
      <label for="question">Question or scenario</label>
      <textarea id="question" placeholder="Example: Production is down and users cannot login. What do you do?"></textarea>
      <div class="controls">
        <select id="mode" aria-label="Answer mode">
          <option value="instant">Instant</option>
          <option value="detailed">Detailed</option>
        </select>
        <select id="voice" aria-label="Voice style">
          <option value="natural">Natural</option>
          <option value="raw">Raw</option>
        </select>
        <button class="primary" id="ask">Answer</button>
        <button class="secondary" id="clear">Clear</button>
      </div>
      <div class="chips" id="examples"></div>
    </aside>
    <section>
      <div id="result" class="empty">Ask a question to pull the closest local answer.</div>
    </section>
  </main>
  <script>
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

    examples.forEach(text => {
      const chip = document.createElement("button");
      chip.className = "chip";
      chip.type = "button";
      chip.textContent = text;
      chip.addEventListener("click", () => { q.value = text; ask(); });
      examplesNode.appendChild(chip);
    });

    function escapeHtml(value) {
      return value.replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));
    }

    async function ask() {
      const question = q.value.trim();
      if (!question) return;
      result.className = "empty";
      result.textContent = "Searching local library...";
      const response = await fetch("/api/answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question, mode: mode.value, voice: voice.value, limit: 3})
      });
      const payload = await response.json();
      if (!payload.matches.length) {
        result.textContent = "No local answer found yet. Add this to the library.";
        return;
      }
      result.className = "result";
      result.innerHTML = payload.matches.map(match => `
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
          ${match.memory.length ? `<div class="memory">Memory: ${match.memory.map(item => escapeHtml(item.name)).join(", ")}</div>` : ""}
        </article>
      `).join("");
    }

    document.querySelector("#ask").addEventListener("click", ask);
    document.querySelector("#clear").addEventListener("click", () => { q.value = ""; result.className = "empty"; result.textContent = "Ask a question to pull the closest local answer."; });
    q.addEventListener("keydown", event => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") ask();
    });
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: str, content_type: str = "text/plain") -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._send(200, PAGE, "text/html")
        elif path == "/health":
            self._send(200, json.dumps({"ok": True, "db": str(DB_PATH)}), "application/json")
        else:
            self._send(404, "Not found")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/answer":
            self._send(404, "Not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body) if body else {}
        question = str(payload.get("question", "")).strip()
        mode = str(payload.get("mode", "instant"))
        voice = str(payload.get("voice", "natural"))
        limit = int(payload.get("limit", 3))
        answer = answer_payload(question, mode=mode, limit=limit, voice=voice)
        log_answer(answer)
        self._send(200, json.dumps(answer), "application/json")

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the local interview helper web UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Interview Help Bot running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
