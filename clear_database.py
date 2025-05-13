from pymongo import MongoClient

# Update this if your MongoDB URI or DB name is different
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "job_recommender"  # Change if your DB name is different


def clear_collections():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_deleted = db["users"].delete_many({})
    jobs_deleted = db["jobs"].delete_many({})
    print(f"Deleted {users_deleted.deleted_count} users.")
    print(f"Deleted {jobs_deleted.deleted_count} jobs.")

if __name__ == "__main__":
    clear_collections() 