from typing import List, Dict, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import time
import re

app = FastAPI()

class LlamaRecommender:
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_available = True
        print(f"Using Ollama model: {model_name}")

        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                if not any(model["name"] == model_name for model in models):
                    print(f"Warning: Model {model_name} not found. Available models: {[m['name'] for m in models]}")
            else:
                print("Warning: Could not verify available models")
                self.ollama_available = False
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to Ollama. Will use fallback scoring mechanism.")
            self.ollama_available = False

    def _generate_prompt(self, job_info: Dict, candidate_info: Dict) -> str:
        prompt = f"""You are an expert AI job matching system. Your task is to evaluate how well this candidate matches the job requirements.

Job Details:
Title: {job_info.get('title', 'N/A')}
Required Skills: {', '.join(job_info.get('required_skills', []))}
Description: {job_info.get('description', 'N/A')}

Candidate Profile:
Name: {candidate_info.get('full_name', 'N/A')}
Skills: {', '.join(candidate_info.get('skills', []))}
Experience: {candidate_info.get('experience', 'N/A')}
Education: {candidate_info.get('education', 'N/A')}

Please analyze the match between this candidate and job position. Consider:
1. Skill match (both technical and soft skills)
2. Experience relevance
3. Education alignment
4. Overall fit for the role

Evaluate the match on a scale of 0-100, where:
0 = No match at all
25 = Poor match
50 = Moderate match
75 = Good match
100 = Perfect match

Provide your evaluation in the following format:
Score: [number]
Explanation: [detailed explanation of the match, including specific strengths and gaps]

Your evaluation:"""
        return prompt

    def get_match_score(self, job_info: Dict, candidate_info: Dict) -> Tuple[float, str]:
        if not self.ollama_available:
            # Fallback mechanism when Ollama is not available
            return self._calculate_fallback_score(job_info, candidate_info)
            
        prompt = self._generate_prompt(job_info, candidate_info)

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
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
                response.raise_for_status()
                result = response.json()
                response_text = result.get('response', '')

                score = 0.0
                explanation = "Error processing Ollama response"
                score_match = re.search(r"Score:\s*([0-9]+(?:\.[0-9]+)?)", response_text)
                explanation_match = re.search(r"Explanation:\s*(.*)", response_text, re.DOTALL)
                if score_match:
                    score = float(score_match.group(1))
                if explanation_match:
                    explanation = explanation_match.group(1).strip()

                return score, explanation

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error calling Ollama after {max_retries} attempts: {str(e)}")
                    self.ollama_available = False
                    return self._calculate_fallback_score(job_info, candidate_info)

    def _calculate_fallback_score(self, job_info: Dict, candidate_info: Dict) -> Tuple[float, str]:
        """Simple keyword matching algorithm as a fallback when Ollama is not available"""
        job_requirements = set(job_info.get("requirements", []))
        if not job_requirements and "required_skills" in job_info:
            job_requirements = set(job_info.get("required_skills", []))
            
        candidate_skills = set(candidate_info.get("skills", []))
        
        # Calculate skill match percentage
        if not job_requirements:
            skill_match = 50.0  # Default if no requirements specified
        else:
            matched_skills = job_requirements.intersection(candidate_skills)
            skill_match = (len(matched_skills) / len(job_requirements)) * 100
        
        # Add location match bonus
        location_match = 0
        if job_info.get("location") == candidate_info.get("location"):
            location_match = 10
        
        # Create explanation
        explanation = f"Keyword match algorithm (fallback): Found {len(job_requirements.intersection(candidate_skills))} matching skills out of {len(job_requirements)} required skills."
        
        # Simple score calculation (primarily based on matching skills)
        score = min(100, skill_match + location_match)
        
        return score, explanation

    def get_job_candidate_matches(self, job_info: Dict, candidates: List[Dict]) -> List[Dict]:
        matches = []
        for candidate in candidates:
            candidate_id = candidate.get("id") if "id" in candidate else str(candidate.get("_id", "unknown"))
            score, explanation = self.get_match_score(job_info, candidate)
            matches.append({
                "candidate_id": candidate_id,
                "match_score": score,
                "explanation": explanation
            })
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)

# -----------------------------
# FastAPI Integration
# -----------------------------

recommender = LlamaRecommender()

class Job(BaseModel):
    title: str
    required_skills: List[str]
    description: str

class Candidate(BaseModel):
    _id: str
    full_name: str
    skills: List[str]
    experience: str
    education: str

class MatchRequest(BaseModel):
    job: Job
    candidate: Candidate

class BulkMatchRequest(BaseModel):
    job: Job
    candidates: List[Candidate]

@app.post("/match")
def match_candidate(request: MatchRequest):
    score, explanation = recommender.get_match_score(request.job.dict(), request.candidate.dict())
    return {"match_score": score, "explanation": explanation}

@app.post("/bulk_match")
def bulk_match_candidates(request: BulkMatchRequest):
    results = recommender.get_job_candidate_matches(request.job.dict(), [c.dict() for c in request.candidates])
    return results
