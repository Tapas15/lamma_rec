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

# Choose one model for everything
model_name = 'llama3.2:1b'

# STEP 1: Get embedding for the first title
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': model_name,
    'prompt': titles[0]
})
embedding = res.json()['embedding']
d = len(embedding)
print(f"Detected embedding dimension: {d}")

# STEP 2: Initialize FAISS index
index = faiss.IndexFlatL2(d)

# STEP 3: Prepare array
X = np.zeros((len(titles), d), dtype='float32')
X[0] = np.array(embedding, dtype='float32')

# STEP 4: Get remaining embeddings and normalize them
def normalize(embedding):
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding

for i, title in enumerate(titles[1:], start=1):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': model_name,
        'prompt': title
    })
    embedding = np.array(res.json()['embedding'], dtype='float32')
    X[i] = normalize(embedding)  # Normalize each embedding

# STEP 5: Add to FAISS
index.add(X)

# STEP 6: Embed and normalize query
query = 'The Impact of Artificial Intelligence'
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': model_name,
    'prompt': query
})
query_embedding = np.array(res.json()['embedding'], dtype='float32')
query_embedding = normalize(query_embedding)  # Normalize query embedding

# STEP 7: Search
D, I = index.search(np.array([query_embedding]), 5)  # D = distances (L2), I = indices

# STEP 8: Compute cosine similarity: dot product between normalized vectors
similarities = np.dot(X[I[0]], query_embedding.T) * 100  # Cosine similarity, then convert to percentage

# STEP 9: Zip titles with scores and sort by descending similarity
results = sorted(zip(I[0], similarities), key=lambda x: x[1], reverse=True)

# STEP 10: Print ordered titles with similarity scores as percentage
print("\nMost similar titles (sorted by cosine similarity %):")
for idx, score in results:
    print(f"- {titles[idx]}  (score: {score:.2f}%)")
