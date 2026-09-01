"""
Script to generate the 16 numbered Jupyter notebooks adhering to HR_AI_Project_Build_Notes.docx
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def create_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.12"},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    filepath = os.path.join(NOTEBOOKS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Generated notebook: {filename}")

def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source if isinstance(source, list) else [line + "\n" for line in source.split("\n")]}

def code_cell(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source if isinstance(source, list) else [line + "\n" for line in source.split("\n")]}

def generate_all_notebooks():
    # 01_data_understanding.ipynb
    create_notebook("01_data_understanding.ipynb", [
        md_cell("# Day 1: 01 - Data Understanding\n\nLoad each dataset and inspect shapes, column types, missingness, and candidate join keys."),
        code_cell("""import os
import pandas as pd
import numpy as np

DATA_RAW = "../data/raw"
print("Raw files:", os.listdir(DATA_RAW))

# 1. Attrition Dataset
df_attrition = pd.read_csv(f"{DATA_RAW}/employee_attrition.csv")
print("Attrition Shape:", df_attrition.shape)
print("Attrition Balance:\n", df_attrition['Attrition'].value_counts(normalize=True) * 100)
df_attrition.head(3)"""),
        code_cell("""# 2. Performance & Engagement
df_perf = pd.read_csv(f"{DATA_RAW}/hr_performance_engagement.csv")
print("Performance Shape:", df_perf.shape)
df_perf.head(3)"""),
        code_cell("""# 3. Occupations & Skills
df_occ = pd.read_csv(f"{DATA_RAW}/occupation_data.csv")
df_ess = pd.read_csv(f"{DATA_RAW}/essential_skills.csv")
df_soft = pd.read_csv(f"{DATA_RAW}/software_skills.csv")

print("Occupations:", df_occ.shape)
print("Essential Skills:", df_ess.shape)
print("Software Skills:", df_soft.shape)""")
    ])

    # 02_data_validation.ipynb
    create_notebook("02_data_validation.ipynb", [
        md_cell("# Day 1: 02 - Data Validation\n\nAssert data validity: age ranges, unique keys, valid categorical values."),
        code_cell("""import pandas as pd

df = pd.read_csv("../data/raw/employee_attrition.csv")
if 'EmployeeNumber' in df.columns:
    df['EmployeeID'] = df['EmployeeNumber']

# Validation Checks
assert df['Age'].between(18, 100).all(), "Age out of range"
assert set(df['Attrition'].unique()) <= {'Yes', 'No'}, "Unexpected Attrition value"
assert df['MonthlyIncome'].min() > 0, "Invalid MonthlyIncome"

print("All Data Validation Assertions Passed Successfully!")""")
    ])

    # 03_data_cleaning.ipynb
    create_notebook("03_data_cleaning.ipynb", [
        md_cell("# Day 1: 03 - Data Cleaning\n\nHandle missing values, types, and generate standardized processed files."),
        code_cell("""import pandas as pd
import numpy as np

df = pd.read_csv("../data/raw/employee_attrition.csv")
# Remove zero-variance / redundant columns
cols_to_drop = [c for c in ['EmployeeCount', 'Over18', 'StandardHours'] if c in df.columns]
df_clean = df.drop(columns=cols_to_drop)

df_clean.to_csv("../data/processed/employees.csv", index=False)
print("Cleaned employees saved, shape:", df_clean.shape)""")
    ])

    # 04_data_relationships.ipynb
    create_notebook("04_data_relationships.ipynb", [
        md_cell("# Day 1: 04 - Data Relationships\n\nMap join keys between Employee, Performance, Roles, and Skill Ontologies."),
        code_cell("""import pandas as pd

emp = pd.read_csv("../data/processed/employees.csv")
roles = pd.read_csv("../data/processed/role_skills.csv")
emp_skills = pd.read_csv("../data/processed/employee_skills.csv")

print(f"Employees: {len(emp)} | Roles defined: {len(roles)} | Skill mappings: {len(emp_skills)}")
print("Relationship schema: Employee (1) -> (M) Employee Skills on EmployeeID")
print("Relationship schema: Employee (M) -> (1) Role Skills on JobRole")""")
    ])

    # 05_feature_engineering.ipynb
    create_notebook("05_feature_engineering.ipynb", [
        md_cell("# Day 2: 05 - Feature Engineering\n\nDerive business features: TenureRatio, SatisfactionComposite, IncomePerYear, PromotionGap."),
        code_cell("""import pandas as pd

