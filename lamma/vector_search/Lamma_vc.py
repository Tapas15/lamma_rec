import faiss
import requests
import numpy as np
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net")
db = client["ai_articles"]
collection = db["titles"]
collection.delete_many({})  # Clear old records

# Data
titles = [
    'Mind blowing AI: The Future of Technology',
    'The Rise of Quantum Computing: A New Era in Technology',
    'The Power of Machine Learning: Transforming Industries',
    'The Impact of Artificial Intelligence on Society',
    'The Future of Robotics: Innovations and Challenges'
]

# Model info
model_name = 'llama3.2:latest'
api_url = 'http://localhost:11434/api/embeddings'

# Normalize helper
def normalize(v):
    v = np.array(v, dtype='float32')
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

# STEP 1: Get embedding dimension
res = requests.post(api_url, json={'model': model_name, 'prompt': titles[0]})
embedding = normalize(res.json()['embedding'])
d = len(embedding)
print(f"Detected embedding dimension: {d}")

# STEP 2: Initialize FAISS cosine index
index = faiss.IndexFlatIP(d)
X = np.zeros((len(titles), d), dtype='float32')
X[0] = embedding

# STEP 3: Insert first title into MongoDB
collection.insert_one({
    "title": titles[0],
    "embedding": embedding.tolist()
})

# STEP 4: Process remaining titles
for i, title in enumerate(titles[1:], start=1):
    res = requests.post(api_url, json={'model': model_name, 'prompt': title})
    emb = normalize(res.json()['embedding'])
    X[i] = emb

    collection.insert_one({
        "title": title,
        "embedding": emb.tolist()
    })

# STEP 5: Add all vectors to FAISS
index.add(X)

print("\n✅ All titles embedded and stored in MongoDB.")
