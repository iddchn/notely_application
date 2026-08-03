from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
import base64
import boto3
from botocore.exceptions import ClientError
import json
import os

mongo_db = None  # Global variable for MongoDB database

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

def setup_database(db):
    # Ensure required collections exist
    required_collections = ["users", "notes"]
    existing_collections = db.list_collection_names()

    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Created missing collection: {collection}")

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure MongoDB
    # app.config.from_object(Config)
    global mongo_db
    mongo_uri = os.getenv("MONGO_URI") or get_secret()
    client = MongoClient(mongo_uri)
    mongo_db = client.get_database("flask-notely")

    setup_database(mongo_db)

    # Register Blueprints
    from application.routers.user_routers import user_blueprint
    from application.routers.note_routers import note_blueprint
    from application.routers.health_routers import health_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(note_blueprint, url_prefix="/notes")
    app.register_blueprint(health_blueprint, url_prefix="/health")

    # Monitoring
    from application.monitoring import setup_monitoring
    setup_monitoring(app)

    return app