from app.answer_engine import find_best_matches
from app.professions import ALLOWED_FILTERS, profession_options
from app.library_loader import load_library


def test_profession_filters_are_registered() -> None:
    keys = {item["key"] for item in profession_options()}
    assert {
        "developer",
        "developer_python",
        "developer_java",
        "developer_sql",
        "developer_fullstack",
        "qa",
        "data_engineer",
        "business_analyst",
    } <= keys
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


def test_python_developer_filter_matches_python_pack() -> None:
    match = find_best_matches("When would you use asyncio in Python?", limit=1, category_filter="developer_python")[0]
    assert match.topic == "Python Developer"


def test_java_developer_filter_matches_java_pack() -> None:
    match = find_best_matches("How do transactions work in Spring?", limit=1, category_filter="developer_java")[0]
    assert match.topic == "Java Developer"


def test_sql_developer_filter_matches_sql_pack() -> None:
    match = find_best_matches("How do you optimize a slow SQL query?", limit=1, category_filter="developer_sql")[0]
    assert match.topic == "SQL Developer"


def test_fullstack_developer_filter_matches_fullstack_pack() -> None:
    match = find_best_matches("How do you manage state in a React application?", limit=1, category_filter="developer_fullstack")[0]
    assert match.topic == "Full Stack Developer"


def test_developer_specialization_pack_counts() -> None:
    counts = {}
    for item in load_library():
        topic = item["topic"]
        counts[topic] = counts.get(topic, 0) + 1

    assert counts["Software Developer - General"] >= 50
    assert counts["Python Developer"] >= 50
    assert counts["Java Developer"] >= 50
    assert counts["SQL Developer"] >= 50
    assert counts["Full Stack Developer"] >= 50
