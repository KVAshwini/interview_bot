# Profession Packs

This folder contains role-focused interview content used by the professions UI and local answer search.

Current pack files:

- `starter_professions.json`: baseline questions across non-DevOps roles.
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
