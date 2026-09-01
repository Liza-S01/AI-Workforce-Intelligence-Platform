"""
Data Setup & Preprocessing Script for Enterprise HR AI Platform.
Copies raw files, processes them, generates skill mappings, courses, policies, and resumes.
"""
import os
import shutil
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATASET_SRC = os.path.join(BASE_DIR, "dataset")

RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
POLICIES_DIR = os.path.join(DATA_DIR, "hr_policies")
RESUMES_DIR = os.path.join(DATA_DIR, "resumes")
JOB_DESC_DIR = os.path.join(DATA_DIR, "job_descriptions")
PREDICTIONS_DIR = os.path.join(DATA_DIR, "predictions")
MODELS_DIR = os.path.join(BASE_DIR, "models", "v1")

for d in [RAW_DIR, PROCESSED_DIR, POLICIES_DIR, RESUMES_DIR, JOB_DESC_DIR, PREDICTIONS_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

def setup_raw_data():
    print("-> Setting up Raw Data...")
    src_raw_map = {
        "employee_attrition.csv": "employee_attrition.csv",
        "employee_performance_pro.csv": "hr_performance_engagement.csv",
        "occupation_data.csv": "occupation_data.csv",
        "essential_skills.csv": "essential_skills.csv",
        "software_skills.csv": "software_skills.csv",
    }
    for src, dst in src_raw_map.items():
        src_path = os.path.join(DATASET_SRC, src)
        dst_path = os.path.join(RAW_DIR, dst)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"   Copied {src} -> raw/{dst}")
        else:
            print(f"   Warning: {src_path} not found!")