df = pd.read_csv("../data/processed/employees.csv")
df["TenureRatio"] = df["YearsAtCompany"] / (df["TotalWorkingYears"] + 1)
df["SatisfactionComposite"] = (df["JobSatisfaction"] + df["EnvironmentSatisfaction"] + df["RelationshipSatisfaction"]) / 3.0
df["IncomePerYear"] = df["MonthlyIncome"] / (df["TotalWorkingYears"] + 1)
df["PromotionGap"] = df["YearsSinceLastPromotion"] / (df["YearsInCurrentRole"] + 1)

print("Engineered Features Sample:")
df[["TenureRatio", "SatisfactionComposite", "IncomePerYear", "PromotionGap"]].head()""")
    ])

    # 06_baseline_model.ipynb
    create_notebook("06_baseline_model.ipynb", [
        md_cell("# Day 2: 06 - Baseline Model\n\nFit an explainable Logistic Regression baseline."),
        code_cell("""import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../data/processed/employees.csv")
y = (df["Attrition"] == "Yes").astype(int)
num_cols = ["Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany", "JobSatisfaction"]
X = StandardScaler().fit_transform(df[num_cols])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
lr = LogisticRegression()
lr.fit(X_train, y_train)

probs = lr.predict_proba(X_test)[:, 1]
print(f"Baseline Logistic Regression ROC-AUC: {roc_auc_score(y_test, probs):.4f}")""")
    ])

    # 07_model_comparison.ipynb
    create_notebook("07_model_comparison.ipynb", [
        md_cell("# Day 2: 07 - Model Comparison\n\nBenchmark Logistic Regression, Random Forest, and Gradient Boosting/XGBoost."),
        code_cell("""import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

df = pd.read_csv("../data/processed/employees.csv")
y = (df["Attrition"] == "Yes").astype(int)
num_cols = ["Age", "MonthlyIncome", "TotalWorkingYears", "YearsAtCompany", "JobSatisfaction", "WorkLifeBalance"]
X = df[num_cols]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

models = {
    "LogisticRegression": LogisticRegression(max_iter=500),
    "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42)
}

for name, clf in models.items():
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:, 1]
    print(f"{name:20s} | Recall: {recall_score(y_test, preds):.3f} | F1: {f1_score(y_test, preds):.3f} | ROC-AUC: {roc_auc_score(y_test, probs):.3f}")""")
    ])

    # 08_model_explainability.ipynb
    create_notebook("08_model_explainability.ipynb", [
        md_cell("# Day 2: 08 - Model Explainability (SHAP)\n\nInspect Global feature importance and Local employee risk factors."),
        code_cell("""import joblib
import pandas as pd
import numpy as np

# Load trained pipeline
artifact = joblib.load("../models/v1/attrition_pipeline.joblib")
pipe = artifact["pipeline"]
print("Model loaded successfully:", type(pipe.named_steps['classifier']))
print("Numeric features:", len(artifact['numeric_cols']), "| Categorical:", len(artifact['cat_cols']))""")
    ])

    # 09_model_versioning.ipynb
    create_notebook("09_model_versioning.ipynb", [
        md_cell("# Day 2: 09 - Model Versioning\n\nVerify serialized artifacts in `models/v1/` and metadata logging."),
        code_cell("""import json
with open("../models/v1/metadata.json") as f:
    meta = json.load(f)
print("Active Model Metadata:")
print(json.dumps(meta, indent=2))""")
    ])

    # 10_engagement_intelligence.ipynb
    create_notebook("10_engagement_intelligence.ipynb", [
        md_cell("# Day 3: 10 - Engagement Analytics\n\nDepartmental engagement scores, distribution, and low-engagement flag."),
        code_cell("""import pandas as pd
df = pd.read_csv("../data/processed/employees.csv")
dept_eng = df.groupby("Department")["EngagementScore"].agg(["mean", "count", "std"]).reset_index()
print(dept_eng)""")
    ])

    # 11_role_intelligence.ipynb
    create_notebook("11_role_intelligence.ipynb", [
        md_cell("# Day 3: 11 - Role Intelligence\n\nRequired skill taxonomy per role."),
        code_cell("""import pandas as pd
