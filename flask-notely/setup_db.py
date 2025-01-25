import base64
from pymongo import MongoClient
import os
import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = os.getenv("MONGO_SECRET_NAME")
    region_name = os.getenv("AWS_REGION")
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print("Encountered an error while fetching secret")
        raise e
    secret_dict = json.loads(get_secret_value_response['SecretString'])
    secret = secret_dict['mongodb_uri']
    return base64.b64decode(secret).decode('utf-8')

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
