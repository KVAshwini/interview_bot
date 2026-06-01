import json

from app.pack_manager import build_pack_manifest


def test_pack_manifest_describes_content_packs() -> None:
    manifest = build_pack_manifest()

    assert manifest["pack_count"] > 0
    assert manifest["total_items"] >= 1800
    assert all(pack["content_only"] for pack in manifest["packs"])
    assert all(pack["sha256"] for pack in manifest["packs"])


def test_pack_manifest_excludes_itself(tmp_path) -> None:
    pack = tmp_path / "sample.json"
    pack.write_text(
        json.dumps(
            [
                {
                    "id": "sample_001",
                    "category": "profession",
                    "topic": "Sample",
                    "question": "Question?",
                    "alternate_questions": [],
                    "instant_answer": "Answer.",
                    "detailed_answer": "Detailed.",
                    "keywords": [],
                }
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "pack_manifest.json").write_text("{}", encoding="utf-8")

    manifest = build_pack_manifest(tmp_path)

    assert manifest["pack_count"] == 1
    assert manifest["packs"][0]["path"].endswith("sample.json")
