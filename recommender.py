from typing import List, Dict, Tuple

class RecommenderSystem:
    def __init__(self):
        pass

    def _generate_explanation(self, candidate_info: Dict, job_info: Dict, match_score: float) -> str:
        candidate_skills = set(candidate_info.get('skills', []))
        job_requirements = set(job_info.get('requirements', []))
        common_skills = candidate_skills.intersection(job_requirements)
        
        if match_score > 70:
            return f"Strong match! Candidate has {len(common_skills)} matching skills: {', '.join(common_skills)}"
        elif match_score > 40:
            return f"Moderate match. Candidate has {len(common_skills)} matching skills: {', '.join(common_skills)}"
        else:
            return f"Low match. Candidate has {len(common_skills)} matching skills: {', '.join(common_skills)}"

    def get_candidate_job_match(self, candidate_info: Dict, job_info: Dict) -> Tuple[float, str]:
        # Use simple skill matching
        candidate_skills = set(candidate_info.get('skills', []))
        job_requirements = set(job_info.get('requirements', []))
        common_skills = candidate_skills.intersection(job_requirements)
        
        if not job_requirements:
            match_percentage = 0
        else:
            match_percentage = round(len(common_skills) / len(job_requirements) * 100, 2)
        
        explanation = self._generate_explanation(candidate_info, job_info, match_percentage)
        return match_percentage, explanation

    def get_job_candidate_matches(self, job_info: Dict, candidates: List[Dict]) -> List[Dict]:
        matches = []
        for candidate in candidates:
            match_score, explanation = self.get_candidate_job_match(candidate, job_info)
            matches.append({
                "candidate_id": str(candidate["_id"]),  # Convert ObjectId to string
                "match_score": match_score,
                "explanation": explanation
            })
        
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)

    def get_candidate_job_matches(self, candidate_info: Dict, jobs: List[Dict]) -> List[Dict]:
        matches = []
        for job in jobs:
            match_score, explanation = self.get_candidate_job_match(candidate_info, job)
            matches.append({
                "job_id": job["id"],
                "match_score": match_score,
                "explanation": explanation
            })
        
        return sorted(matches, key=lambda x: x["match_score"], reverse=True) 