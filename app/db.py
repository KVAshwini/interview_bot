import json
import sqlite3
from pathlib import Path
from typing import Any

from app.config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS qa_items (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    topic TEXT NOT NULL,
    question TEXT NOT NULL,
    alternate_questions TEXT NOT NULL,
    instant_answer TEXT NOT NULL,
    detailed_answer TEXT NOT NULL,
    keywords TEXT NOT NULL,
    difficulty TEXT,
    answer_style TEXT,
    source_file TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    searchable_text TEXT NOT NULL
);
"""


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def item_text(item: dict[str, Any]) -> str:
    fields = [
        item.get("question", ""),
        item.get("scenario", ""),
        " ".join(item.get("alternate_questions", [])),
        " ".join(item.get("alternate_scenarios", [])),
        item.get("topic", ""),
        " ".join(item.get("keywords", [])),
    ]
    return " ".join(str(field) for field in fields if field)


def upsert_items(conn: sqlite3.Connection, items: list[dict[str, Any]]) -> None:
    sql = """
    INSERT INTO qa_items (
        id, category, topic, question, alternate_questions, instant_answer,
        detailed_answer, keywords, difficulty, answer_style, source_file,
        raw_json, searchable_text
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        category=excluded.category,
        topic=excluded.topic,
        question=excluded.question,
        alternate_questions=excluded.alternate_questions,
        instant_answer=excluded.instant_answer,
        detailed_answer=excluded.detailed_answer,
        keywords=excluded.keywords,
        difficulty=excluded.difficulty,
        answer_style=excluded.answer_style,
        source_file=excluded.source_file,
        raw_json=excluded.raw_json,
        searchable_text=excluded.searchable_text
    """
    for item in items:
        question = item.get("question") or item.get("scenario", "")
        alternates = item.get("alternate_questions") or item.get("alternate_scenarios") or []
        detailed = item.get("detailed_answer")
        if isinstance(detailed, dict):
            detailed = "\n".join(f"{key}: {value}" for key, value in detailed.items())
        if not detailed:
            structured = item.get("structured_answer", {})
            if isinstance(structured, dict):
                detailed = "\n".join(f"{key}: {value}" for key, value in structured.items())
            else:
                detailed = item.get("instant_answer", "")

        conn.execute(
            sql,
            (
                item["id"],
                item.get("category", "general"),
                item.get("topic", "General"),
                question,
                json.dumps(alternates),
                item.get("instant_answer", ""),
                detailed,
                json.dumps(item.get("keywords", [])),
                item.get("difficulty"),
                item.get("answer_style"),
                item.get("source_file", "unknown"),
                json.dumps(item, indent=2),
                item_text(item),
            ),
        )
    conn.commit()


def all_items(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(conn.execute("SELECT * FROM qa_items ORDER BY category, topic, id"))
