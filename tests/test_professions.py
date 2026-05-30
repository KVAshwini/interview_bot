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


def test_qa_filter_matches_deep_qa_pack() -> None:
    match = find_best_matches("How do you handle flaky automated tests?", limit=1, category_filter="qa")[0]
    assert match.category == "profession"
    assert match.topic == "QA Engineer"


def test_qa_api_testing_matches_qa_engineer() -> None:
    match = find_best_matches("What do you validate in API testing?", limit=1, category_filter="qa")[0]
    assert match.topic == "QA Engineer"
    assert "API" in match.question or "API" in match.instant_answer
