import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "qa_library" / "professions"


ROLE_CONTEXT = {
    "qa_engineer": "quality risk, reproducibility, test coverage, automation stability, release confidence, and defect prevention",
    "data_engineer": "data correctness, schema contracts, pipeline reliability, freshness, lineage, backfills, and downstream impact",
    "data_analyst": "business definitions, SQL correctness, metric trust, stakeholder decisions, dashboard quality, and data validation",
    "business_analyst": "business process, requirements clarity, stakeholder alignment, acceptance criteria, traceability, and change impact",
    "project_manager": "delivery risk, dependencies, scope, timeline, communication, ownership, and escalation",
    "product_manager": "customer value, product outcomes, prioritization, discovery evidence, roadmap tradeoffs, and measurable impact",
    "cybersecurity": "threat context, evidence preservation, containment, least privilege, detection, auditability, and risk reduction",
    "cloud_engineer": "secure cloud architecture, reliability, networking, IAM, cost, automation, monitoring, and operational readiness",
    "database_admin": "availability, backup and restore, query performance, locking, capacity, recovery, and data integrity",
}


def make_item(pack: str, idx: int, topic: str, area: str, question: str, alternates: list[str], keywords: list[str], difficulty: str = "high") -> dict:
    context = ROLE_CONTEXT[pack]
    instant = (
        f"For {area}, I first clarify the goal, the people or systems affected, the current evidence, and the decision that depends on it. "
        f"Then I focus on the risks around {context}. A strong answer should include what I would do immediately, how I would validate it, and how I would prevent the same issue from repeating."
    )
    detailed = (
        f"For {area}, I would begin by confirming the objective, stakeholders, affected workflow or system, constraints, and success criteria. "
        f"Then I review the relevant artifacts, data, logs, process steps, ownership, dependencies, and recent changes so I can distinguish symptoms from root cause. "
        f"If there is active business or production impact, I reduce that impact first and keep communication clear. After the immediate issue is under control, I validate the outcome with evidence and close the loop through documentation, automation, monitoring, controls, or process improvement. "
        f"In this area, the depth comes from covering {context} with concrete examples rather than giving a generic process answer."
    )
    return {
        "id": f"profession_{pack}_deep_{idx:03d}",
        "category": "profession",
        "topic": topic,
        "question": question,
        "alternate_questions": alternates,
        "instant_answer": instant,
        "detailed_answer": detailed,
        "keywords": keywords,
        "answer_style": "profession_interview_practical",
        "difficulty": difficulty,
    }


