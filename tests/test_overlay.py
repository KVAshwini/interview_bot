import sys

from app import overlay


class FakeUser32:
    def __init__(self, results: list[int]) -> None:
        self.results = results
        self.calls: list[tuple[int, int]] = []

    def SetWindowDisplayAffinity(self, hwnd: int, affinity: int) -> int:
        self.calls.append((hwnd, affinity))
        return self.results.pop(0)


def test_capture_exclusion_uses_exclude_from_capture() -> None:
    user32 = FakeUser32([1])

    assert overlay.set_window_capture_exclusion(123, True, user32)
    assert user32.calls == [(123, overlay.WDA_EXCLUDEFROMCAPTURE)]


def test_capture_exclusion_falls_back_to_monitor_affinity() -> None:
    user32 = FakeUser32([0, 1])

    assert overlay.set_window_capture_exclusion(456, True, user32)
    assert user32.calls == [
        (456, overlay.WDA_EXCLUDEFROMCAPTURE),
        (456, overlay.WDA_MONITOR),
    ]


def test_capture_exclusion_disable_uses_none_without_fallback() -> None:
    user32 = FakeUser32([1])

    assert overlay.set_window_capture_exclusion(789, False, user32)
    assert user32.calls == [(789, overlay.WDA_NONE)]


def test_apply_capture_exclusion_is_windows_only(monkeypatch) -> None:
    class Root:
        def winfo_id(self) -> int:
            return 123

    monkeypatch.setattr(sys, "platform", "linux")

    assert not overlay.apply_capture_exclusion(Root(), True)
