import requests
import numpy as np
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Step 1: Connect to MongoDB
client = MongoClient("mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net", server_api=ServerApi('1'))
db = client['vector_db']
collection = db['documents']

# Step 2: Embedding function using LLaMA 3 via Ollama
def get_embedding(text: str):
    response = requests.post(
        'http://localhost:11434/api/embeddings',
        json={
            "model": "llama3.2:latest",
            "prompt": text
        }
    )
    data = response.json()
    return data['embedding']

# Step 3: Insert document with embedding
def insert_document(text: str):
    vector = get_embedding(text)
    doc = {
        "text": text,
        "embedding": vector
    }
    collection.insert_one(doc)
    print("Inserted:", text)

# Step 4: Vector search using $vectorSearch (MongoDB 7+)
def search_similar_documents(query: str, top_k: int = 3):
    query_vector = get_embedding(query)
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "vector_index"  # Name of your vector index
            }
        }
    ])
    print("Results:")
    for doc in results:
        print(doc['text'])

# Example usage:
insert_document("The cat is sleeping on the sofa.")
insert_document("The dog is playing in the garden.")
insert_document("Artificial intelligence is transforming the world.")

search_similar_documents("What dog doing")