QA = [
    ("risk-based testing", "How do you apply risk-based testing?", ["How do you decide what to test first?", "How do you test when time is limited?"], ["qa engineer", "risk based testing", "priority", "coverage"]),
    ("automation strategy", "How do you decide which tests to automate?", ["What should not be automated?", "How do you choose automation candidates?"], ["qa engineer", "automation strategy", "regression", "coverage"]),
    ("shift-left QA", "What does shift-left testing mean?", ["How can QA get involved earlier?", "How do you prevent defects before coding finishes?"], ["qa engineer", "shift left", "requirements", "prevention"]),
    ("acceptance criteria", "How do you review acceptance criteria?", ["What makes acceptance criteria testable?", "How do you find gaps in user stories?"], ["qa engineer", "acceptance criteria", "requirements", "user story"]),
    ("negative testing", "How do you design negative test cases?", ["How do you test invalid input?", "Why is negative testing important?"], ["qa engineer", "negative testing", "validation", "edge cases"]),
    ("boundary testing", "Explain boundary value testing.", ["How do you test limits?", "What boundary cases do you include?"], ["qa engineer", "boundary testing", "limits", "test design"]),
    ("equivalence partitioning", "What is equivalence partitioning?", ["How do you reduce test cases without losing coverage?", "How do you group similar inputs?"], ["qa engineer", "equivalence partitioning", "test design", "coverage"]),
    ("traceability", "How do you maintain requirements traceability?", ["How do you map tests to requirements?", "How do you prove coverage?"], ["qa engineer", "traceability", "requirements", "coverage"]),
    ("test environment", "How do you handle unstable test environments?", ["Environment is down during testing. What do you do?", "How do you reduce environment-related test failures?"], ["qa engineer", "test environment", "stability", "triage"]),
    ("api auth testing", "How do you test API authentication and authorization?", ["How do you test secured APIs?", "What permission cases do you test in APIs?"], ["qa engineer", "api testing", "authentication", "authorization"]),
    ("contract testing", "How does QA use contract testing?", ["How do you prevent API integration breaks?", "What is consumer-driven contract testing?"], ["qa engineer", "contract testing", "api", "integration"]),
    ("database testing", "How do you validate database changes as QA?", ["What database checks do you perform?", "How do you test data persistence?"], ["qa engineer", "database testing", "sql", "data validation"]),
    ("accessibility testing", "How do you test accessibility?", ["What accessibility checks should QA perform?", "How do you test keyboard and screen reader behavior?"], ["qa engineer", "accessibility", "wcag", "keyboard"]),
    ("cross-browser testing", "How do you plan cross-browser testing?", ["Which browsers do you test?", "How do you reduce browser compatibility risk?"], ["qa engineer", "cross browser", "compatibility", "web testing"]),
    ("release rollback validation", "How do you validate rollback readiness?", ["How does QA test rollback plans?", "What do you check before production release?"], ["qa engineer", "rollback", "release", "validation"]),
    ("test metrics", "What QA metrics are actually useful?", ["How do you measure quality?", "Which test metrics can be misleading?"], ["qa engineer", "metrics", "defects", "quality"]),
    ("automation reporting", "What should automation reports show?", ["How do you make test results useful?", "How do you debug failed automation from reports?"], ["qa engineer", "automation reporting", "ci", "logs"]),
    ("parallel automation", "How do you run automation in parallel safely?", ["What issues happen with parallel tests?", "How do you avoid test data conflicts in parallel runs?"], ["qa engineer", "parallel testing", "automation", "test data"]),
    ("uat support", "How does QA support UAT?", ["What is QA's role in user acceptance testing?", "How do you handle UAT defects?"], ["qa engineer", "uat", "stakeholders", "defects"]),
    ("production monitoring", "How can QA help after release?", ["What does QA monitor post-release?", "How do you validate production after deployment?"], ["qa engineer", "post release", "monitoring", "smoke testing"]),
    ("root cause analysis", "How do you perform defect root cause analysis?", ["How do you prevent repeated defects?", "What do you check after a bug escapes?"], ["qa engineer", "root cause", "escaped defect", "prevention"]),
    ("test coverage gaps", "How do you find gaps in test coverage?", ["How do you know what tests are missing?", "How do defects reveal coverage gaps?"], ["qa engineer", "coverage", "gap analysis", "regression"]),
    ("automation maintenance", "How do you maintain a large automation suite?", ["How do you keep tests from becoming outdated?", "How do you handle old automation scripts?"], ["qa engineer", "automation maintenance", "suite", "stability"]),
    ("quality ownership", "How do you promote quality ownership across a team?", ["Is quality only QA's responsibility?", "How do developers and QA share quality?"], ["qa engineer", "quality ownership", "collaboration", "team"]),
]


