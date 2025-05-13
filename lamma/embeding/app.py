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

# STEP 4: Get remaining embeddings
for i, title in enumerate(titles[1:], start=1):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': model_name,
        'prompt': title
    })
    X[i] = np.array(res.json()['embedding'], dtype='float32')

# STEP 5: Add to FAISS
index.add(X)

# STEP 6: Embed query
query = 'The Impact of Artificial Intelligence'
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': model_name,
    'prompt': query
})
query_embedding = np.array([res.json()['embedding']], dtype='float32')

# STEP 7: Search
D, I = index.search(query_embedding, 5)


# STEP 7: Search top K results
top_k = 5
D, I = index.search(query_embedding, top_k)  # D = distances (L2), I = indices

# STEP 8: Convert distances to similarity percentages
# similarity = 1 / (1 + distance) → then convert to percentage
similarities = (1 / (1 + D[0])) * 100  # Now in 0–100 range

# STEP 9: Zip titles with scores and sort by descending score
results = sorted(zip(I[0], similarities), key=lambda x: x[1], reverse=True)

# STEP 10: Print ordered titles with percentage similarity scores
print("\nMost similar titles (sorted by similarity %):")
for idx, score in results:
    print(f"- {titles[idx]}  (score: {score:.2f}%)")

