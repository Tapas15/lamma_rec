import faiss
import requests
import numpy as np

# Sample titles
titles = [
    'Mind blowing AI: The Future of Technology',
    'The Rise of Quantum Computing: A New Era in Technology',
    'The Power of Machine Learning: Transforming Industries',
    'The Impact of Artificial Intelligence on Society',
    'The Future of Robotics: Innovations and Challenges'
]

# Model to use for embedding
model_name = 'llama3.2:latest'

# Helper: Normalize a vector
def normalize(v):
    v = np.array(v, dtype='float32')
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

# STEP 1: Get embedding dimension from first title
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': model_name,
    'prompt': titles[0]
})
embedding = normalize(res.json()['embedding'])  # Normalize first one
d = len(embedding)
print(f"Detected embedding dimension: {d}")

# STEP 2: Initialize cosine similarity index (normalized inner product)
index = faiss.IndexFlatIP(d)

# STEP 3: Collect normalized embeddings
X = np.zeros((len(titles), d), dtype='float32')
X[0] = embedding

for i, title in enumerate(titles[1:], start=1):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': model_name,
        'prompt': title
    })
    X[i] = normalize(res.json()['embedding'])

# STEP 4: Add normalized embeddings to index
index.add(X)

# STEP 5: Get and normalize query embedding
query = "How machine learning has the power to change industries"
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': model_name,
    'prompt': query
})
query_embedding = normalize(res.json()['embedding']).reshape(1, -1)

# STEP 6: Search using cosine similarity
top_k = 5
similarities, indices = index.search(query_embedding, top_k)  # similarity = dot product of normalized vectors

# STEP 7: Convert cosine similarity (range -1 to 1) to percentage (0–100%)
percent_scores = (similarities[0] * 100).clip(min=0)  # clip negatives to 0 if needed

# STEP 8: Show results
print("\nMost similar titles (sorted by cosine similarity %):")
sorted_results = sorted(zip(indices[0], percent_scores), key=lambda x: x[1], reverse=True)
for idx, score in sorted_results:
    print(f"- {titles[idx]}  (score: {score:.2f}%)")
