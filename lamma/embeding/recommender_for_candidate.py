import faiss
import requests
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
model_name = 'llama3.2:latest'

# -----------------------------
# JOB LISTINGS
# -----------------------------
job_listings = [
    {
        "job_id": 1,
        "company_name": "Google",
        "job_title": "Senior Software Engineer",
        "location": "Mountain View, CA",
        "job_description": "Join our team to build next-gen cloud solutions and AI-powered applications.",
        "required_skills": ["Python", "Distributed Systems", "AI/ML", "Cloud Platforms"],
        "job_type": "Full-time",
        "experience_level": "Senior",
        "salary_range": "$150,000 - $200,000",
        "job_link": "https://careers.google.com/jobs/1"
    },
    {
        "job_id": 2,
        "company_name": "OpenAI",
        "job_title": "Research Engineer",
        "location": "San Francisco, CA",
        "job_description": "Work on cutting-edge machine learning and reinforcement learning research.",
        "required_skills": ["Python", "Deep Learning", "PyTorch", "RL"],
        "job_type": "Full-time",
        "experience_level": "Mid",
        "salary_range": "$160,000 - $210,000",
        "job_link": "https://openai.com/careers/jobs/2"
    },
    # Add more jobs here...
]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def normalize(v):
    v = np.array(v, dtype='float32')
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def get_embedding(text):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': model_name,
        'prompt': text
    })
    return normalize(res.json()['embedding'])

def format_job(job):
    return (
        f"{job['job_title']} at {job['company_name']} in {job['location']}. "
        f"{job['job_description']} Skills: {', '.join(job['required_skills'])}. "
        f"Type: {job['job_type']}, Level: {job['experience_level']}, Salary: {job['salary_range']}."
    )

def format_candidate(candidate):
    return (
        f"{candidate['name']} is a {candidate['experience_level']} candidate located in {candidate['location']} "
        f"looking for a {candidate['job_type']} role. Skilled in {', '.join(candidate['skills'])}. "
        f"Preferred salary: {candidate['expected_salary']}."
    )

# -----------------------------
# FAISS INDEXING
# -----------------------------
first_text = format_job(job_listings[0])
first_vector = get_embedding(first_text)
d = len(first_vector)
faiss_index = faiss.IndexFlatIP(d)
X = np.zeros((len(job_listings), d), dtype='float32')
metadata = []

for i, job in enumerate(job_listings):
    emb = get_embedding(format_job(job))
    X[i] = emb
    metadata.append(job)

faiss_index.add(X)
print("✅ Job index built.")

# -----------------------------
# CANDIDATE PROFILE INPUT
# -----------------------------
candidate = {
    "name": "Tapas kumar",
    "location": "California",
    "experience_level": "Senior",
    "skills": ["AI/ML Engineer", "Cloud Computing", "Python", "Distributed Systems"],
    "job_type": "Full-time",
    "expected_salary": "$100,000 - $220,000"
}

# -----------------------------
# SEARCH JOBS FOR CANDIDATE
# -----------------------------
def recommend_jobs_for_candidate(candidate_profile, top_k=5):
    prompt = format_candidate(candidate_profile)
    query_vec = get_embedding(prompt).reshape(1, -1)
    similarities, indices = faiss_index.search(query_vec, top_k)
    percent_scores = (similarities[0] * 100).clip(min=0)

    print(f"\n🔍 Job Recommendations for {candidate_profile['name']}")
    print("="*60)
    for idx, score in zip(indices[0], percent_scores):
        job = metadata[idx]
        print(f"📌 Match Score: {score:.2f}%")
        print(f"🆔 Job ID: {job['job_id']}")
        print(f"🏢 Company: {job['company_name']}")
        print(f"💼 Title: {job['job_title']}")
        print(f"📍 Location: {job['location']}")
        print(f"📝 Description: {job['job_description']}")
        print(f"🧠 Skills Required: {', '.join(job['required_skills'])}")
        print(f"⌛ Job Type: {job['job_type']}")
        print(f"📈 Experience Level: {job['experience_level']}")
        print(f"💰 Salary Range: {job['salary_range']}")
        print(f"🔗 Job Link: {job['job_link']}")
        print("="*60)

# -----------------------------
# RUN SEARCH
# -----------------------------
recommend_jobs_for_candidate(candidate)
