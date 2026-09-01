from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_dashboard_summary_endpoint():
    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_employees" in data
    assert "high_risk_employees" in data
    assert "average_engagement" in data

def test_employee_profile_endpoint():
    response = client.get("/employees/101")
    assert response.status_code == 200
    data = response.json()
    assert "EmployeeID" in data
    assert "JobRole" in data

def test_attrition_prediction_endpoint():
    payload = {
        "EmployeeID": 105,
        "Age": 29,
        "Department": "Research & Development",
        "JobRole": "Research Scientist",
        "MonthlyIncome": 4500.0,
        "TotalWorkingYears": 6,
        "YearsAtCompany": 3,
        "YearsInCurrentRole": 2,
        "OverTime": "No",
        "JobSatisfaction": 3,
        "WorkLifeBalance": 3
    }
    response = client.post("/predict/attrition", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "AttritionProbability" in data
    assert "RiskLevel" in data

def test_policy_qa_endpoint():
    payload = {"query": "How many days of paid vacation do I get?"}
    response = client.post("/nlp/policy-qa", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["sources"]) > 0

def test_resume_matching_endpoint():
    payload = {"target_role": "ml_engineer"}
    response = client.post("/nlp/match-resumes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_agent_orchestrator_routing():
    queries = [
        ("Who is at risk of quitting in Sales?", "ATTRITION_AGENT"),
        ("What courses should employees take for MLOps?", "SKILL_GAP_AGENT"),
        ("What is the remote work policy?", "POLICY_RAG_AGENT"),
        ("Match candidate resumes for ML Engineer", "RESUME_MATCHING_AGENT")
    ]
    for q, expected_agent in queries:
        resp = client.post("/agent/query", json={"query": q})
        assert resp.status_code == 200
        result = resp.json()
        assert result["routed_agent"] == expected_agent
        assert len(result["thought_trace"]) > 0