def process_data():
    print("-> Processing Datasets...")
    attrition_df = pd.read_csv(os.path.join(RAW_DIR, "employee_attrition.csv"))
    
    # 1. Employees Master Table (data/processed/employees.csv)
    # Ensure standard column names and unique IDs
    if "EmployeeNumber" in attrition_df.columns:
        attrition_df["EmployeeID"] = attrition_df["EmployeeNumber"]
    elif "EmployeeID" not in attrition_df.columns:
        attrition_df["EmployeeID"] = range(101, 101 + len(attrition_df))
    
    # Map roles cleanly
    role_map = {
        "Sales Executive": "Sales Executive",
        "Research Scientist": "Research Scientist",
        "Laboratory Technician": "Lab Technician",
        "Manufacturing Director": "Manufacturing Director",
        "Healthcare Representative": "Healthcare Rep",
        "Manager": "Engineering Manager",
        "Sales Representative": "Sales Rep",
        "Research Director": "Research Director",
        "Human Resources": "HR Specialist"
    }
    attrition_df["JobRoleStandard"] = attrition_df["JobRole"].map(lambda x: role_map.get(x, x))
    
    # Add synthetic engagement metrics if not present
    np.random.seed(42)
    attrition_df["EngagementScore"] = np.clip(
        (attrition_df["JobSatisfaction"] * 18 + attrition_df["WorkLifeBalance"] * 10 + np.random.randint(10, 25, len(attrition_df))),
        35, 98
    )
    
    attrition_df.to_csv(os.path.join(PROCESSED_DIR, "employees.csv"), index=False)
    print(f"   Created processed/employees.csv ({len(attrition_df)} records)")

    # 2. Role Skills Master (data/processed/role_skills.csv)
    role_skills_data = [
        # Research Scientist / Data / ML
        {"JobRole": "Research Scientist", "RequiredSkills": "Python, Machine Learning, Statistics, Deep Learning, SQL, Data Visualization", "Domain": "AI & Data"},
        {"JobRole": "Data Analyst", "RequiredSkills": "SQL, Python, PowerBI, Excel, Statistics, Tableau, Data Cleaning", "Domain": "AI & Data"},
        {"JobRole": "ML Engineer", "RequiredSkills": "Python, MLOps, Docker, AWS, PyTorch, Kubernetes, Feature Engineering", "Domain": "Engineering"},
        {"JobRole": "Backend Engineer", "RequiredSkills": "Python, FastAPI, PostgreSQL, Docker, Redis, CI/CD, Git", "Domain": "Engineering"},
        {"JobRole": "Sales Executive", "RequiredSkills": "B2B Sales, CRM, Negotiation, Market Analysis, Account Management, Communication", "Domain": "Sales"},
        {"JobRole": "Sales Rep", "RequiredSkills": "Lead Generation, Customer Relationship, Product Demos, Cold Calling, CRM", "Domain": "Sales"},
        {"JobRole": "Lab Technician", "RequiredSkills": "Quality Assurance, Equipment Calibration, Lab Safety, Data Recording, SOP Compliance", "Domain": "Operations"},
        {"JobRole": "Manufacturing Director", "RequiredSkills": "Lean Manufacturing, Supply Chain, Six Sigma, Budgeting, Plant Management", "Domain": "Operations"},
        {"JobRole": "Healthcare Rep", "RequiredSkills": "Medical Terminology, Regulatory Compliance, Client Advisory, Healthcare Ethics", "Domain": "Healthcare"},
        {"JobRole": "Engineering Manager", "RequiredSkills": "Agile Leadership, Project Management, System Architecture, Mentorship, Resource Allocation", "Domain": "Management"},
        {"JobRole": "HR Specialist", "RequiredSkills": "Talent Acquisition, Employee Relations, HR Policies, Payroll Systems, Conflict Resolution", "Domain": "Human Resources"}
    ]
    role_skills_df = pd.DataFrame(role_skills_data)
    role_skills_df.to_csv(os.path.join(PROCESSED_DIR, "role_skills.csv"), index=False)
    print(f"   Created processed/role_skills.csv")

    # 3. Employee Skills Inventory (data/processed/employee_skills.csv)
    # Generate realistic skill portfolios with deliberate gaps for demonstration
    emp_skills_list = []
    
    role_skill_lookup = {row["JobRole"]: [s.strip() for s in row["RequiredSkills"].split(",")] for _, row in role_skills_df.iterrows()}
    # Fallback pool
    tech_pool = ["Python", "SQL", "Excel", "Git", "PowerBI", "Communication", "Data Analysis", "AWS", "Docker", "MLOps", "Statistics"]

    for _, emp in attrition_df.iterrows():
        eid = emp["EmployeeID"]
        role = emp["JobRole"]
        req_skills = role_skill_lookup.get(role, tech_pool[:5])
        
        # Give employee a subset of required skills + some random general skills
        num_known = max(2, int(len(req_skills) * (0.5 + 0.5 * (emp["JobSatisfaction"] / 4.0))))
        known_required = np.random.choice(req_skills, size=min(num_known, len(req_skills)), replace=False).tolist()
        
        # Add 1-2 additional skills
        additional = np.random.choice(tech_pool, size=np.random.randint(1, 3), replace=False).tolist()
        all_emp_skills = list(set(known_required + additional))
        
        for sk in all_emp_skills:
            emp_skills_list.append({
                "EmployeeID": eid,
                "Skill": sk,
                "ProficiencyLevel": np.random.choice(["Beginner", "Intermediate", "Advanced"], p=[0.25, 0.55, 0.20]),
                "LastAssessed": "2026-03-15"
            })
            
    emp_skills_df = pd.DataFrame(emp_skills_list)
    emp_skills_df.to_csv(os.path.join(PROCESSED_DIR, "employee_skills.csv"), index=False)
    print(f"   Created processed/employee_skills.csv ({len(emp_skills_df)} skill entries)")

    # 4. Upskilling Course Catalog (data/processed/courses.csv)
    courses_data = [
        {"CourseID": "CRS-101", "CourseTitle": "Production MLOps with Docker & Kubernetes", "TargetSkill": "MLOps", "Category": "Engineering", "DurationHours": 24, "Provider": "DeepLearning.AI", "Level": "Advanced"},
        {"CourseID": "CRS-102", "CourseTitle": "AWS Certified Machine Learning & Cloud Architect", "TargetSkill": "AWS", "Category": "Cloud", "DurationHours": 32, "Provider": "Amazon Web Services", "Level": "Intermediate"},
        {"CourseID": "CRS-103", "CourseTitle": "Generative AI and Large Language Model Deployment", "TargetSkill": "Generative AI", "Category": "AI & Data", "DurationHours": 18, "Provider": "Google Cloud Skills", "Level": "Advanced"},
        {"CourseID": "CRS-104", "CourseTitle": "Advanced SQL & Modern Data Warehousing", "TargetSkill": "SQL", "Category": "AI & Data", "DurationHours": 16, "Provider": "Coursera", "Level": "Intermediate"},
        {"CourseID": "CRS-105", "CourseTitle": "Docker Containers for Microservices & Python Apps", "TargetSkill": "Docker", "Category": "Engineering", "DurationHours": 14, "Provider": "Linux Foundation", "Level": "Beginner"},
        {"CourseID": "CRS-106", "CourseTitle": "Executive Leadership, Agile & Change Management", "TargetSkill": "Agile Leadership", "Category": "Management", "DurationHours": 20, "Provider": "Harvard Online", "Level": "Executive"},
        {"CourseID": "CRS-107", "CourseTitle": "PowerBI & Interactive Business Analytics", "TargetSkill": "PowerBI", "Category": "AI & Data", "DurationHours": 12, "Provider": "Microsoft Learn", "Level": "Intermediate"},
        {"CourseID": "CRS-108", "CourseTitle": "Strategic Enterprise B2B Sales & Negotiation", "TargetSkill": "B2B Sales", "Category": "Sales", "DurationHours": 15, "Provider": "Salesforce Academy", "Level": "Advanced"},
        {"CourseID": "CRS-109", "CourseTitle": "FastAPI Masterclass: Building Async Microservices", "TargetSkill": "FastAPI", "Category": "Engineering", "DurationHours": 16, "Provider": "TestDriven.io", "Level": "Intermediate"},
        {"CourseID": "CRS-110", "CourseTitle": "Lean Six Sigma Black Belt: Operational Excellence", "TargetSkill": "Lean Manufacturing", "Category": "Operations", "DurationHours": 40, "Provider": "ASQ", "Level": "Advanced"}
    ]
    courses_df = pd.DataFrame(courses_data)
    courses_df.to_csv(os.path.join(PROCESSED_DIR, "courses.csv"), index=False)
    print(f"   Created processed/courses.csv")

    # 5. Performance History & Engagement data
    perf_list = []
    for _, emp in attrition_df.iterrows():
        eid = emp["EmployeeID"]
        for year in [2024, 2025, 2026]:
            score = max(1, min(5, int(emp["PerformanceRating"]) + np.random.choice([-1, 0, 0, 1])))
            perf_list.append({
                "EmployeeID": eid,
                "Year": year,
                "PerformanceRating": score,
                "GoalsAchieved": f"{np.random.randint(70, 100)}%",
                "ReviewerNotes": "Consistent delivery with focus on key deliverables." if score >= 3 else "Needs improvement in deadlines and upskilling."
            })
    pd.DataFrame(perf_list).to_csv(os.path.join(PROCESSED_DIR, "performance_history.csv"), index=False)
    
    eng_df = attrition_df[["EmployeeID", "Department", "JobRole", "EngagementScore", "JobSatisfaction", "WorkLifeBalance"]].copy()
    eng_df["EngagementCategory"] = pd.cut(eng_df["EngagementScore"], bins=[0, 50, 75, 100], labels=["Low", "Medium", "High"])
    eng_df.to_csv(os.path.join(PROCESSED_DIR, "engagement_data.csv"), index=False)
    print(f"   Created processed/performance_history.csv & engagement_data.csv")