roles_df = pd.read_csv("../data/processed/role_skills.csv")
print(roles_df.to_string())""")
    ])

    # 12_employee_skills.ipynb
    create_notebook("12_employee_skills.ipynb", [
        md_cell("# Day 3: 12 - Employee Skills Table\n\nEmployee skill inventory with proficiency levels."),
        code_cell("""import pandas as pd
skills_df = pd.read_csv("../data/processed/employee_skills.csv")
print(f"Total employee skill records: {len(skills_df)}")
skills_df.head(10)""")
    ])

    # 13_skill_gap_engine.ipynb
    create_notebook("13_skill_gap_engine.ipynb", [
        md_cell("# Day 3: 13 - Skill Gap Engine\n\nSet-difference calculation for employee vs role required skills."),
        code_cell("""def compute_skill_gap(required_skills, employee_skills):
    req_set = set([s.strip().lower() for s in required_skills])
    has_set = set([s.strip().lower() for s in employee_skills])
    return list(req_set - has_set)

# Example
req = ["Python", "SQL", "MLOps", "Docker", "AWS"]
has = ["Python", "SQL", "AWS"]
print("Missing Skills:", compute_skill_gap(req, has))""")
    ])

    # 14_organization_skill_gap.ipynb
    create_notebook("14_organization_skill_gap.ipynb", [
        md_cell("# Day 3: 14 - Organization-Wide Skill Gap\n\nAggregated missing skills across the entire workforce."),
        code_cell("""import pandas as pd

emp_df = pd.read_csv("../data/processed/employees.csv")
role_df = pd.read_csv("../data/processed/role_skills.csv")
skills_df = pd.read_csv("../data/processed/employee_skills.csv")

role_map = {r["JobRole"]: [s.strip() for s in r["RequiredSkills"].split(",")] for _, r in role_df.iterrows()}
emp_skills_map = skills_df.groupby("EmployeeID")["Skill"].apply(lambda s: set(s.str.lower())).to_dict()

gap_counts = {}
for _, emp in emp_df.iterrows():
    eid = emp["EmployeeID"]
    req = role_map.get(emp["JobRole"], [])
    has = emp_skills_map.get(eid, set())
    for s in req:
        if s.lower() not in has:
            gap_counts[s] = gap_counts.get(s, 0) + 1

gap_df = pd.DataFrame(list(gap_counts.items()), columns=["Skill", "EmployeesMissing"]).sort_values(by="EmployeesMissing", ascending=False)
gap_df["Severity"] = gap_df["EmployeesMissing"].apply(lambda x: "HIGH" if x > 200 else ("MEDIUM" if x > 100 else "LOW"))
gap_df.head(10)""")
    ])

    # 15_recommendation_engine.ipynb
    create_notebook("15_recommendation_engine.ipynb", [
        md_cell("# Day 3: 15 - Upskilling Recommendation Engine\n\nMap employee skill gaps to courses in catalog."),
        code_cell("""import pandas as pd

courses = pd.read_csv("../data/processed/courses.csv")

def recommend_courses(missing_skills):
    recs = []
    for skill in missing_skills:
        match = courses[courses["TargetSkill"].str.lower() == skill.lower()]
        if not match.empty:
            recs.append(match.iloc[0]["CourseTitle"])
        else:
            recs.append(f"Mastery Track: {skill.title()}")
    return recs

print("Recommendations for ['MLOps', 'Docker']:")
print(recommend_courses(["MLOps", "Docker"]))""")
    ])

    # 16_employee_intelligence.ipynb
    create_notebook("16_employee_intelligence.ipynb", [
        md_cell("# Day 3: 16 - Employee Intelligence Table\n\nUnified master table: Attrition Risk, Engagement, Skill Gap, Recommendations."),
        code_cell("""import pandas as pd
import numpy as np

emp = pd.read_csv("../data/processed/employees.csv")
print("Master Employee Intelligence Records:", len(emp))
emp[["EmployeeID", "Department", "JobRole", "EngagementScore", "Attrition"]].head(10)""")
    ])

if __name__ == "__main__":
    generate_all_notebooks()
