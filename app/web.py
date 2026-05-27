import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app.answer_engine import answer_payload
from app.config import DB_PATH, PROJECT_ROOT
from app.session_log import log_answer


STATIC_DIR = PROJECT_ROOT / "static"
ALLOWED_MODES = {"instant", "detailed"}
ALLOWED_VOICES = {"natural", "raw"}


class RequestError(ValueError):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


def _json_response(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _read_static(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_answer_request(body: str) -> dict:
    try:
        payload = json.loads(body) if body else {}
    except json.JSONDecodeError as exc:
        raise RequestError("Request body must be valid JSON") from exc

    question = str(payload.get("question", "")).strip()
    if not question:
        raise RequestError("question is required")

    mode = str(payload.get("mode", "instant"))
    if mode not in ALLOWED_MODES:
        raise RequestError(f"mode must be one of: {', '.join(sorted(ALLOWED_MODES))}")

    voice = str(payload.get("voice", "natural"))
    if voice not in ALLOWED_VOICES:
        raise RequestError(f"voice must be one of: {', '.join(sorted(ALLOWED_VOICES))}")

    try:
        limit = int(payload.get("limit", 3))
    except (TypeError, ValueError) as exc:
        raise RequestError("limit must be an integer") from exc
    if limit < 1 or limit > 10:
        raise RequestError("limit must be between 1 and 10")

    return {"question": question, "mode": mode, "voice": voice, "limit": limit}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: str, content_type: str = "text/plain") -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, status: int, payload: dict) -> None:
        self._send(status, _json_response(payload), "application/json")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._send(200, _read_static(STATIC_DIR / "index.html"), "text/html")
        elif path == "/static/styles.css":
            self._send(200, _read_static(STATIC_DIR / "styles.css"), "text/css")
        elif path == "/static/app.js":
            self._send(200, _read_static(STATIC_DIR / "app.js"), "text/javascript")
        elif path == "/health":
            self._send_json(200, {"ok": True, "db": str(DB_PATH)})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/answer":
            self._send_json(404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        try:
            request = parse_answer_request(body)
            answer = answer_payload(
                request["question"],
                mode=request["mode"],
                limit=request["limit"],
                voice=request["voice"],
            )
        except RequestError as exc:
            self._send_json(exc.status, {"error": str(exc)})
            return

        log_answer(answer)
        self._send_json(200, answer)

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