def generate_documents():
    print("-> Generating HR Policy PDFs, Candidate Resumes, and Job Descriptions...")
    
    # 1. Job descriptions
    jds = {
        "ml_engineer.txt": """Position: Machine Learning Engineer
Department: Engineering / AI Labs
Location: Hybrid / Remote

Key Responsibilities:
- Design, train, and deploy production machine learning and deep learning pipelines.
- Implement MLOps best practices with Docker, Kubernetes, MLflow, and CI/CD.
- Architect high-throughput inference APIs using FastAPI and PyTorch.
- Optimize feature stores, vector databases, and real-time streaming data.

Required Qualifications:
- 3+ years experience with Python, PyTorch/TensorFlow, and Scikit-Learn.
- Strong knowledge of MLOps, Containerization (Docker), AWS/GCP cloud platforms.
- Experience building RESTful APIs with FastAPI or Flask.
- BS/MS in Computer Science, Data Science, or related engineering discipline.
""",
        "data_analyst.txt": """Position: Senior Data Analyst
Department: Business Intelligence
Location: Bangalore / Hybrid

Key Responsibilities:
- Extract, transform, and analyze complex enterprise datasets using SQL and Python.
- Design interactive executive dashboards and KPI scorecards in PowerBI and Tableau.
- Perform exploratory data analysis (EDA), cohort analysis, and retention metrics.
- Translate business requirements into actionable data models and stakeholder reports.

Required Qualifications:
- 3+ years of expertise in SQL queries, PostgreSQL, and Data Modeling.
- Proficiency in Python (Pandas, NumPy, Matplotlib) and PowerBI.
- Strong communication and statistical hypothesis testing skills.
""",
        "backend_engineer.txt": """Position: Senior Backend Engineer
Department: Core Engineering
Location: Remote

Key Responsibilities:
- Build robust, scalable, async backend microservices using Python and FastAPI.
- Design relational schemas in PostgreSQL and caching layers with Redis.
- Maintain CI/CD pipelines, container orchestration, and automated pytest suites.
- Integrate third-party AI APIs, authentication mechanisms, and event queues.

Required Qualifications:
- 4+ years of backend development in Python, FastAPI/Django, and PostgreSQL.
- Solid understanding of distributed systems, REST APIs, Docker, and Git.
"""
    }
    for filename, content in jds.items():
        with open(os.path.join(JOB_DESC_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   Created job_descriptions/{filename}")

    # 2. Resumes
    resumes = {
        "candidate_001.txt": """CANDIDATE: Alex Rivera
TITLE: Machine Learning & MLOps Engineer
EMAIL: alex.rivera@example.com | GITHUB: github.com/alexrivera-ml

SUMMARY:
Results-driven Machine Learning Engineer with 4 years of experience building and deploying end-to-end ML and deep learning models to production. Specialized in MLOps, PyTorch, Docker, Kubernetes, AWS, and FastAPI microservices.

SKILLS:
- Languages & Frameworks: Python, PyTorch, Scikit-Learn, FastAPI, SQL, Bash
- MLOps & DevOps: Docker, Kubernetes, MLflow, AWS (SageMaker, S3, EC2), CI/CD, Git
- Data Engineering: Pandas, Spark, Redis, PostgreSQL

EXPERIENCE:
- Senior ML Engineer at TechCorp (2023 - Present):
  Deployed production LLM fine-tuning pipelines and real-time fraud detection systems. Reduced inference latency by 45% using TorchScript and Docker containerization.
- Machine Learning Developer at DataFlow Inc (2021 - 2023):
  Built computer vision and tabular classification models. Automated MLOps tracking with MLflow.

EDUCATION:
- B.S. in Computer Science, University of California (2021)
""",
        "candidate_002.txt": """CANDIDATE: Sarah Chen
TITLE: Senior Business Intelligence & Data Analyst
EMAIL: sarah.chen@example.com

SUMMARY:
Data Analyst with 5+ years of experience delivering actionable business intelligence, customer lifetime value analytics, and executive dashboards across retail and fintech sectors.

SKILLS:
- Analytics & BI: PowerBI, Tableau, Advanced Excel, Looker, Statistical Analysis
- Programming & Databases: SQL (PostgreSQL, MySQL, Snowflake), Python (Pandas, Seaborn), R
- Business Strategy: A/B Testing, Cohort Analysis, KPI Definition, Stakeholder Management

EXPERIENCE:
- Lead BI Analyst at RetailHub (2022 - Present):
  Built cross-functional dashboards in PowerBI used by 200+ managers. Optimized complex SQL queries saving 12 hours of report generation weekly.
- Data Analyst at FinMetrics (2019 - 2022):
  Conducted exploratory data analysis on 5M+ transactions, identifying churn drivers.

EDUCATION:
- M.S. in Business Analytics, NYU (2019)
""",
        "candidate_003.txt": """CANDIDATE: Marcus Vance
TITLE: Backend & Cloud Software Engineer
EMAIL: marcus.vance@example.com

SUMMARY:
Software Engineer with 4 years experience architecting resilient REST APIs, microservices, and asynchronous background pipelines using Python, FastAPI, PostgreSQL, Redis, and Docker.

SKILLS:
- Core Tech: Python, FastAPI, Django, PostgreSQL, Redis, SQLAlchemy, Pydantic
- Cloud & Infrastructure: Docker, AWS (ECS, RDS, S3), Git, CI/CD GitHub Actions, Linux
- Architecture: Microservices, Distributed Systems, Unit Testing (Pytest), JWT Auth

EXPERIENCE:
- Backend Engineer at CloudScale Solutions (2022 - Present):
  Designed high-concurrency FastAPI microservices handling 15k requests/sec. Maintained automated pytest suite with 92% coverage.
- Software Developer at AppCraft (2020 - 2022):
  Developed REST APIs and managed PostgreSQL database migrations.

EDUCATION:
- B.Tech in Information Technology (2020)
"""
    }
    for filename, content in resumes.items():
        with open(os.path.join(RESUMES_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   Created resumes/{filename}")

    # Generate PDFs if reportlab is available
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        # Policy PDFs
        policies = {
            "leave_policy.pdf": ("Enterprise Leave & Time-Off Policy", [
                "1. Annual Paid Time Off: All full-time employees accrue 20 days of paid vacation per year.",
                "2. Sick & Wellness Leave: Up to 10 days of paid sick leave per year, requiring medical cert after 3 consecutive days.",
                "3. Parental Leave: 16 weeks of fully paid parental leave for primary caregivers, 6 weeks for secondary caregivers.",
                "4. Carry-Over Rules: A maximum of 5 unused vacation days can be carried forward into the next calendar year.",
                "5. Leave Request Procedure: Requests must be submitted via the HRMS portal at least 2 weeks in advance."
            ]),
            "remote_work_policy.pdf": ("Enterprise Remote & Hybrid Work Guidelines", [
                "1. Hybrid Schedule: Eligible employees may work remotely up to 3 days per week with manager approval.",
                "2. Core Collaboration Hours: Teams must be reachable and active between 10:00 AM and 4:00 PM local time.",
                "3. Home Office Equipment: One-time home office stipend of $750 provided upon successful onboarding.",
                "4. Cybersecurity & VPN: All remote access must use company-issued VPN and two-factor authentication (2FA).",
                "5. Workspace Ergonomics: Employees are responsible for maintaining a safe and dedicated work environment."
            ]),
            "payroll_policy.pdf": ("Enterprise Compensation, Payroll & Benefits Policy", [
                "1. Pay Frequency: Salaries are disbursed on the 28th day of each calendar month via direct bank deposit.",
                "2. Performance Bonuses: Annual bonuses are evaluated in Q4 based on company performance and individual ratings.",
                "3. Overtime Policy: Non-exempt employees receive 1.5x standard hourly rate for hours exceeding 40 per week.",
                "4. Health & Wellness Insurance: Comprehensive medical, dental, and vision coverage funded 90% by the employer.",
                "5. Expense Reimbursement: Business-related expenses must be submitted with receipts within 30 days."
            ]),
            "learning_policy.pdf": ("Enterprise Learning & Professional Development Policy", [
                "1. Annual Learning Budget: Every full-time employee receives $2,000 annually for approved courses and certifications.",
                "2. Skill Gap Upskilling: Priority sponsorship is given to strategic focus areas (MLOps, Cloud, GenAI, Leadership).",
                "3. Certification Reimbursement: Exam fees for approved industry certifications (AWS, PMP, CKAD) reimbursed 100% upon passing.",
                "4. Dedicated Learning Hours: Up to 4 hours per week during normal business hours may be dedicated to approved training.",
                "5. Knowledge Sharing: Employees completing sponsored courses are encouraged to conduct internal lunch-and-learn sessions."
            ])
        }
        for pdf_name, (title, clauses) in policies.items():
            pdf_path = os.path.join(POLICIES_DIR, pdf_name)
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, title)
            c.setFont("Helvetica", 10)
            c.drawString(50, 730, "Document Version 2.4 | Classification: Internal HR Document | Updated: 2026")
            c.line(50, 720, 560, 720)
            
            y = 690
            c.setFont("Helvetica", 11)
            for clause in clauses:
                c.drawString(50, y, clause)
                y -= 30
            c.save()
            print(f"   Generated PDF hr_policies/{pdf_name}")
            
        # Also generate PDF versions of candidate resumes
        for res_name, text in resumes.items():
            pdf_name = res_name.replace(".txt", ".pdf")
            pdf_path = os.path.join(RESUMES_DIR, pdf_name)
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 14)
            lines = text.split("\n")
            y = 750
            for line in lines:
                if line.startswith("CANDIDATE:") or line.startswith("SUMMARY:") or line.startswith("SKILLS:") or line.startswith("EXPERIENCE:") or line.startswith("EDUCATION:"):
                    c.setFont("Helvetica-Bold", 11)
                else:
                    c.setFont("Helvetica", 9)
                c.drawString(50, y, line[:90])
                y -= 14
                if y < 50:
                    break
            c.save()
            print(f"   Generated PDF resumes/{pdf_name}")
            
    except Exception as e:
        print(f"   Note: ReportLab PDF generation notice: {e}. Text versions exist.")

if __name__ == "__main__":
    setup_raw_data()
    process_data()
    generate_documents()
    print("\n-> Data Setup Completed Successfully!")
