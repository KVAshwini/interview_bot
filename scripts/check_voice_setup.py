import importlib.util


PACKAGES = {
    "faster_whisper": "Faster-Whisper speech-to-text",
    "sounddevice": "microphone recording",
    "soundfile": "wav file writing",
}


def main() -> None:
    missing = []
    for module, purpose in PACKAGES.items():
        if importlib.util.find_spec(module) is None:
            missing.append((module, purpose))

    if missing:
        print("Voice setup is incomplete.")
        for module, purpose in missing:
            print(f"- missing {module}: {purpose}")
        raise SystemExit(1)

    print("Voice setup looks good.")
    for module, purpose in PACKAGES.items():
        print(f"- {module}: {purpose}")


if __name__ == "__main__":
    main()
