import ctypes
import sys
import tkinter as tk
from tkinter import ttk

from app.answer_engine import answer_payload
from app.session_log import log_answer


WDA_NONE = 0x00000000
WDA_MONITOR = 0x00000001
WDA_EXCLUDEFROMCAPTURE = 0x00000011


def set_window_capture_exclusion(hwnd: int, enabled: bool, user32: object | None = None) -> bool:
    if user32 is None:
        user32 = ctypes.windll.user32
    affinity = WDA_EXCLUDEFROMCAPTURE if enabled else WDA_NONE
    if user32.SetWindowDisplayAffinity(hwnd, affinity):
        return True
    if enabled and user32.SetWindowDisplayAffinity(hwnd, WDA_MONITOR):
        return True
    return False


def apply_capture_exclusion(root: tk.Tk, enabled: bool) -> bool:
    if sys.platform != "win32":
        return False
    hwnd = int(root.winfo_id())
    return set_window_capture_exclusion(hwnd, enabled)


class OverlayApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Interview Help Bot Overlay")
        self.root.geometry("760x640+120+80")
        self.root.minsize(520, 420)
        self.root.attributes("-topmost", True)
        self.opacity = tk.DoubleVar(value=0.88)
        self.capture_hidden = tk.BooleanVar(value=True)
        self.mode = tk.StringVar(value="instant")
        self.voice = tk.StringVar(value="natural")
        self.status = tk.StringVar(value="Private overlay ready")

        self._build()
        self.root.after(100, self._apply_privacy_mode)

    def _build(self) -> None:
        self.root.configure(bg="#f7f8f5")
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x", pady=(0, 10))

        ttk.Button(toolbar, text="Transparency", command=self._toggle_opacity).pack(side="left")
        ttk.Checkbutton(
            toolbar,
            text="Hide from screen capture",
            variable=self.capture_hidden,
            command=self._apply_privacy_mode,
        ).pack(side="left", padx=8)
        ttk.Label(toolbar, textvariable=self.status).pack(side="right")

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(0, 8))
        ttk.Label(controls, text="Mode").pack(side="left")
        ttk.Combobox(controls, textvariable=self.mode, values=("instant", "detailed"), width=10, state="readonly").pack(
            side="left", padx=(6, 14)
        )
        ttk.Label(controls, text="Voice").pack(side="left")
        ttk.Combobox(controls, textvariable=self.voice, values=("natural", "raw"), width=10, state="readonly").pack(
            side="left", padx=(6, 14)
        )
        ttk.Button(controls, text="Answer", command=self.ask).pack(side="left")
        ttk.Button(controls, text="Clear", command=self.clear).pack(side="left", padx=6)

        ttk.Label(frame, text="Question or scenario").pack(anchor="w")
        self.question = tk.Text(frame, height=5, wrap="word", undo=True)
        self.question.pack(fill="x", pady=(4, 10))
        self.question.bind("<Control-Return>", lambda _event: self.ask())

        ttk.Label(frame, text="Answer").pack(anchor="w")
        self.answer = tk.Text(frame, wrap="word", undo=False)
        self.answer.pack(fill="both", expand=True, pady=(4, 0))
        self.answer.insert("1.0", "Ask a question to pull the closest local answer.")
        self.answer.configure(state="disabled")

    def _toggle_opacity(self) -> None:
        current = self.opacity.get()
        next_value = 0.45 if current > 0.6 else 0.88
        self.opacity.set(next_value)
        self.root.attributes("-alpha", next_value)

    def _apply_privacy_mode(self) -> None:
        enabled = self.capture_hidden.get()
        if apply_capture_exclusion(self.root, enabled):
            self.status.set("Hidden from screen capture" if enabled else "Capture visible")
        elif sys.platform == "win32":
            self.status.set("Capture hiding unavailable on this Windows session")
        else:
            self.status.set("Capture hiding is Windows-only")

    def clear(self) -> None:
        self.question.delete("1.0", "end")
        self._set_answer("Ask a question to pull the closest local answer.")

    def ask(self) -> None:
        question = self.question.get("1.0", "end").strip()
        if not question:
            return
        self._set_answer("Searching local library...")
        self.root.update_idletasks()
        payload = answer_payload(question, mode=self.mode.get(), limit=3, voice=self.voice.get())
        log_answer(payload)
        self._set_answer(self._format_payload(payload))

    def _set_answer(self, text: str) -> None:
        self.answer.configure(state="normal")
        self.answer.delete("1.0", "end")
        self.answer.insert("1.0", text)
        self.answer.configure(state="disabled")

    def _format_payload(self, payload: dict) -> str:
        if not payload["matches"]:
            return "No local answer found yet. Add this to the library."
        sections = []
        for match in payload["matches"]:
            sections.append(
                "\n".join(
                    [
                        f"[{match['confidence']} | {match['score']:.2f}] {match['topic']}",
                        f"Matched: {match['question']}",
                        "",
                        "Quick:",
                        match["versions"]["quick"],
                        "",
                        "Natural:",
                        match["versions"]["natural"],
                        "",
                        "Stored:",
                        match["versions"]["detailed"],
                        "",
                        "Keywords: " + ", ".join(match["keywords"][:8]),
                    ]
                )
            )
        return "\n\n---\n\n".join(sections)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    OverlayApp().run()


if __name__ == "__main__":
    main()
