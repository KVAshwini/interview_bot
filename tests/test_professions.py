from app.answer_engine import find_best_matches
from app.professions import ALLOWED_FILTERS, profession_options


def test_profession_filters_are_registered() -> None:
    keys = {item["key"] for item in profession_options()}
    assert {"developer", "qa", "data_engineer", "business_analyst"} <= keys
    assert keys <= ALLOWED_FILTERS


def test_developer_filter_matches_developer_pack() -> None:
    match = find_best_matches("How do you debug a production API issue?", limit=1, category_filter="developer")[0]
    assert match.category == "profession"
    assert "Developer" in match.topic
