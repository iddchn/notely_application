from encodings.base64_codec import base64_decode

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():

    secret_name = os.getenv("MONGO_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")
    print(f"Getting secret name {secret_name} from region {region_name}")
    # Create a Secrets Manager client
    session = boto3.session.Session()
    print(f"Session: {session}")
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    print(f"Client: {client}")
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print("Encountered an error while fetching secret")
        raise e
    secret_dict = json.loads(get_secret_value_response['SecretString'])
    secret = secret_dict['mongo_uri']
    print(f"Secret: {base64_decode(secret)}")
    return base64_decode(secret)


def setup_database():
    mongo_uri = get_secret()
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