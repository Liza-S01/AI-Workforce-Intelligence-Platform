import os
import re
from app.utils.config import RESUMES_DIR, JOB_DESC_DIR
from app.utils.logger import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatchingService:
    def __init__(self):
        pass

    def _read_file_text(self, filepath: str) -> str:
        if filepath.endswith(".pdf"):
            try:
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                return " ".join([page.extract_text() or "" for page in reader.pages])
            except Exception as e:
                logger.warning(f"Error reading resume PDF {filepath}: {e}")
                return ""
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()

    def get_job_descriptions(self) -> dict:
        jds = {}
        if os.path.exists(JOB_DESC_DIR):
            for fname in os.listdir(JOB_DESC_DIR):
                if fname.endswith(".txt"):
                    role_key = fname.replace(".txt", "")
                    with open(os.path.join(JOB_DESC_DIR, fname), "r", encoding="utf-8") as f:
                        jds[role_key] = f.read()
        return jds

    def get_available_candidates(self) -> list:
        candidates = []
        if os.path.exists(RESUMES_DIR):
            for fname in sorted(os.listdir(RESUMES_DIR)):
                if fname.endswith(".txt") or fname.endswith(".pdf"):
                    cid = fname.split(".")[0]
                    text = self._read_file_text(os.path.join(RESUMES_DIR, fname))
                    
                    # Extract name from text
                    name_match = re.search(r"CANDIDATE:\s*([^\n]+)", text, re.IGNORECASE)
                    cname = name_match.group(1).strip() if name_match else cid.replace("_", " ").title()
                    
                    candidates.append({
                        "id": cid,
                        "filename": fname,
                        "name": cname,
                        "text": text
                    })
        return candidates

    def match_candidates_to_role(self, role_name: str) -> list:
        role_key = role_name.lower().replace(" ", "_")
        jds = self.get_job_descriptions()
        jd_text = jds.get(role_key, "")
        
        # If exact file not found, use first JD or generate representative text
        if not jd_text and jds:
            jd_text = list(jds.values())[0]

        candidates = self.get_available_candidates()
        if not candidates:
            return []

        # Target role skill keyword sets
        skills_by_role = {
            "ml_engineer": ["Python", "PyTorch", "MLOps", "Docker", "Kubernetes", "AWS", "FastAPI", "TensorFlow"],
            "data_analyst": ["SQL", "PowerBI", "Tableau", "Python", "Excel", "Statistics", "Data Analysis"],
            "backend_engineer": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "CI/CD", "Git", "Microservices"]
        }
        role_skills = skills_by_role.get(role_key, ["Python", "SQL", "Docker", "Git", "Communication"])

        results = []
        for cand in candidates:
            cand_text = cand["text"]
            
            # TF-IDF similarity
            tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            try:
                matrix = tfidf.fit_transform([jd_text, cand_text])
                sim = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
            except Exception:
                sim = 0.5

            # Skill presence check
            matched = [s for s in role_skills if re.search(rf"\b{re.escape(s)}\b", cand_text, re.IGNORECASE)]
            missing = [s for s in role_skills if s not in matched]

            # Weighted final score
            skill_ratio = len(matched) / max(1, len(role_skills))
            final_score = round((sim * 0.4 + skill_ratio * 0.6) * 100, 1)

            if final_score >= 75:
                rec = "Strong Match — Recommend for Interview"
            elif final_score >= 50:
                rec = "Moderate Match — Potential with Upskilling"
            else:
                rec = "Low Fit for Target Role"

            results.append({
                "candidate_id": cand["id"],
                "candidate_name": cand["name"],
                "match_score": final_score,
                "matched_skills": matched,
                "missing_skills": missing,
                "recommendation": rec
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results

resume_service = ResumeMatchingService()
