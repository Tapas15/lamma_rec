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

# STEP 1: Get embedding for the first title to determine correct dimension
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': 'llama3.2:latest',
    'prompt': titles[0]
})

embedding = res.json()['embedding']
d = len(embedding)  # Set correct dimension
print(f"Detected embedding dimension: {d}")

# STEP 2: Initialize FAISS index
index = faiss.IndexFlatL2(d)

# STEP 3: Prepare storage for embeddings
X = np.zeros((len(titles), d), dtype='float32')
X[0] = np.array(embedding, dtype='float32')  # Store first one

# STEP 4: Get embeddings for remaining titles
for i, title in enumerate(titles[1:], start=1):
    res = requests.post('http://localhost:11434/api/embeddings', json={
        'model': 'llama3.2:latest',
        'prompt': title
    })
    embedding = res.json()['embedding']
    X[i] = np.array(embedding, dtype='float32')

# STEP 5: Add all embeddings to FAISS index
index.add(X)

# STEP 6: Query embedding
new_prompt = 'The machine learning revolution: How AI is changing the world'
res = requests.post('http://localhost:11434/api/embeddings', json={
    'model': 'llama3.2:latest',
    'prompt': new_prompt
})
query_embedding = np.array([res.json()['embedding']], dtype='float32')

# STEP 7: Search for top 5 most similar titles
D, I = index.search(query_embedding, 5)

# STEP 8: Display results
print("\nMost similar titles:")
for idx in I[0]:
    print(f"- {titles[idx]}")
