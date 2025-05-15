import requests
import numpy as np
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net")
db = client["ai_articles"]
collection = db["titles"]

# Normalize helper
def normalize(v):
    v = np.array(v, dtype='float32')
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def embed_query(prompt):
    res = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "llama3.2:latest",
        "prompt": prompt
    })
    return normalize(res.json()["embedding"]).tolist()

def search_titles(query_text, top_k=5):
    query_vector = embed_query(query_text)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "embedding_index",  # Name of your vector index
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": 100,
                "limit": top_k
            }
        }
    ]
    results = collection.aggregate(pipeline)
    return [(doc["title"], doc.get("score", 0)) for doc in results]

# 🔍 Example usage
query = "AI transforming healthcare with robotics and machine learning"
results = search_titles(query)

for title, score in results:
    print(f"{title} - Score: {score:.2f}")
