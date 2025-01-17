from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os

def setup_database():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/flask-notely")
    client = MongoClient(mongo_uri)
    db = client.get_database("flask-notely")

    # Ensure required collections exist
    required_collections = ["users", "notes"]
    existing_collections = db.list_collection_names()

    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Created missing collection: {collection}")

    # Initialize the first user
    initialize_first_user(db)

def initialize_first_user(db):
    users_collection = db.get_collection("users")

    if users_collection.count_documents({}) == 0:
        hashed_password = generate_password_hash("admin123", method="pbkdf2:sha256")
        first_user = {
            "name": "admin",
            "email": "admin@example.com",
            "password": hashed_password,
        }
        users_collection.insert_one(first_user)
        print("First user created: admin@example.com with password admin123")
    else:
        print("Users already exist. No default user created.")