import faiss
import requests
import numpy as np

# -------------------------------
# Step 1: Define job listings
# -------------------------------
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
    # Add more job listings here...
]

model_name = 'llama3.2:latest'
faiss_index = None
embedding_dim = None
metadata = []  # store job metadata with index alignment

# -------------------------------
# Step 2: Helper functions
# -------------------------------

def normalize(v):
    v = np.array(v, dtype='float32')
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def format_job(job):
    return (
        f"{job['job_title']} at {job['company_name']} in {job['location']}. "
        f"{job['job_description']} Skills: {', '.join(job['required_skills'])}. "
        f"Type: {job['job_type']}, Level: {job['experience_level']}, Salary: {job['salary_range']}."
    )

def get_embedding(text):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': model_name,
        'prompt': text
    })
    return normalize(res.json()['embedding'])

# -------------------------------
# Step 3: Build FAISS index
# -------------------------------

print("Generating embeddings and building FAISS index...")

# Get first embedding to determine dimension
first_text = format_job(job_listings[0])
first_vector = get_embedding(first_text)
embedding_dim = len(first_vector)

# Initialize index
faiss_index = faiss.IndexFlatIP(embedding_dim)
X = np.zeros((len(job_listings), embedding_dim), dtype='float32')

# Embed each job
for i, job in enumerate(job_listings):
    job_text = format_job(job)
    emb = get_embedding(job_text)
    X[i] = emb
    metadata.append(job)

# Add all to FAISS
faiss_index.add(X)

print("Index ready.\n")

# -------------------------------
# Step 4: Search jobs
# -------------------------------

def search_jobs(query_text, top_k=5):
    print(f"\n🔍 Searching for: \"{query_text}\"")
    query_vec = get_embedding(query_text).reshape(1, -1)
    similarities, indices = faiss_index.search(query_vec, top_k)
    percent_scores = (similarities[0] * 100).clip(min=0)

    print("\n🎯 Top matching jobs:\n" + "="*50)
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
        print("="*50)


# -------------------------------
# Step 5: Query Example
# -------------------------------

query = "Looking for a senior AI engineer position in California focused on cloud technologies"
search_jobs(query)