DATA_ENGINEER = [
    ("data contracts", "How do you use data contracts?", ["How do you prevent upstream schema changes from breaking pipelines?", "What belongs in a data contract?"], ["data engineer", "data contract", "schema", "pipeline"]),
    ("pipeline orchestration", "How do you orchestrate data pipelines?", ["How do tools like Airflow help?", "How do you manage pipeline dependencies?"], ["data engineer", "airflow", "orchestration", "dependencies"]),
    ("backfills", "How do you run a safe data backfill?", ["How do you reprocess historical data?", "What can go wrong during a backfill?"], ["data engineer", "backfill", "historical data", "idempotency"]),
    ("late arriving data", "How do you handle late-arriving data?", ["What if events arrive after the window closes?", "How do pipelines handle delayed records?"], ["data engineer", "late data", "watermark", "events"]),
    ("cdc", "How does change data capture work?", ["When do you use CDC?", "How do you process database changes in pipelines?"], ["data engineer", "cdc", "change data capture", "replication"]),
    ("streaming vs batch", "When do you choose streaming over batch?", ["Batch vs streaming pipelines?", "What are streaming tradeoffs?"], ["data engineer", "streaming", "batch", "latency"]),
    ("spark tuning", "How do you tune a slow Spark job?", ["Spark job is slow. What do you check?", "How do partitions affect Spark performance?"], ["data engineer", "spark", "partitions", "performance"]),
    ("small files", "How do you handle small-file problems in data lakes?", ["Why are many small files bad?", "How do you optimize data lake file layout?"], ["data engineer", "data lake", "small files", "compaction"]),
    ("partition strategy", "How do you design partitioning for data lakes?", ["Which columns should partition data?", "What are partitioning pitfalls?"], ["data engineer", "partitioning", "data lake", "performance"]),
    ("data lineage", "How do you track data lineage?", ["How do you know where data came from?", "Why is lineage important?"], ["data engineer", "lineage", "metadata", "governance"]),
    ("freshness checks", "How do you monitor data freshness?", ["How do you know data is late?", "What freshness alerts do you create?"], ["data engineer", "freshness", "monitoring", "sla"]),
    ("volume anomalies", "How do you detect abnormal data volume?", ["How do you catch missing or duplicate loads?", "What volume checks do you add?"], ["data engineer", "volume checks", "anomaly", "data quality"]),
    ("schema evolution", "How do you support schema evolution?", ["How do you add columns safely?", "How do you handle changing event schemas?"], ["data engineer", "schema evolution", "compatibility", "events"]),
    ("warehouse modeling", "How do you model data for a warehouse?", ["Fact vs dimension tables?", "How do you design analytics tables?"], ["data engineer", "warehouse", "fact table", "dimension"]),
    ("slow warehouse query", "How do you troubleshoot slow warehouse queries?", ["BigQuery or Snowflake query is slow. What do you check?", "How do you optimize analytical SQL?"], ["data engineer", "warehouse", "query optimization", "sql"]),
    ("data lakehouse", "What is a lakehouse architecture?", ["How does a lakehouse differ from a warehouse?", "When use Delta or Iceberg?"], ["data engineer", "lakehouse", "delta", "iceberg"]),
    ("deduplication", "How do you deduplicate events?", ["How do you handle duplicate messages?", "What keys do you use for deduplication?"], ["data engineer", "deduplication", "events", "idempotency"]),
    ("exactly once", "What does exactly-once processing mean?", ["Is exactly-once really possible?", "How do you avoid duplicate processing?"], ["data engineer", "exactly once", "streaming", "idempotency"]),
    ("data reconciliation", "How do you reconcile source and target data?", ["How do you prove a pipeline loaded correctly?", "What checks compare source and warehouse?"], ["data engineer", "reconciliation", "source target", "validation"]),
    ("pipeline retries", "How do you design retries in pipelines?", ["When should a data job retry?", "How do you avoid corrupting data on rerun?"], ["data engineer", "retry", "idempotency", "pipeline"]),
    ("secrets", "How do you manage secrets in data pipelines?", ["How do jobs access credentials safely?", "How do you avoid hardcoded data credentials?"], ["data engineer", "secrets", "credentials", "security"]),
    ("pii handling", "How do you handle PII in data platforms?", ["How do you mask sensitive data?", "How do data engineers protect privacy?"], ["data engineer", "pii", "masking", "privacy"]),
    ("cost optimization", "How do you control data platform cost?", ["Data warehouse bill increased. What do you check?", "How do you reduce Spark or warehouse spend?"], ["data engineer", "cost", "warehouse", "optimization"]),
    ("sla", "How do you define data pipeline SLAs?", ["How do you set pipeline reliability targets?", "What does data availability mean?"], ["data engineer", "sla", "reliability", "freshness"]),
    ("incident response", "A critical data pipeline failed before business reporting. What do you do?", ["ETL failed before executive dashboard refresh. How do you respond?", "How do you handle a data incident?"], ["data engineer", "incident", "pipeline failure", "reporting"]),
    ("data tests", "What automated tests do you add for pipelines?", ["How do you test transformations?", "How do dbt tests or pipeline tests help?"], ["data engineer", "testing", "dbt", "transformations"]),
    ("slow ingestion", "How do you troubleshoot slow data ingestion?", ["Ingestion lag is increasing. What do you check?", "How do you improve pipeline throughput?"], ["data engineer", "ingestion", "throughput", "lag"]),
    ("event ordering", "How do you handle out-of-order events?", ["Events arrive in wrong order. What do you do?", "How do stream processors handle ordering?"], ["data engineer", "event ordering", "streaming", "watermark"]),
    ("data catalog", "Why use a data catalog?", ["How do users discover trusted datasets?", "What metadata should data catalogs store?"], ["data engineer", "data catalog", "metadata", "governance"]),
    ("ownership", "How do you define data ownership?", ["Who owns a dataset?", "How do you handle unclear data ownership?"], ["data engineer", "ownership", "governance", "data product"]),
    ("environment promotion", "How do you promote pipeline changes safely?", ["How do dev, test, and prod data environments work?", "How do you release data pipeline changes?"], ["data engineer", "deployment", "environments", "release"]),
    ("null handling", "How do you handle unexpected nulls in pipelines?", ["Source sent nulls. What do you check?", "How do you validate required fields?"], ["data engineer", "nulls", "validation", "schema"]),
    ("corrupt records", "How do you handle corrupt records?", ["What do you do with bad input files?", "How do you quarantine invalid data?"], ["data engineer", "corrupt records", "quarantine", "data quality"]),
    ("data retention", "How do you implement data retention?", ["How do you expire old data?", "How do retention policies affect pipelines?"], ["data engineer", "retention", "lifecycle", "compliance"]),
    ("api ingestion", "How do you ingest data from APIs reliably?", ["How do you handle API rate limits in data pipelines?", "How do you backfill API data?"], ["data engineer", "api ingestion", "rate limits", "backfill"]),
    ("file formats", "How do you choose between Parquet, Avro, JSON, and CSV?", ["Which data file format do you use?", "How do file formats affect performance?"], ["data engineer", "parquet", "avro", "json", "csv"]),
    ("compaction", "What is compaction in data lakes?", ["How do you optimize data lake files?", "Why compact small files?"], ["data engineer", "compaction", "data lake", "performance"]),
    ("pipeline observability", "What metrics do you monitor for pipelines?", ["How do you monitor data jobs?", "What alerts should data pipelines have?"], ["data engineer", "observability", "metrics", "alerts"]),
    ("data drift", "How do you detect data drift?", ["What if input distribution changes?", "How do you monitor unexpected data pattern changes?"], ["data engineer", "data drift", "anomaly", "monitoring"]),
    ("incremental models", "How do incremental models work?", ["How do dbt incremental models avoid full rebuilds?", "What are incremental model risks?"], ["data engineer", "incremental models", "dbt", "warehouse"]),
    ("blue green data", "How do you release data model changes safely?", ["How do you avoid breaking dashboards?", "How do you version data models?"], ["data engineer", "data model", "release", "compatibility"]),
    ("access control", "How do you manage access to datasets?", ["How do you enforce least privilege in data platforms?", "How do row-level permissions work?"], ["data engineer", "access control", "permissions", "security"]),
    ("quality framework", "How do you build a data quality framework?", ["How do you standardize validation across pipelines?", "What reusable checks do you create?"], ["data engineer", "data quality framework", "validation", "automation"]),
    ("root cause", "How do you investigate bad data in a dashboard?", ["Dashboard numbers are wrong. How do you find the cause?", "How do you trace bad analytics data?"], ["data engineer", "root cause", "dashboard", "lineage"]),
    ("capacity planning", "How do you plan capacity for data systems?", ["How do you predict storage and compute growth?", "How do you scale data platforms?"], ["data engineer", "capacity", "scaling", "storage"]),
    ("documentation", "What documentation should data pipelines have?", ["How do you document datasets?", "What should a data runbook include?"], ["data engineer", "documentation", "runbook", "metadata"]),
]


