from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Tuple
import requests
import re

app = FastAPI()

class LlamaRecommender:
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        print(f"Using Ollama model: {model_name}")

    def _generate_recommendation_prompt(self, job_info: Dict, candidate_info: Dict) -> str:
        return f"""You are an expert AI system for job candidate recommendations.

Job Information:
- Job Title: {job_info.get('title')}
- Required Skills: {', '.join(job_info.get('required_skills', []))}
- Job Description: {job_info.get('description')}

Candidate Profile:
- Name: {candidate_info.get('full_name')}
- Skills: {', '.join(candidate_info.get('skills', []))}
- Experience: {candidate_info.get('experience')}
- Education: {candidate_info.get('education')}

Recommendation Task:
Please assess whether this candidate is a good fit for the job. Provide a recommendation based on the candidate’s skills, experience, and education in relation to the job.

Match Score:
- Provide a numeric score between 0 and 10 based on how well the candidate matches the job.

Explanation:
- Provide a brief, clear explanation of why or why not the candidate is a good fit for the job. Include strengths and weaknesses, and highlight any potential skills or experience gaps.

Format your response like this:
Score: [number]
Explanation: [reason]
"""

    def get_match_score_and_recommendation(self, job_info: Dict, candidate_info: Dict) -> Tuple[float, str]:
        prompt = self._generate_recommendation_prompt(job_info, candidate_info)
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_predict": 512,
                        "stop": ["Score:", "Explanation:"]
                    }
                },
                timeout=30
            )
            result = response.json()
            response_text = result.get('response', '')

            score_match = re.search(r"Score:\s*([0-9]+(?:\.[0-9]+)?)", response_text)
            explanation_match = re.search(r"Explanation:\s*(.*)", response_text, re.DOTALL)

            score = float(score_match.group(1)) if score_match else 0.0
            explanation = explanation_match.group(1).strip() if explanation_match else "No explanation found."

            return score, explanation

        except Exception as e:
            return 0.0, f"Error: {str(e)}"

    def get_job_candidate_matches(self, job_info: Dict, candidates: List[Dict]) -> List[Dict]:
        matches = []
        for candidate in candidates:
            score, explanation = self.get_match_score_and_recommendation(job_info, candidate)
            matches.append({
                "candidate_id": candidate.get("_id", ""),
                "match_score": score,
                "explanation": explanation
            })
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)

class JobInfo(BaseModel):
    title: str
    required_skills: List[str]
    description: str

class CandidateInfo(BaseModel):
    _id: str
    full_name: str
    skills: List[str]
    experience: str
    education: str

class MatchRequest(BaseModel):
    job: JobInfo
    candidate: CandidateInfo

@app.post("/recommend")
def recommend(request: MatchRequest):
    recommender = LlamaRecommender()  # Instantiate the recommender
    score, explanation = recommender.get_match_score_and_recommendation(request.job.dict(), request.candidate.dict())
    return {"match_score": score, "explanation": explanation}
