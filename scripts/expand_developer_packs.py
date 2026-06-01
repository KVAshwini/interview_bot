import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "qa_library" / "professions"


def item(pack: str, idx: int, topic: str, area: str, question: str, alternates: list[str], keywords: list[str], difficulty: str = "high") -> dict:
    instant = (
        f"For {area}, I first pin down the expected behavior, the failing path, and the impact on users or downstream systems. "
        f"Then I trace the code and data flow, check edge cases and recent changes, and validate the answer with targeted tests. "
        f"If the topic has production risk, I also call out logging, monitoring, rollback, or regression coverage."
    )
    detailed = (
        f"For {area}, my answer would start with the exact behavior I expect and the signal showing that something is wrong. "
        f"From there I follow the request, job, or data path through the relevant layers and check state, validation, permissions, "
        f"error handling, concurrency, resource usage, and integration boundaries. If users are affected, I separate mitigation from root cause: "
        f"stabilize first, then fix carefully. I finish by explaining how I would prove the fix with tests, logs, metrics, or a small rollout, "
        f"so the interviewer hears both technical depth and production judgment."
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


GENERAL = [
    ("SOLID principles", "How do you apply SOLID principles in real code?", ["Explain SOLID with practical examples.", "How do you keep object-oriented code maintainable?"], ["solid", "oop", "maintainability", "design"]),
    ("dependency injection", "Why is dependency injection useful?", ["How does dependency injection improve testability?", "When do you use inversion of control?"], ["dependency injection", "ioc", "testing", "design"]),
    ("clean architecture", "How do you separate business logic from infrastructure?", ["How do you structure application layers?", "What belongs in service, repository, and controller layers?"], ["architecture", "layers", "business logic", "repository"]),
    ("API versioning", "How do you handle API versioning?", ["How do you avoid breaking API consumers?", "What is your strategy for backward compatibility?"], ["api", "versioning", "compatibility", "contracts"]),
    ("idempotency", "What is idempotency and why does it matter?", ["How do you prevent duplicate processing?", "How do you design safe retries?"], ["idempotency", "retries", "distributed systems", "api"]),
    ("concurrency", "How do you handle concurrency bugs?", ["How do you debug race conditions?", "What causes inconsistent state under load?"], ["concurrency", "race condition", "locking", "thread safety"]),
    ("caching", "How do you design caching safely?", ["When should you cache data?", "How do you avoid stale cache issues?"], ["cache", "ttl", "invalidation", "performance"]),
    ("pagination", "How do you design pagination for APIs?", ["Offset vs cursor pagination?", "How do you paginate large datasets?"], ["pagination", "cursor", "api", "database"]),
    ("logging", "What makes application logs useful?", ["How do you design logs for debugging?", "What should you avoid logging?"], ["logging", "correlation id", "debugging", "security"]),
    ("observability", "How do logs, metrics, and traces work together?", ["What is observability?", "How do you troubleshoot distributed systems?"], ["observability", "metrics", "tracing", "logs"]),
    ("feature flags", "How do you use feature flags safely?", ["How do you roll out risky changes?", "What are feature flag risks?"], ["feature flags", "rollout", "rollback", "release"]),
    ("database migrations", "How do you run database migrations safely?", ["How do you avoid breaking deployments with schema changes?", "What is backward-compatible migration?"], ["database", "migration", "schema", "deployment"]),
    ("message queues", "How do you use queues in application design?", ["When do you use asynchronous processing?", "How do you handle queue failures?"], ["queue", "async", "retry", "dead letter"]),
    ("distributed transactions", "How do you handle consistency across services?", ["How do you avoid distributed transaction problems?", "What is eventual consistency?"], ["distributed systems", "eventual consistency", "saga", "transactions"]),
    ("security basics", "What security practices do you follow as a developer?", ["How do you prevent common application vulnerabilities?", "What security checks belong in normal development?"], ["security", "owasp", "validation", "authorization"]),
    ("authorization", "How do you design authorization checks?", ["Where should permission checks happen?", "How do you prevent privilege escalation?"], ["authorization", "rbac", "permissions", "security"]),
    ("input validation", "How do you validate user input?", ["Client-side vs server-side validation?", "How do you prevent bad input?"], ["validation", "input", "security", "api"]),
    ("rate limiting", "How do you protect APIs from abuse?", ["How do rate limits work?", "How do you prevent traffic spikes from hurting services?"], ["rate limiting", "api", "security", "throttling"]),
    ("resilience", "How do you make services resilient?", ["How do you handle downstream service failures?", "Explain timeouts, retries, and circuit breakers."], ["resilience", "timeouts", "retries", "circuit breaker"]),
    ("data modeling", "How do you approach data modeling?", ["How do you design entities and relationships?", "How do you choose database schema structure?"], ["data model", "schema", "relationships", "database"]),
    ("testing pyramid", "How do you apply the testing pyramid?", ["How many unit, integration, and end-to-end tests should you write?", "How do you keep tests fast and useful?"], ["testing pyramid", "unit tests", "integration tests", "e2e"]),
    ("branching strategy", "How do you work with Git branches?", ["How do you keep pull requests manageable?", "What is your Git workflow?"], ["git", "branching", "pull request", "merge"]),
    ("CI pipeline", "What should a good CI pipeline include?", ["How do you catch problems before deployment?", "What checks should run in CI?"], ["ci", "pipeline", "tests", "quality gates"]),
    ("deployment rollback", "How do you plan rollback for a release?", ["What do you do when deployment causes issues?", "How do you reduce release risk?"], ["deployment", "rollback", "release", "risk"]),
    ("debugging production", "How do you debug without direct production access?", ["How do you troubleshoot with limited access?", "How do you support production safely?"], ["debugging", "production", "logs", "access"]),
    ("large refactor", "How do you plan a large refactor?", ["How do you reduce risk during refactoring?", "How do you modernize old code safely?"], ["refactoring", "legacy code", "tests", "migration"]),
    ("legacy code", "How do you work with legacy code?", ["How do you improve code you did not write?", "How do you add features to old systems?"], ["legacy code", "refactoring", "tests", "maintenance"]),
    ("code ownership", "How do you handle code ownership in a team?", ["How do you avoid knowledge silos?", "How do teams maintain shared code quality?"], ["code ownership", "teamwork", "documentation", "review"]),
    ("documentation", "What technical documentation do you write?", ["How do you document APIs and decisions?", "How do you keep documentation useful?"], ["documentation", "adr", "api docs", "runbook"]),
    ("incident follow-up", "What do you do after a production incident?", ["How do you prevent repeat incidents?", "What belongs in a postmortem?"], ["incident", "postmortem", "rca", "prevention"]),
    ("edge cases", "How do you identify edge cases?", ["How do you think beyond the happy path?", "What edge cases do you test?"], ["edge cases", "testing", "negative cases", "boundaries"]),
    ("time zones", "How do you handle time zones in applications?", ["Why are dates hard in software?", "How do you avoid timezone bugs?"], ["timezone", "datetime", "utc", "localization"]),
    ("file uploads", "How do you implement file upload safely?", ["What security issues exist with file uploads?", "How do you validate uploaded files?"], ["file upload", "security", "validation", "storage"]),
    ("background jobs", "How do you design background jobs?", ["How do you retry failed jobs?", "How do you monitor async workers?"], ["background jobs", "workers", "retry", "queue"]),
    ("configuration", "How do you manage application configuration?", ["How do you handle environment-specific settings?", "How do you avoid hardcoded config?"], ["configuration", "environment", "secrets", "settings"]),
    ("secrets", "How do you handle secrets in applications?", ["Where should API keys be stored?", "How do you avoid leaking secrets?"], ["secrets", "security", "environment variables", "key vault"]),
    ("multi-tenancy", "How do you design multi-tenant applications?", ["How do you isolate tenant data?", "What are multi-tenant risks?"], ["multi tenancy", "tenant isolation", "security", "database"]),
    ("data privacy", "How do you protect sensitive user data?", ["How do you handle PII?", "What should developers do for privacy?"], ["privacy", "pii", "encryption", "data protection"]),
    ("API errors", "How should APIs return errors?", ["What makes a good API error response?", "How do you structure validation errors?"], ["api", "errors", "status codes", "validation"]),
    ("schema compatibility", "How do you keep systems compatible during changes?", ["How do you deploy breaking changes safely?", "How do you support old and new clients?"], ["compatibility", "schema", "deployment", "versioning"]),
    ("load testing", "How do you validate an application under load?", ["How do you plan load tests?", "What metrics do you check during performance testing?"], ["load testing", "performance", "throughput", "latency"]),
    ("memory leaks", "How do you investigate memory leaks?", ["Application memory keeps growing. What do you check?", "How do you find retained objects?"], ["memory leak", "profiling", "heap", "performance"]),
    ("N+1 queries", "What is the N+1 query problem?", ["How do you detect N+1 database calls?", "How do you fix inefficient ORM queries?"], ["n+1", "orm", "database", "performance"]),
    ("data consistency", "How do you validate data consistency?", ["How do you prevent inconsistent records?", "How do you reconcile data across systems?"], ["data consistency", "reconciliation", "validation", "database"]),
    ("service ownership", "What does owning a service in production mean?", ["How do developers support what they build?", "What operational responsibilities should developers have?"], ["production ownership", "support", "monitoring", "runbook"]),
    ("design tradeoffs", "How do you explain technical tradeoffs?", ["How do you choose between two designs?", "How do you communicate engineering decisions?"], ["tradeoffs", "design", "communication", "architecture"]),
]


PYTHON = [
    ("decorators", "How do Python decorators work?", ["Explain decorators with an example.", "When would you use a decorator in Python?"], ["python", "decorators", "functions", "wrappers"]),
    ("generators", "When do you use generators in Python?", ["What is yield used for?", "How do generators help memory usage?"], ["python", "generators", "yield", "memory"]),
    ("context managers", "How do context managers work in Python?", ["What does with do in Python?", "How do you manage resources safely?"], ["python", "context manager", "with", "resources"]),
    ("typing", "How do you use type hints in Python?", ["Why use typing in Python?", "How do type hints help maintainability?"], ["python", "typing", "mypy", "maintainability"]),
    ("pydantic", "How does Pydantic help API development?", ["Why use Pydantic models?", "How do you validate request bodies in Python?"], ["python", "pydantic", "validation", "fastapi"]),
    ("sqlalchemy", "How do you use SQLAlchemy safely?", ["How do you manage sessions in SQLAlchemy?", "What are ORM risks?"], ["python", "sqlalchemy", "orm", "sessions"]),
    ("django orm", "How do you avoid performance issues in Django ORM?", ["How do select_related and prefetch_related help?", "How do you fix N+1 queries in Django?"], ["python", "django", "orm", "n+1"]),
    ("flask", "How do you structure a Flask application?", ["What belongs in Flask blueprints?", "How do you make Flask apps maintainable?"], ["python", "flask", "blueprints", "api"]),
    ("fastapi dependencies", "How do FastAPI dependencies work?", ["How do you inject database sessions in FastAPI?", "How do you share auth logic in FastAPI?"], ["python", "fastapi", "dependencies", "auth"]),
    ("celery", "How do you use Celery for background jobs?", ["How do you retry Celery tasks?", "How do you monitor Python background workers?"], ["python", "celery", "background jobs", "retry"]),
    ("pytest fixtures", "How do pytest fixtures work?", ["How do you share test setup in pytest?", "When do you use fixture scopes?"], ["python", "pytest", "fixtures", "testing"]),
    ("mocking", "How do you mock dependencies in Python tests?", ["When should you use unittest.mock?", "What should you avoid mocking?"], ["python", "mocking", "tests", "pytest"]),
    ("async blocking", "How do you avoid blocking the event loop?", ["What happens if async code calls blocking functions?", "How do you debug slow asyncio apps?"], ["python", "asyncio", "event loop", "blocking"]),
    ("multiprocessing", "When do you use multiprocessing in Python?", ["How do you run CPU-bound Python work?", "Threads vs processes in Python?"], ["python", "multiprocessing", "cpu bound", "gil"]),
    ("logging", "How do you set up logging in Python services?", ["What should Python logs include?", "How do you structure logs for production?"], ["python", "logging", "structured logs", "production"]),
    ("exceptions", "How do you design Python exception handling?", ["When do you raise custom exceptions?", "How do you avoid swallowing exceptions?"], ["python", "exceptions", "error handling", "custom exceptions"]),
    ("virtualenv", "How do you keep Python environments reproducible?", ["venv vs Poetry?", "How do you manage dependency versions?"], ["python", "venv", "poetry", "dependencies"]),
    ("packaging", "How do you package a Python project?", ["What is pyproject.toml?", "How do you publish or install Python packages?"], ["python", "packaging", "pyproject", "pip"]),
    ("performance profiling", "How do you profile Python performance?", ["Python code is slow. What tools do you use?", "How do you find bottlenecks in Python?"], ["python", "profiling", "cprofile", "performance"]),
    ("pandas performance", "How do you optimize pandas processing?", ["Pandas job is slow. What do you check?", "How do you reduce memory use in pandas?"], ["python", "pandas", "dataframe", "performance"]),
    ("streaming files", "How do you process large files in Python?", ["How do you avoid loading huge files into memory?", "How do you stream CSV or JSON data?"], ["python", "streaming", "files", "memory"]),
    ("api clients", "How do you build a reliable Python API client?", ["How do you handle retries and timeouts in requests?", "How do you call external APIs safely?"], ["python", "api client", "timeouts", "retries"]),
    ("security", "What Python security issues do you watch for?", ["How do you avoid unsafe deserialization?", "What are common Python security mistakes?"], ["python", "security", "deserialization", "secrets"]),
    ("dependency injection", "How do you apply dependency injection in Python?", ["How do you make Python code testable?", "How do you avoid hardcoded dependencies?"], ["python", "dependency injection", "testing", "design"]),
    ("dataclasses", "When would you use dataclasses?", ["Dataclass vs regular class?", "How do dataclasses improve Python models?"], ["python", "dataclasses", "models", "typing"]),
    ("collections", "How do you choose Python data structures?", ["List vs tuple vs set vs dict?", "How do Python dictionaries work in practice?"], ["python", "collections", "dict", "set"]),
    ("copying", "What is the difference between shallow copy and deep copy?", ["How do object references work in Python?", "When can copying cause bugs?"], ["python", "copy", "references", "mutability"]),
    ("mutability", "How do mutable defaults cause bugs in Python?", ["Why avoid mutable default arguments?", "Explain a common Python function default bug."], ["python", "mutability", "defaults", "bug"]),
    ("imports", "How do Python imports and modules work?", ["How do you avoid circular imports?", "How do you structure Python packages?"], ["python", "imports", "modules", "packages"]),
    ("configuration", "How do you manage configuration in Python apps?", ["How do Python apps read environment variables?", "How do you separate dev and prod config?"], ["python", "configuration", "environment", "settings"]),
    ("database migrations", "How do you run migrations in Python projects?", ["How do you use Alembic?", "How do you manage schema changes with SQLAlchemy?"], ["python", "alembic", "migrations", "database"]),
    ("auth", "How do you implement authentication in a Python API?", ["How do you validate JWT in FastAPI?", "How do you secure Python endpoints?"], ["python", "authentication", "jwt", "fastapi"]),
    ("authorization", "How do you implement authorization in Python services?", ["How do you check permissions in Python APIs?", "How do you enforce RBAC?"], ["python", "authorization", "rbac", "permissions"]),
    ("background retries", "How do you design retries for Python background jobs?", ["How do you avoid duplicate task processing?", "How do you handle failed Python jobs?"], ["python", "background jobs", "retries", "idempotency"]),
    ("websockets", "How do you handle WebSockets in Python?", ["When use WebSockets instead of REST?", "How do you manage realtime Python connections?"], ["python", "websocket", "realtime", "fastapi"]),
    ("testing APIs", "How do you test FastAPI endpoints?", ["How do you use TestClient?", "How do you test Python API validation?"], ["python", "fastapi", "testclient", "api tests"]),
    ("linting", "How do you maintain Python code quality?", ["What tools do you use for linting and formatting?", "How do ruff, black, or mypy help?"], ["python", "linting", "formatting", "ruff"]),
    ("docker", "How do you containerize a Python service?", ["What belongs in a Python Dockerfile?", "How do you keep Python images small?"], ["python", "docker", "container", "deployment"]),
    ("gunicorn", "How do you run Python web apps in production?", ["Uvicorn vs Gunicorn?", "How do workers affect Python API performance?"], ["python", "gunicorn", "uvicorn", "workers"]),
    ("secrets", "How do you protect secrets in Python applications?", ["How do you avoid committing secrets?", "How do Python apps access secret stores?"], ["python", "secrets", "security", "environment"]),
    ("serialization", "How do you handle JSON serialization in Python?", ["How do you serialize datetimes?", "How do you avoid API serialization bugs?"], ["python", "json", "serialization", "datetime"]),
    ("data validation", "How do you validate data pipelines in Python?", ["How do you test Python ETL code?", "How do you catch bad data in Python jobs?"], ["python", "data validation", "etl", "pipeline"]),
    ("thread safety", "How do you handle thread safety in Python?", ["When are Python objects not thread-safe?", "How do you protect shared state?"], ["python", "thread safety", "locks", "concurrency"]),
    ("file handling", "How do you handle files safely in Python?", ["How do you avoid file descriptor leaks?", "How do you use pathlib and context managers?"], ["python", "files", "pathlib", "context manager"]),
]


JAVA = [
    ("spring security", "How do you secure endpoints in Spring Security?", ["How do you configure authentication and authorization in Spring?", "How do you protect Java APIs?"], ["java", "spring security", "authorization", "jwt"]),
    ("jpa performance", "How do you avoid JPA performance problems?", ["How do you fix N+1 queries in Hibernate?", "What are common ORM issues in Java?"], ["java", "jpa", "hibernate", "n+1"]),
    ("garbage collection", "How does garbage collection affect Java applications?", ["What GC metrics do you monitor?", "How do you tune GC issues?"], ["java", "garbage collection", "jvm", "performance"]),
    ("streams", "When do you use Java Streams?", ["What are the tradeoffs of streams?", "How do you avoid stream performance mistakes?"], ["java", "streams", "collections", "performance"]),
    ("optionals", "How do you use Optional correctly?", ["When should Optional not be used?", "How does Optional reduce null bugs?"], ["java", "optional", "null", "api design"]),
    ("equals hashcode", "Why are equals and hashCode important?", ["What happens if hashCode is wrong?", "How do Java collections use equals?"], ["java", "equals", "hashcode", "collections"]),
    ("immutability", "Why is immutability useful in Java?", ["How do immutable objects help concurrency?", "How do you design immutable classes?"], ["java", "immutability", "thread safety", "design"]),
    ("thread pools", "How do you configure Java thread pools?", ["What can go wrong with ExecutorService?", "How do thread pools affect performance?"], ["java", "thread pool", "executorservice", "concurrency"]),
    ("completablefuture", "When do you use CompletableFuture?", ["How do you handle async work in Java?", "How do you combine async operations?"], ["java", "completablefuture", "async", "concurrency"]),
    ("locks", "How do you handle synchronization in Java?", ["synchronized vs ReentrantLock?", "How do you avoid deadlocks?"], ["java", "synchronization", "locks", "deadlock"]),
    ("spring transactions", "What can go wrong with @Transactional?", ["Why might Spring transaction rollback not happen?", "How do proxy transactions work?"], ["java", "spring", "transactional", "rollback"]),
    ("bean lifecycle", "Explain Spring bean lifecycle.", ["How does Spring create beans?", "What is dependency injection in Spring?"], ["java", "spring", "bean lifecycle", "dependency injection"]),
    ("configuration", "How do you manage Spring configuration?", ["Profiles vs properties?", "How do you separate environment config in Java?"], ["java", "spring", "configuration", "profiles"]),
    ("actuator", "How do you use Spring Boot Actuator?", ["What production endpoints do you expose?", "How do you monitor Spring Boot apps?"], ["java", "spring boot", "actuator", "monitoring"]),
    ("exception handling", "How do you handle exceptions in Spring Boot?", ["How do you use ControllerAdvice?", "How do you return clean API errors in Java?"], ["java", "spring boot", "exceptions", "controlleradvice"]),
    ("validation", "How do you validate requests in Spring Boot?", ["How do Bean Validation annotations work?", "How do you handle validation errors?"], ["java", "spring boot", "validation", "bean validation"]),
    ("microservices resilience", "How do you make Java microservices resilient?", ["How do you handle downstream failures?", "How do retries and circuit breakers work in Java?"], ["java", "microservices", "resilience", "circuit breaker"]),
    ("kafka", "How do you consume Kafka messages in Java?", ["How do Kafka consumer groups work?", "How do you handle retries in Kafka consumers?"], ["java", "kafka", "consumer", "retry"]),
    ("idempotency", "How do you make Java message processing idempotent?", ["How do you prevent duplicate events?", "How do you handle Kafka redelivery?"], ["java", "idempotency", "messaging", "events"]),
    ("maven gradle", "How do Maven and Gradle manage builds?", ["Maven vs Gradle?", "How do you manage Java dependencies?"], ["java", "maven", "gradle", "dependencies"]),
    ("testing slices", "How do Spring test slices work?", ["When use @WebMvcTest vs @SpringBootTest?", "How do you keep Spring tests fast?"], ["java", "spring tests", "webmvctest", "springboottest"]),
    ("testcontainers", "Why use Testcontainers?", ["How do you test database integration in Java?", "How do you avoid fake integration tests?"], ["java", "testcontainers", "integration tests", "database"]),
    ("mockito", "How do you use Mockito effectively?", ["When should you mock dependencies?", "What are mocking pitfalls?"], ["java", "mockito", "unit tests", "mocking"]),
    ("records", "When would you use Java records?", ["What are records good for?", "Records vs classes in Java?"], ["java", "records", "dto", "immutability"]),
    ("sealed classes", "What are sealed classes useful for?", ["How do sealed types improve design?", "When use sealed classes in Java?"], ["java", "sealed classes", "types", "design"]),
    ("generics", "How do Java generics work?", ["What is type erasure?", "Why use generics?"], ["java", "generics", "type erasure", "collections"]),
    ("class loading", "How does Java class loading work?", ["What are classpath issues?", "How do dependency conflicts happen?"], ["java", "classloader", "classpath", "dependencies"]),
    ("memory leaks", "How can Java have memory leaks?", ["What causes retained objects in Java?", "How do you detect Java memory leaks?"], ["java", "memory leak", "heap dump", "jvm"]),
    ("api pagination", "How do you implement pagination in Spring APIs?", ["Page vs Slice in Spring Data?", "How do you paginate large tables?"], ["java", "spring data", "pagination", "api"]),
    ("database migrations", "How do you manage database migrations in Java apps?", ["Flyway vs Liquibase?", "How do you deploy schema changes safely?"], ["java", "flyway", "liquibase", "migrations"]),
    ("security secrets", "How do Java services handle secrets?", ["How do you avoid secrets in application.properties?", "How do apps access Key Vault or secret managers?"], ["java", "secrets", "security", "configuration"]),
    ("logging", "How do you structure Java application logs?", ["What should Spring Boot logs include?", "How do correlation IDs work?"], ["java", "logging", "slf4j", "correlation id"]),
    ("tracing", "How do you trace requests across Java services?", ["How do distributed traces help?", "How do you debug cross-service latency?"], ["java", "tracing", "observability", "microservices"]),
    ("rest template webclient", "RestTemplate vs WebClient?", ["When do you use WebClient?", "How do Java services call external APIs?"], ["java", "webclient", "resttemplate", "http client"]),
    ("timeouts", "How do you configure timeouts in Java API clients?", ["What happens without timeouts?", "How do you prevent thread exhaustion?"], ["java", "timeouts", "http client", "resilience"]),
    ("serialization", "How do you handle JSON serialization in Java?", ["How do Jackson annotations help?", "How do you avoid API serialization bugs?"], ["java", "jackson", "json", "serialization"]),
    ("date time", "How do you handle dates and time zones in Java?", ["Why use java.time?", "How do you avoid timezone bugs?"], ["java", "datetime", "timezone", "java.time"]),
    ("batch", "How do you design batch jobs in Java?", ["How do Spring Batch jobs work?", "How do you restart failed batch jobs?"], ["java", "spring batch", "batch jobs", "restart"]),
    ("file processing", "How do you process large files in Java?", ["How do you avoid memory issues with files?", "How do streams help file processing?"], ["java", "files", "streaming", "memory"]),
    ("containerization", "How do you containerize a Java service?", ["How do JVM settings work in containers?", "How do you keep Java Docker images efficient?"], ["java", "docker", "container", "jvm"]),
    ("blue green", "How do Java services support zero-downtime deployment?", ["How do you deploy without breaking clients?", "How do you handle rolling deployments?"], ["java", "deployment", "zero downtime", "compatibility"]),
    ("api gateway", "How do Java services work behind an API gateway?", ["What belongs in gateway vs service?", "How do you handle auth and routing?"], ["java", "api gateway", "routing", "auth"]),
    ("validation groups", "When would you use validation groups?", ["How do you validate create vs update differently?", "How do Bean Validation groups work?"], ["java", "validation groups", "bean validation", "spring"]),
    ("domain events", "How do you use domain events in Java?", ["When do you publish events from a service?", "How do domain events reduce coupling?"], ["java", "domain events", "events", "ddd"]),
]


SQL = [
    ("execution plan", "How do you read an execution plan?", ["What do you look for in a query plan?", "How do execution plans reveal bottlenecks?"], ["sql", "execution plan", "query tuning", "performance"]),
    ("sargability", "What does sargable mean in SQL?", ["Why do functions on columns hurt indexes?", "How do you write index-friendly predicates?"], ["sql", "sargable", "indexes", "predicates"]),
    ("parameter sniffing", "What is parameter sniffing?", ["How can parameters make SQL performance inconsistent?", "How do you fix parameter sniffing issues?"], ["sql", "parameter sniffing", "query plan", "performance"]),
    ("covering indexes", "What is a covering index?", ["How do included columns help?", "When would you create a covering index?"], ["sql", "covering index", "included columns", "performance"]),
    ("composite indexes", "How do you design composite indexes?", ["Why does column order matter in indexes?", "How do multi-column indexes work?"], ["sql", "composite index", "column order", "indexing"]),
    ("deadlocks", "How do you troubleshoot SQL deadlocks?", ["What causes database deadlocks?", "How do you reduce deadlocks?"], ["sql", "deadlock", "locks", "transactions"]),
    ("isolation levels", "Explain SQL isolation levels.", ["Read committed vs snapshot isolation?", "How do isolation levels affect concurrency?"], ["sql", "isolation level", "transactions", "concurrency"]),
    ("transactions", "How do you design safe SQL transactions?", ["How long should transactions stay open?", "How do you avoid lock contention?"], ["sql", "transactions", "locking", "consistency"]),
    ("normalization", "What is normalization and when would you denormalize?", ["How do you design relational schema?", "What are normalization tradeoffs?"], ["sql", "normalization", "denormalization", "schema"]),
    ("cte", "When do you use CTEs?", ["CTE vs subquery?", "How do common table expressions help readability?"], ["sql", "cte", "subquery", "readability"]),
    ("recursive cte", "What is a recursive CTE?", ["How do you query hierarchical data?", "How do you handle parent-child relationships in SQL?"], ["sql", "recursive cte", "hierarchy", "tree"]),
    ("window frames", "How do window frames work?", ["Rows vs range in window functions?", "How do running totals work in SQL?"], ["sql", "window functions", "rows", "range"]),
    ("deduplication", "How do you remove duplicates in SQL?", ["How do you find duplicate records?", "How do you keep the latest row per key?"], ["sql", "duplicates", "row_number", "deduplication"]),
    ("merge upsert", "How do you implement upserts?", ["MERGE vs insert/update?", "How do you load changed records safely?"], ["sql", "merge", "upsert", "etl"]),
    ("incremental load", "How do you design incremental SQL loads?", ["How do you use watermarks?", "How do you avoid full reloads?"], ["sql", "incremental load", "watermark", "etl"]),
    ("partitioning", "How does table partitioning help?", ["When should you partition a table?", "What are partitioning risks?"], ["sql", "partitioning", "large tables", "performance"]),
    ("temp tables", "When do you use temp tables?", ["Temp table vs table variable?", "How do temp objects affect SQL performance?"], ["sql", "temp table", "table variable", "performance"]),
    ("views", "When should you use SQL views?", ["View vs table?", "What are view performance concerns?"], ["sql", "views", "abstraction", "performance"]),
    ("materialized views", "What are materialized views used for?", ["How do indexed views help?", "When do you precompute query results?"], ["sql", "materialized view", "indexed view", "performance"]),
    ("stored proc errors", "How do you handle errors in stored procedures?", ["How do try/catch blocks work in SQL procedures?", "How do you rollback on stored procedure failure?"], ["sql", "stored procedure", "error handling", "rollback"]),
    ("dynamic sql", "When is dynamic SQL appropriate?", ["What are dynamic SQL risks?", "How do you prevent SQL injection in dynamic SQL?"], ["sql", "dynamic sql", "injection", "security"]),
    ("sql injection", "How do you prevent SQL injection?", ["Why use parameterized queries?", "What makes string-built SQL dangerous?"], ["sql", "sql injection", "parameterized queries", "security"]),
    ("referential integrity", "How do foreign keys protect data quality?", ["When should you use foreign key constraints?", "What are referential integrity tradeoffs?"], ["sql", "foreign key", "referential integrity", "constraints"]),
    ("constraints", "How do constraints improve database design?", ["Check constraint vs application validation?", "What constraints do you add to tables?"], ["sql", "constraints", "check constraint", "data integrity"]),
    ("nulls", "How do NULL values affect SQL queries?", ["Why can NULL cause bugs?", "How do you handle NULLs in joins and filters?"], ["sql", "null", "three-valued logic", "filters"]),
    ("aggregates", "How do GROUP BY queries go wrong?", ["How do joins inflate aggregates?", "How do you avoid double counting in SQL?"], ["sql", "group by", "aggregation", "double counting"]),
    ("having", "WHERE vs HAVING?", ["When do you filter before or after aggregation?", "Explain HAVING clause."], ["sql", "where", "having", "aggregation"]),
    ("set operations", "UNION vs UNION ALL?", ["When do you use INTERSECT or EXCEPT?", "How do SQL set operations work?"], ["sql", "union", "intersect", "except"]),
    ("ranking", "RANK vs DENSE_RANK vs ROW_NUMBER?", ["How do SQL ranking functions differ?", "How do you find top records per group?"], ["sql", "rank", "dense_rank", "row_number"]),
    ("date queries", "How do you write safe date filters?", ["How do date ranges cause off-by-one bugs?", "How do you filter by day in SQL?"], ["sql", "date", "filter", "timezone"]),
    ("slow reports", "How do you optimize slow reporting queries?", ["Dashboard query is slow. What do you check?", "How do you tune analytical SQL?"], ["sql", "reporting", "dashboard", "performance"]),
    ("etl validation", "How do you validate ETL output with SQL?", ["How do you reconcile source and target tables?", "What SQL checks prove a load succeeded?"], ["sql", "etl", "validation", "reconciliation"]),
    ("data warehouse", "Star schema vs snowflake schema?", ["How do fact and dimension tables work?", "How do you model analytics data?"], ["sql", "data warehouse", "star schema", "dimensions"]),
    ("slow inserts", "How do you troubleshoot slow inserts?", ["What slows down bulk loads?", "How do indexes affect insert performance?"], ["sql", "insert", "bulk load", "performance"]),
    ("locking", "How do you investigate blocking sessions?", ["Why are users waiting on database locks?", "How do you find blockers in SQL?"], ["sql", "blocking", "locks", "sessions"]),
    ("statistics", "Why are database statistics important?", ["How do stale stats affect query plans?", "When do you update statistics?"], ["sql", "statistics", "query optimizer", "performance"]),
    ("index maintenance", "How do you maintain indexes?", ["Fragmentation vs statistics?", "How do you decide rebuild or reorganize?"], ["sql", "index maintenance", "fragmentation", "statistics"]),
    ("query hints", "When should you use query hints?", ["Why are query hints risky?", "How do you avoid overusing hints?"], ["sql", "query hints", "optimizer", "performance"]),
    ("permissions", "How do you manage SQL permissions?", ["How do you apply least privilege in databases?", "How do roles work in SQL security?"], ["sql", "permissions", "least privilege", "security"]),
    ("auditing", "How do you audit database changes?", ["How do you track who changed data?", "What database audit logs matter?"], ["sql", "audit", "change tracking", "security"]),
    ("backup restore", "What should SQL developers know about backups?", ["How do schema changes affect restore plans?", "Why test database restores?"], ["sql", "backup", "restore", "recovery"]),
    ("migration rollback", "How do you rollback a bad SQL migration?", ["How do you make schema deployments reversible?", "What if a migration fails halfway?"], ["sql", "migration", "rollback", "deployment"]),
    ("large deletes", "How do you delete large amounts of data safely?", ["Why can big deletes hurt production?", "How do you batch delete records?"], ["sql", "delete", "batching", "locks"]),
    ("archiving", "How do you archive old database data?", ["How do you keep large tables manageable?", "How do retention policies affect SQL design?"], ["sql", "archiving", "retention", "partitioning"]),
]


FULLSTACK = [
    ("component design", "How do you design reusable frontend components?", ["What makes a React component reusable?", "How do you avoid over-abstracting UI components?"], ["full stack", "react", "components", "frontend"]),
    ("typescript", "Why use TypeScript in full-stack apps?", ["How does TypeScript reduce bugs?", "How do frontend and backend types stay aligned?"], ["full stack", "typescript", "types", "frontend"]),
    ("routing", "How do you handle routing in a single-page app?", ["Client routing vs server routing?", "How do protected routes work?"], ["full stack", "routing", "spa", "react"]),
    ("server rendering", "SSR vs CSR?", ["When do you use server-side rendering?", "What are tradeoffs of client-side rendering?"], ["full stack", "ssr", "csr", "frontend"]),
    ("api integration", "How do you integrate frontend with backend APIs?", ["How do you handle loading and error states?", "How do frontend apps call APIs reliably?"], ["full stack", "api", "frontend", "backend"]),
    ("error boundaries", "What are React error boundaries?", ["How do you handle frontend crashes?", "How do you prevent one UI error from breaking a page?"], ["full stack", "react", "error boundary", "frontend"]),
    ("forms", "How do you build complex forms?", ["How do you manage form validation and submission?", "How do you handle form errors from APIs?"], ["full stack", "forms", "validation", "frontend"]),
    ("accessibility", "How do you make web apps accessible?", ["What accessibility checks do you perform?", "How do ARIA and keyboard navigation matter?"], ["full stack", "accessibility", "aria", "frontend"]),
    ("responsive design", "How do you build responsive layouts?", ["How do you support desktop and mobile?", "What causes layout bugs?"], ["full stack", "responsive design", "css", "frontend"]),
    ("css architecture", "How do you manage CSS at scale?", ["CSS modules vs utility classes?", "How do you prevent style conflicts?"], ["full stack", "css", "styles", "frontend"]),
    ("frontend testing", "How do you test frontend code?", ["Unit vs component vs end-to-end tests?", "How do you test React behavior?"], ["full stack", "frontend testing", "react", "e2e"]),
    ("e2e testing", "What should end-to-end tests cover?", ["How do you avoid flaky UI tests?", "What user journeys should be automated?"], ["full stack", "e2e", "playwright", "testing"]),
    ("api security", "How do you secure frontend to backend communication?", ["How do you protect tokens?", "How do CORS and cookies affect security?"], ["full stack", "security", "cors", "cookies"]),
    ("csrf", "What is CSRF and how do you prevent it?", ["When are CSRF tokens needed?", "How do SameSite cookies help?"], ["full stack", "csrf", "security", "cookies"]),
    ("xss", "What is XSS and how do you prevent it?", ["How can frontend code expose XSS?", "How do escaping and CSP help?"], ["full stack", "xss", "security", "frontend"]),
    ("cors", "Explain CORS.", ["Why do browsers block cross-origin requests?", "How do you configure CORS safely?"], ["full stack", "cors", "api", "security"]),
    ("jwt refresh", "How do you handle token refresh?", ["How do refresh tokens work?", "How do you handle expired sessions?"], ["full stack", "jwt", "refresh token", "auth"]),
    ("file uploads", "How do you implement file uploads end to end?", ["How do frontend uploads connect to backend storage?", "How do you validate uploaded files?"], ["full stack", "file upload", "storage", "security"]),
    ("real time", "How do you build realtime features?", ["WebSockets vs polling?", "How do you handle live updates in full-stack apps?"], ["full stack", "websocket", "realtime", "polling"]),
    ("notifications", "How do you design notification systems?", ["How do in-app and email notifications work?", "How do you avoid duplicate notifications?"], ["full stack", "notifications", "events", "backend"]),
    ("search", "How do you implement search in a web app?", ["Database search vs search engine?", "How do filters and pagination work with search?"], ["full stack", "search", "filters", "pagination"]),
    ("optimistic updates", "What are optimistic UI updates?", ["When should the UI update before the server responds?", "How do you rollback optimistic changes?"], ["full stack", "optimistic update", "frontend", "api"]),
    ("cache invalidation", "How do you handle frontend cache invalidation?", ["How do you keep UI data fresh?", "How do query caches work?", "The browser shows old data after the backend update succeeds. What do you check?"], ["full stack", "cache", "invalidation", "frontend"]),
    ("backend pagination", "How should backend pagination support the frontend?", ["How do APIs return paged data?", "Cursor vs offset for frontend lists?"], ["full stack", "pagination", "api", "frontend"]),
    ("schema sharing", "How do you share schemas between frontend and backend?", ["How do OpenAPI or generated types help?", "How do you avoid contract drift?"], ["full stack", "openapi", "schemas", "typescript"]),
    ("environment config", "How do you manage frontend and backend configuration?", ["How do environment variables work in web apps?", "What config should not be exposed to browsers?"], ["full stack", "configuration", "environment", "secrets"]),
    ("deployment", "How do you deploy a full-stack application?", ["How do frontend and backend deploy together?", "What should a full-stack CI/CD pipeline do?"], ["full stack", "deployment", "ci cd", "frontend"]),
    ("monorepo", "When would you use a monorepo?", ["Monorepo vs multiple repos?", "How do full-stack teams share code?"], ["full stack", "monorepo", "workspace", "shared code"]),
    ("api errors", "How should backend errors appear in the UI?", ["How do you map API errors to form errors?", "What makes error handling user-friendly?"], ["full stack", "api errors", "frontend", "ux"]),
    ("loading states", "How do you design loading and empty states?", ["How do you prevent confusing UI states?", "How do frontend apps handle slow APIs?"], ["full stack", "loading states", "ux", "frontend"]),
    ("database design", "How does database design affect the frontend?", ["How do backend data models shape UI behavior?", "How do you avoid overfetching?"], ["full stack", "database", "api design", "frontend"]),
    ("graphql", "When would you use GraphQL?", ["GraphQL vs REST?", "What are GraphQL tradeoffs?"], ["full stack", "graphql", "rest", "api"]),
    ("rest design", "What makes a REST API easy for frontend teams?", ["How do you design resource endpoints?", "What should API responses include?"], ["full stack", "rest", "api design", "frontend"]),
    ("backend validation", "How do backend validation rules reach the frontend?", ["How do you show server validation errors?", "How do shared validation schemas help?"], ["full stack", "validation", "api", "forms"]),
    ("role based ui", "How do you handle role-based UI behavior?", ["Should frontend hide unauthorized actions?", "How do backend permissions and UI permissions work together?"], ["full stack", "rbac", "authorization", "ui"]),
    ("performance budgets", "What is a frontend performance budget?", ["How do you prevent bundle size growth?", "How do you monitor web performance over time?"], ["full stack", "performance budget", "bundle", "web vitals"]),
    ("image optimization", "How do you optimize images in web apps?", ["How do image sizes affect performance?", "What are lazy loading and responsive images?"], ["full stack", "images", "performance", "frontend"]),
    ("large lists", "How do you render large lists efficiently?", ["What is virtualization?", "How do you avoid slow tables in frontend apps?"], ["full stack", "virtualization", "large lists", "performance"]),
    ("state bugs", "How do you debug stale state in React?", ["Why does UI show old data?", "How do closures and async updates affect React state?"], ["full stack", "react", "state", "debugging"]),
    ("race conditions", "How do race conditions happen in frontend apps?", ["How do you handle multiple API responses arriving out of order?", "How do you cancel stale requests?"], ["full stack", "race condition", "api", "frontend"]),
    ("offline support", "How do you design offline-friendly web apps?", ["How do service workers help?", "How do you sync data after reconnecting?"], ["full stack", "offline", "service worker", "sync"]),
    ("analytics", "How do you add analytics without hurting users?", ["How do you track product events safely?", "What privacy concerns exist with analytics?"], ["full stack", "analytics", "privacy", "events"]),
    ("feature flags", "How do full-stack feature flags work?", ["How do you roll out UI and backend changes safely?", "How do you prevent inconsistent flag behavior?"], ["full stack", "feature flags", "rollout", "backend"]),
    ("debugging production", "How do you debug a production full-stack issue?", ["How do you trace a bug from browser to backend?", "What do you check when a user reports a broken page?"], ["full stack", "debugging", "browser", "logs"]),
]


PACKS = {
    "developer_general_deep.json": ("developer_general", "Software Developer - General", GENERAL),
    "developer_python_deep.json": ("developer_python", "Python Developer", PYTHON),
    "developer_java_deep.json": ("developer_java", "Java Developer", JAVA),
    "developer_sql_deep.json": ("developer_sql", "SQL Developer", SQL),
    "developer_fullstack_deep.json": ("developer_fullstack", "Full Stack Developer", FULLSTACK),
}


def write_pack(filename: str, pack_key: str, topic: str, rows: list[tuple[str, str, list[str], list[str]]]) -> None:
    payload = [
        item(pack_key, index, topic, area, question, alternates, keywords)
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