DATA_ANALYST = [
    ("requirements", "How do you gather analytics requirements?", ["How do you understand what stakeholders need?", "How do you define a reporting request?"], ["data analyst", "requirements", "stakeholders", "reporting"]),
    ("metric governance", "How do you prevent multiple definitions of the same metric?", ["How do you create a single source of truth?", "How do you handle KPI disagreement?"], ["data analyst", "metrics", "governance", "kpi"]),
    ("dashboard design", "How do you design an executive dashboard?", ["What makes a dashboard useful?", "How do you choose dashboard visuals?"], ["data analyst", "dashboard", "visualization", "executive"]),
    ("sql joins", "How do you avoid double counting in SQL analysis?", ["Why do joins inflate numbers?", "How do you validate join grain?"], ["data analyst", "sql", "joins", "double counting"]),
    ("cohort analysis", "How do you perform cohort analysis?", ["What is cohort retention?", "How do you analyze users over time?"], ["data analyst", "cohort", "retention", "analysis"]),
    ("funnel analysis", "How do you analyze a conversion funnel?", ["How do you find funnel drop-off?", "What does funnel analysis show?"], ["data analyst", "funnel", "conversion", "drop off"]),
    ("ab testing", "How do you analyze an A/B test?", ["How do you know if an experiment is significant?", "What can go wrong with A/B tests?"], ["data analyst", "ab test", "experiment", "significance"]),
    ("outliers", "How do you handle outliers?", ["Do you remove outliers?", "How do outliers affect analysis?"], ["data analyst", "outliers", "statistics", "analysis"]),
    ("missing data", "How do you handle missing data?", ["What do nulls mean in analysis?", "How do you explain missing values?"], ["data analyst", "missing data", "nulls", "quality"]),
    ("data validation", "How do you validate a dashboard before publishing?", ["How do you know report numbers are correct?", "What checks do you run before sharing analysis?"], ["data analyst", "validation", "dashboard", "qa"]),
    ("storytelling", "How do you present data insights?", ["How do you tell a story with data?", "How do you make analysis actionable?"], ["data analyst", "storytelling", "insights", "presentation"]),
    ("root cause analysis", "A KPI dropped suddenly. How do you investigate?", ["Metric changed unexpectedly. What do you check?", "How do you find why a dashboard number moved?"], ["data analyst", "root cause", "kpi", "trend"]),
    ("segmentation", "How do you segment customers or users?", ["How do you compare groups in analysis?", "What makes a useful segment?"], ["data analyst", "segmentation", "customers", "analysis"]),
    ("forecasting", "How do you approach forecasting?", ["How do you forecast demand or revenue?", "What assumptions matter in forecasts?"], ["data analyst", "forecasting", "trend", "seasonality"]),
    ("seasonality", "How do you account for seasonality?", ["How do seasonal patterns affect metrics?", "How do you compare periods fairly?"], ["data analyst", "seasonality", "time series", "comparison"]),
    ("data refresh", "How do you handle stale dashboard data?", ["Dashboard did not refresh. What do you do?", "How do you communicate data freshness?"], ["data analyst", "freshness", "dashboard", "refresh"]),
    ("self service", "How do you support self-service analytics?", ["How do you help business users use data?", "What makes a dataset self-service friendly?"], ["data analyst", "self service", "analytics", "documentation"]),
    ("visualization choice", "How do you choose the right chart?", ["Bar chart vs line chart?", "How do you avoid misleading visuals?"], ["data analyst", "visualization", "charts", "dashboard"]),
    ("data cleaning", "How do you clean messy data?", ["What data cleaning steps do you take?", "How do you handle inconsistent source data?"], ["data analyst", "data cleaning", "quality", "standardization"]),
    ("excel vs sql", "When do you use Excel, SQL, or BI tools?", ["How do you choose analysis tools?", "What belongs in SQL vs dashboard layer?"], ["data analyst", "excel", "sql", "bi"]),
    ("stakeholder conflict", "How do you handle stakeholders disagreeing with your numbers?", ["What if business users say your report is wrong?", "How do you resolve data disputes?"], ["data analyst", "stakeholders", "metric dispute", "validation"]),
    ("privacy", "How do you handle sensitive data in analysis?", ["How do analysts protect PII?", "What data should not be exposed in dashboards?"], ["data analyst", "privacy", "pii", "security"]),
    ("sampling", "When would you use sampling?", ["How can sampling bias analysis?", "What are risks of sampled data?"], ["data analyst", "sampling", "bias", "statistics"]),
    ("correlation causation", "How do you explain correlation vs causation?", ["Why does correlation not prove causation?", "How do you avoid false conclusions?"], ["data analyst", "correlation", "causation", "statistics"]),
    ("data model", "How do you understand a new data model?", ["How do you learn unfamiliar tables?", "How do you find the right data source?"], ["data analyst", "data model", "tables", "lineage"]),
    ("sql windows", "How do you use SQL window functions in analysis?", ["When do you use row_number or lag?", "How do window functions help reporting?"], ["data analyst", "sql", "window functions", "analysis"]),
    ("time zones", "How do time zones affect reporting?", ["Why do dashboard dates differ?", "How do you handle UTC vs local dates?"], ["data analyst", "timezone", "dates", "reporting"]),
    ("granularity", "Why does data grain matter?", ["What is the grain of a table?", "How does grain affect analysis?"], ["data analyst", "grain", "granularity", "sql"]),
    ("performance", "How do you optimize slow dashboards?", ["Dashboard loads slowly. What do you check?", "How do extracts or aggregates improve BI performance?"], ["data analyst", "dashboard performance", "bi", "optimization"]),
    ("documentation", "How do you document metrics and dashboards?", ["What belongs in a data dictionary?", "How do users know what a report means?"], ["data analyst", "documentation", "data dictionary", "metrics"]),
    ("ad hoc analysis", "How do you handle urgent ad hoc analysis?", ["How do you balance speed and accuracy?", "What do you communicate with quick analysis?"], ["data analyst", "ad hoc", "accuracy", "stakeholders"]),
    ("quality issue", "You find data quality issues during analysis. What do you do?", ["How do you report bad data?", "What if source data is unreliable?"], ["data analyst", "data quality", "issue", "source"]),
    ("kpi tree", "How do you break down a high-level KPI?", ["How do you find metric drivers?", "How do KPI trees help analysis?"], ["data analyst", "kpi tree", "drivers", "metrics"]),
    ("retention", "How do you analyze retention?", ["How do you calculate churn?", "What retention metrics do you use?"], ["data analyst", "retention", "churn", "cohort"]),
    ("revenue analysis", "How do you analyze revenue changes?", ["Revenue dropped. What do you check?", "How do price, volume, and mix affect revenue?"], ["data analyst", "revenue", "variance", "business"]),
    ("operational reporting", "How do you design operational reports?", ["What makes an operational dashboard different?", "How do teams use daily reports?"], ["data analyst", "operations", "reporting", "dashboard"]),
    ("data extracts", "How do you validate data extracts?", ["How do you ensure CSV exports are correct?", "What checks do you perform before sending data?"], ["data analyst", "extracts", "validation", "csv"]),
    ("bias", "How do you identify bias in analysis?", ["How can data selection bias results?", "How do you avoid misleading analysis?"], ["data analyst", "bias", "analysis", "sampling"]),
    ("confidence", "How do you communicate uncertainty?", ["How do you explain confidence intervals?", "How do you show limitations in analysis?"], ["data analyst", "uncertainty", "confidence", "statistics"]),
    ("requirements change", "What do you do when reporting requirements change?", ["How do you handle dashboard scope changes?", "How do you update metrics safely?"], ["data analyst", "requirements", "change", "dashboard"]),
    ("bi governance", "How do you prevent dashboard sprawl?", ["How do you manage many reports?", "How do you retire unused dashboards?"], ["data analyst", "bi governance", "dashboards", "ownership"]),
    ("sql debugging", "How do you debug a wrong SQL result?", ["SQL query returns unexpected numbers. What do you check?", "How do you test SQL step by step?"], ["data analyst", "sql debugging", "validation", "joins"]),
    ("automation", "What reporting tasks would you automate?", ["How do you reduce manual reporting?", "When should a report become automated?"], ["data analyst", "automation", "reporting", "efficiency"]),
    ("business impact", "How do you connect analysis to business impact?", ["How do you make recommendations from data?", "How do you avoid just reporting numbers?"], ["data analyst", "business impact", "recommendations", "insights"]),
    ("dashboard adoption", "How do you measure dashboard adoption?", ["How do you know if a dashboard is being used?", "What do you do with low dashboard usage?"], ["data analyst", "dashboard adoption", "usage", "stakeholders"]),
    ("data storytelling risk", "How do you avoid misleading stakeholders with data?", ["How do you present limitations clearly?", "How do you prevent incorrect interpretation of charts?"], ["data analyst", "storytelling", "risk", "communication"]),
]


