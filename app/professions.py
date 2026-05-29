from dataclasses import dataclass


@dataclass(frozen=True)
class Profession:
    key: str
    label: str
    aliases: tuple[str, ...]


PROFESSIONS = [
    Profession("devops", "DevOps / SRE", ("devops", "sre", "production support", "ci/cd")),
    Profession("developer", "Software Developer", ("developer", "software engineer", "backend", "frontend", "full stack")),
    Profession("qa", "QA / Test Engineer", ("qa", "test engineer", "automation testing", "quality assurance")),
    Profession("data_engineer", "Data Engineer", ("data engineer", "etl", "data pipeline", "spark")),
    Profession("data_analyst", "Data Analyst", ("data analyst", "sql analyst", "dashboard", "reporting")),
    Profession("business_analyst", "Business Analyst", ("business analyst", "requirements", "stakeholders", "user stories")),
    Profession("project_manager", "Project Manager", ("project manager", "delivery manager", "scrum", "risk management")),
    Profession("product_manager", "Product Manager", ("product manager", "roadmap", "prioritization", "product strategy")),
    Profession("cybersecurity", "Cybersecurity Analyst", ("cybersecurity", "security analyst", "siem", "vulnerability")),
    Profession("cloud_engineer", "Cloud Engineer", ("cloud engineer", "aws", "azure", "gcp", "cloud infrastructure")),
    Profession("database_admin", "Database Administrator", ("database administrator", "dba", "sql server", "oracle", "backup")),
]


BASE_FILTERS = {"all", "kubernetes", "azure", "terraform", "linux", "scenario", "behavioral"}
PROFESSION_FILTERS = {profession.key for profession in PROFESSIONS}
ALLOWED_FILTERS = BASE_FILTERS | PROFESSION_FILTERS


def profession_options() -> list[dict[str, str]]:
    return [{"key": profession.key, "label": profession.label} for profession in PROFESSIONS]


def aliases_for(filter_key: str) -> tuple[str, ...]:
    for profession in PROFESSIONS:
        if profession.key == filter_key:
            return profession.aliases
    return ()
