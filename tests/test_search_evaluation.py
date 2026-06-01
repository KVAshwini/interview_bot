import pytest

from app.answer_engine import find_best_matches


SEARCH_CASES = [
    ("developer_python", "The Python API blocks the event loop when one downstream call is slow", "Python Developer"),
    ("developer_java", "A Spring Boot service is using too much heap after release", "Java Developer"),
    ("developer_sql", "The SQL report is doing a table scan and ignoring the index", "SQL Developer"),
    ("developer_fullstack", "React still shows stale data after the API update succeeds", "Full Stack Developer"),
    ("qa", "The automated UI suite fails randomly in CI but passes locally", "QA Engineer"),
    ("data_engineer", "The Airflow pipeline is late and downstream dashboards are stale", "Data Engineer"),
    ("data_analyst", "The dashboard KPI dropped suddenly and stakeholders need the reason", "Data Analyst"),
    ("business_analyst", "The stakeholder request is vague and needs testable acceptance criteria", "Business Analyst"),
    ("project_manager", "A cross-team dependency is slipping and threatens the critical path", "Project Manager"),
    ("product_manager", "How would you decide which roadmap item should be built first?", "Product Manager"),
    ("cybersecurity", "A suspicious email may have stolen credentials from users", "Cybersecurity Analyst"),
    ("cloud_engineer", "The cloud bill spiked and unused resources may be running", "Cloud Engineer"),
    ("database_admin", "The database has blocking sessions and user queries are timing out", "Database Administrator"),
]


@pytest.mark.parametrize(("category_filter", "query", "expected_topic"), SEARCH_CASES)
def test_profession_search_eval_cases(category_filter: str, query: str, expected_topic: str) -> None:
    match = find_best_matches(query, limit=1, category_filter=category_filter)[0]

    assert match.topic == expected_topic