BUSINESS_ANALYST_AREAS = [
    "stakeholder interviews", "current-state process mapping", "future-state process design", "user story writing",
    "acceptance criteria", "business rules", "non-functional requirements", "requirements prioritization",
    "scope management", "impact analysis", "gap analysis", "process improvement", "workflow exceptions",
    "data requirements", "reporting requirements", "integration requirements", "API requirements",
    "UAT planning", "UAT defect triage", "requirements traceability", "change requests", "regulatory requirements",
    "risk and assumptions", "dependency mapping", "system context diagrams", "wireframes and prototypes",
    "use cases", "user journeys", "backlog refinement", "sprint planning support", "definition of ready",
    "definition of done", "stakeholder conflict", "requirements sign-off", "vendor requirements",
    "migration requirements", "cutover planning", "training and adoption", "operational readiness",
    "root cause analysis", "KPI definition", "decision logs", "RACI ownership", "Agile ceremonies",
    "documentation quality", "production support handoff",
]


PROJECT_MANAGER_AREAS = [
    "project charter", "scope baseline", "schedule planning", "critical path", "risk register",
    "issue management", "dependency tracking", "stakeholder communication", "status reporting",
    "budget tracking", "resource planning", "vendor coordination", "change control", "scope creep",
    "delivery roadmap", "milestone planning", "go-live readiness", "cutover planning", "rollback planning",
    "project governance", "steering committee updates", "escalation management", "team velocity",
    "Agile project delivery", "Scrum ceremonies", "hybrid delivery", "waterfall delivery", "RAID logs",
    "quality gates", "release coordination", "cross-functional alignment", "blocked work", "timeline slippage",
    "executive reporting", "post-implementation review", "lessons learned", "capacity planning",
    "dependency delays", "project recovery", "priority conflicts", "communication plans", "decision tracking",
    "compliance projects", "security project delivery", "data migration projects", "production incident projects",
]


