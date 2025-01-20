from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
import os

mongo_db = None  # Global variable for MongoDB database

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure MongoDB
    app.config.from_object(Config)
    global mongo_db
    mongo_uri = app.config["MONGO_URI"]
    client = MongoClient(mongo_uri)
    mongo_db = client.get_database()

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