import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flask-notely")