PRODUCT_MANAGER_AREAS = [
    "product discovery", "customer interviews", "problem validation", "solution validation", "roadmap planning",
    "backlog prioritization", "RICE scoring", "MoSCoW prioritization", "OKRs", "north star metrics",
    "user personas", "jobs to be done", "MVP definition", "feature tradeoffs", "product requirements",
    "PRD writing", "go-to-market readiness", "launch planning", "experiment design", "A/B testing",
    "funnel analysis", "retention metrics", "churn analysis", "pricing decisions", "competitive analysis",
    "stakeholder alignment", "engineering tradeoffs", "technical debt prioritization", "customer feedback loops",
    "support ticket analysis", "analytics instrumentation", "success metrics", "product risk",
    "regulatory constraints", "platform products", "internal tools", "API products", "mobile product decisions",
    "growth features", "enterprise features", "accessibility requirements", "security requirements",
    "deprecation strategy", "release notes", "adoption measurement", "post-launch review",
]


CYBERSECURITY_AREAS = [
    "SIEM alert triage", "phishing investigation", "malware containment", "endpoint detection",
    "vulnerability management", "patch prioritization", "risk scoring", "incident severity",
    "identity and access review", "least privilege", "privileged access management", "MFA enforcement",
    "log analysis", "threat hunting", "IOC investigation", "network segmentation", "firewall rule review",
    "cloud security posture", "container security", "secrets exposure", "data loss prevention",
    "security awareness", "email security", "web application security", "OWASP Top 10", "SQL injection",
    "XSS prevention", "CSRF prevention", "zero trust", "security baselines", "audit evidence",
    "compliance control testing", "backup ransomware readiness", "incident communication",
    "forensic evidence handling", "root cause analysis", "post-incident review", "security monitoring",
    "false positive tuning", "SOC escalation", "third-party risk", "asset inventory", "certificate expiry",
    "key rotation", "encryption at rest", "encryption in transit",
]


