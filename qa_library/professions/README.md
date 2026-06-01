# Profession Packs

This folder contains role-focused interview content used by the professions UI and local answer search.

Current pack files:

- `starter_professions.json`: baseline questions across non-DevOps roles.
- `developer_general.json`: general software engineering process, reliability, and maintainability.
- `developer_python.json`: Python, FastAPI, asyncio, pytest, packaging, and runtime troubleshooting.
- `developer_java.json`: Java, Spring Boot, JVM, transactions, collections, microservices, and testing.
- `developer_sql.json`: SQL query tuning, indexes, joins, window functions, stored procedures, and data quality.
- `developer_fullstack.json`: React, frontend/backend contracts, auth, validation, frontend performance, and full-stack debugging.
- `developer_general_deep.json`: expanded deep technical general developer coverage.
- `developer_python_deep.json`: expanded deep technical Python developer coverage.
- `developer_java_deep.json`: expanded deep technical Java developer coverage.
- `developer_sql_deep.json`: expanded deep technical SQL developer coverage.
- `developer_fullstack_deep.json`: expanded deep technical full-stack developer coverage.
- `qa_engineer.json`: QA Engineer fundamentals.
- `qa_engineer_advanced.json`: deeper QA/SDET, automation, API, performance, security, and CI/CD questions.
- `expanded_professions.json`: expanded coverage for developer, data, analyst, business, project, product, cybersecurity, cloud, and DBA roles.

Each item includes:

- `question`
- `alternate_questions`
- `instant_answer`
- `detailed_answer`
- `keywords`
- `difficulty`
- `answer_style`

The loader imports every `.json` file under `qa_library/`, so new profession pack files are included automatically after running:

```powershell
python scripts\build_database.py
```

Developer specialization targets:

- Software Developer - General: 50 Q&A items.
- Python Developer: 50 Q&A items.
- Java Developer: 50 Q&A items.
- SQL Developer: 50 Q&A items.
- Full Stack Developer: 50 Q&A items.
