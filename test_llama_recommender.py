from llama_recommender import LlamaRecommender
import json

def test_llama_recommender():
    print("\nTesting Llama Recommender Integration...")
    
    # Initialize the recommender
    recommender = LlamaRecommender()
    
    # Sample job data
    job_info = {
        "title": "Senior Python Developer",
        "required_skills": ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],
        "description": "We are looking for a Senior Python Developer with experience in building scalable web applications. The ideal candidate should have strong experience with FastAPI, MongoDB, and cloud services.",
        "location": "Remote",
        "salary_range": "$120,000 - $150,000"
    }
    
    # Sample candidates
    candidates = [
        {
            "_id": "1",
            "full_name": "John Doe",
            "skills": ["Python", "FastAPI", "MongoDB", "Docker", "AWS", "React"],
            "experience": "5 years of experience in full-stack development with Python and modern web technologies",
            "education": "Bachelor's in Computer Science"
        },
        {
            "_id": "2",
            "full_name": "Jane Smith",
            "skills": ["Python", "Django", "PostgreSQL", "JavaScript"],
            "experience": "3 years of experience in web development with Python and Django",
            "education": "Master's in Software Engineering"
        },
        {
            "_id": "3",
            "full_name": "Mike Johnson",
            "skills": ["Java", "Spring Boot", "MySQL"],
            "experience": "4 years of experience in Java development",
            "education": "Bachelor's in Information Technology"
        }
    ]
    
    print("\nTesting single candidate match...")
    # Test single candidate match
    score, explanation = recommender.get_match_score(job_info, candidates[0])
    print(f"\nMatch Score: {score}")
    print(f"Explanation: {explanation}")
    
    print("\nTesting multiple candidate matches...")
    # Test multiple candidate matches
    matches = recommender.get_job_candidate_matches(job_info, candidates)
    
    print("\nRanked Matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. Candidate ID: {match['candidate_id']}")
        print(f"   Match Score: {match['match_score']}")
        print(f"   Explanation: {match['explanation']}")

if __name__ == "__main__":
    test_llama_recommender() 