CLOUD_ENGINEER_AREAS = [
    "landing zone design", "hub-and-spoke networking", "VPC or VNet design", "subnet planning",
    "network security groups", "private endpoints", "load balancing", "DNS troubleshooting",
    "IAM least privilege", "managed identities", "secret management", "cloud cost optimization",
    "tagging strategy", "budget alerts", "autoscaling", "high availability", "multi-region design",
    "disaster recovery", "backup strategy", "infrastructure as code", "Terraform state management",
    "CI/CD for infrastructure", "container deployment", "Kubernetes operations", "serverless design",
    "object storage lifecycle", "database managed services", "cloud monitoring", "log aggregation",
    "alert tuning", "incident response", "cloud migration", "rehost migration", "replatform migration",
    "refactor migration", "security posture management", "policy as code", "compliance controls",
    "certificate management", "zero-downtime deployment", "blue-green deployment", "canary rollout",
    "capacity planning", "quota limits", "service health events", "cloud access reviews",
]


DBA_AREAS = [
    "backup strategy", "restore validation", "point-in-time recovery", "RTO and RPO", "high availability",
    "replication lag", "failover testing", "disaster recovery drills", "query plan analysis",
    "index tuning", "statistics maintenance", "blocking sessions", "deadlocks", "isolation levels",
    "transaction log growth", "database capacity planning", "storage performance", "tempdb issues",
    "connection pool exhaustion", "slow stored procedures", "parameter sniffing", "partitioning",
    "archiving strategy", "database security", "least privilege access", "audit logging",
    "encryption at rest", "encryption in transit", "patching database servers", "version upgrades",
    "schema change review", "migration rollback", "data corruption response", "integrity checks",
    "maintenance windows", "monitoring and alerts", "database baselines", "performance regression",
    "cloud managed databases", "read replicas", "write scaling", "database cost optimization",
    "automation scripts", "runbook documentation", "incident postmortems", "developer query review",
]


