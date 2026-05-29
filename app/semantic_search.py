from app.text_utils import normalize, tokens


CONCEPTS = {
    "kubernetes": {
        "kubernetes", "k8s", "aks", "pod", "pods", "deployment", "deployments",
        "node", "nodes", "ingress", "service", "namespace", "kubectl",
    },
    "crashloop": {
        "crashloop", "crashloopbackoff", "restarting", "restart", "restarts",
        "crashing", "dying", "keeps dying", "keeps restarting", "oomkilled",
    },
    "terraform": {"terraform", "tf", "state", "tfstate", "plan", "apply", "drift", "lock", "import"},
    "cicd": {
        "ci/cd", "cicd", "pipeline", "pipelines", "deployment", "release",
        "rollback", "roll back", "build", "artifact", "runner",
    },
    "azure": {
        "azure", "app service", "key vault", "managed identity", "rbac",
        "service connection", "aks", "vnet", "nsg",
    },
    "linux": {
        "linux", "cpu", "memory", "disk", "inode", "process", "port",
        "systemctl", "journalctl", "swap", "load average",
    },
    "docker": {"docker", "container", "image", "dockerfile", "registry", "entrypoint", "layers"},
    "monitoring": {
        "monitor", "monitoring", "alert", "alerts", "prometheus", "grafana",
        "logs", "logging", "observability", "slo", "latency", "error rate",
    },
    "incident": {
        "incident", "outage", "p1", "production down", "sev1", "war room",
        "impact", "mitigation", "rca", "postmortem",
    },
    "kafka": {"kafka", "consumer lag", "lag", "broker", "partition", "offset", "producer", "consumer"},
    "security": {"security", "secure", "secret", "certificate", "ssl", "tls", "least privilege", "rbac"},
    "developer": {
        "developer", "software engineer", "backend", "frontend", "full stack", "api",
        "code", "coding", "debugging", "system design",
    },
    "qa": {"qa", "quality assurance", "testing", "test automation", "selenium", "pytest", "defect", "bug"},
    "data_engineer": {"data engineer", "etl", "elt", "pipeline", "spark", "airflow", "warehouse", "data lake"},
    "data_analyst": {"data analyst", "sql", "dashboard", "reporting", "power bi", "tableau", "analysis"},
    "business_analyst": {"business analyst", "requirements", "stakeholder", "user story", "brd", "process"},
    "project_manager": {"project manager", "delivery", "timeline", "risk", "scrum", "agile", "stakeholders"},
    "product_manager": {"product manager", "roadmap", "prioritization", "metrics", "customer", "backlog"},
    "cloud_engineer": {"cloud engineer", "cloud", "aws", "azure", "gcp", "networking", "iam"},
    "database_admin": {"database administrator", "dba", "backup", "restore", "replication", "sql server", "oracle"},
}


CATEGORY_HINTS = {
    "all": set(CONCEPTS),
    "devops": {"cicd", "incident", "monitoring"},
    "kubernetes": {"kubernetes", "crashloop", "monitoring"},
    "azure": {"azure", "kubernetes", "security", "monitoring"},
    "terraform": {"terraform", "azure", "cicd"},
    "linux": {"linux", "monitoring", "incident"},
    "scenario": {"incident", "crashloop", "kafka", "terraform", "monitoring"},
    "behavioral": {"incident"},
    "developer": {"developer"},
    "qa": {"qa"},
    "data_engineer": {"data_engineer"},
    "data_analyst": {"data_analyst"},
    "business_analyst": {"business_analyst"},
    "project_manager": {"project_manager"},
    "product_manager": {"product_manager"},
    "cybersecurity": {"security"},
    "cloud_engineer": {"cloud_engineer", "azure"},
    "database_admin": {"database_admin"},
}


def concept_hits(text: str) -> set[str]:
    normalized = normalize(text)
    token_set = set(tokens(text))
    hits = set()
    for concept, terms in CONCEPTS.items():
        for term in terms:
            if " " in term:
                if term in normalized:
                    hits.add(concept)
                    break
            elif term in token_set or term in normalized:
                hits.add(concept)
                break
    return hits


def semantic_score(query: str, candidate: str) -> float:
    query_hits = concept_hits(query)
    candidate_hits = concept_hits(candidate)
    if not query_hits or not candidate_hits:
        return 0.0
    overlap = len(query_hits & candidate_hits)
    return round(overlap / len(query_hits | candidate_hits), 4)


def category_boost(category_filter: str, candidate: str) -> float:
    hints = CATEGORY_HINTS.get(category_filter, set())
    if not hints:
        return 0.0
    hits = concept_hits(candidate)
    return 0.04 if hits & hints else 0.0
