# Synthetic Data Disclosure & Provenance Note

## 📊 Overview
To build and evaluate this end-to-end Workforce Intelligence & Upskilling platform, the project combines **real foundational datasets** with **synthetically generated artifacts** designed to simulate real-world enterprise HR environments.

---

## 1. 🟢 Real Datasets (Located in `data/raw/`)
These five datasets are sourced from real-world open-source benchmarks and public taxonomies:

1. **`employee_attrition.csv`**: IBM HR Analytics Employee Attrition & Performance dataset (1,470 records, 35 features).
2. **`hr_performance_engagement.csv`**: Employee performance and appraisal metrics dataset.
3. **`occupation_data.csv`**: O*NET Standard Occupational Classification (SOC) reference taxonomy.
4. **`essential_skills.csv`**: O*NET essential workplace skills by occupational title.
5. **`software_skills.csv`**: O*NET software, programming, and technical tools taxonomy.

---

## 2. 🟡 Synthetically Generated Data & Artifacts
The following datasets, documents, and files were synthetically generated to model complete end-to-end talent workflows:

1. **`data/processed/employee_skills.csv`**: Individual employee skill portfolios and proficiency ratings.
2. **`data/processed/role_skills.csv`**: Standardized role-to-skill competency profiles.
3. **`data/processed/courses.csv`**: Upskilling course catalog (titles, durations, providers, target skills).
4. **`data/processed/performance_history.csv`**: Multi-year performance and evaluation records.
5. **`data/processed/engagement_data.csv`**: Synthetically aggregated engagement score categories.
6. **`data/hr_policies/*.pdf`**: Simulated company policy documents (Leave, Remote Work, Payroll, Learning).
7. **`data/resumes/*.pdf, *.txt`**: Simulated candidate resumes for recruiting and screening.
8. **`data/job_descriptions/*.txt`**: Standardized job descriptions for engineering and analyst roles.

> [!NOTE]
> Synthetic data is used exclusively for functional simulation, RAG demonstration, and candidate matching pipelines. It contains no real personal identifiable information (PII).