def rows_from_areas(role_label: str, role_keyword: str, areas: list[str]) -> list[tuple[str, str, list[str], list[str]]]:
    rows = []
    for area in areas:
        title = area.replace("-", " ")
        question = f"How do you handle {title} as a {role_label}?"
        alternates = [
            f"What is your approach to {title}?",
            f"Walk me through a real scenario involving {title}.",
            f"What risks or tradeoffs do you watch for with {title}?",
        ]
        keywords = [role_keyword, title, "scenario", "risk", "best practices"]
        rows.append((title, question, alternates, keywords))
    return rows


PACKS = {
    "qa_engineer_deep.json": ("qa_engineer", "QA Engineer", QA),
    "data_engineer_deep.json": ("data_engineer", "Data Engineer", DATA_ENGINEER),
    "data_analyst_deep.json": ("data_analyst", "Data Analyst", DATA_ANALYST),
    "business_analyst_deep.json": (
        "business_analyst",
        "Business Analyst",
        rows_from_areas("Business Analyst", "business analyst", BUSINESS_ANALYST_AREAS),
    ),
    "project_manager_deep.json": (
        "project_manager",
        "Project Manager",
        rows_from_areas("Project Manager", "project manager", PROJECT_MANAGER_AREAS),
    ),
    "product_manager_deep.json": (
        "product_manager",
        "Product Manager",
        rows_from_areas("Product Manager", "product manager", PRODUCT_MANAGER_AREAS),
    ),
    "cybersecurity_deep.json": (
        "cybersecurity",
        "Cybersecurity Analyst",
        rows_from_areas("Cybersecurity Analyst", "cybersecurity analyst", CYBERSECURITY_AREAS),
    ),
    "cloud_engineer_deep.json": (
        "cloud_engineer",
        "Cloud Engineer",
        rows_from_areas("Cloud Engineer", "cloud engineer", CLOUD_ENGINEER_AREAS),
    ),
    "database_admin_deep.json": (
        "database_admin",
        "Database Administrator",
        rows_from_areas("Database Administrator", "database administrator", DBA_AREAS),
    ),
}


def write_pack(filename: str, pack_key: str, topic: str, rows: list[tuple[str, str, list[str], list[str]]]) -> None:
    payload = [
        make_item(pack_key, index, topic, area, question, alternates, keywords)
        for index, (area, question, alternates, keywords) in enumerate(rows, start=1)
    ]
    path = PACK_DIR / filename
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(payload)} items to {path.relative_to(ROOT)}")


def main() -> None:
    for filename, (pack_key, topic, rows) in PACKS.items():
        write_pack(filename, pack_key, topic, rows)


if __name__ == "__main__":
    main()
