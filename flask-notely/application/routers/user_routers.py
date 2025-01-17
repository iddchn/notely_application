from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from init_app import mongo_db

user_blueprint = Blueprint("User", __name__)

@user_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password
    }
    mongo_db.users.insert_one(new_user)
    return jsonify({"message": "User created successfully"}), 201

@user_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    user = mongo_db.users.find_one({"email": data["email"]})
    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@user_blueprint.route("/", methods=["PUT"])
def update_user():
    data = request.json
    user_id = data["id"]
    updated_user = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"], method="pbkdf2:sha256")
    }
    result = mongo_db.users.update_one({"_id": user_id}, {"$set": updated_user})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User updated successfully"}), 200

@user_blueprint.route("/", methods=["DELETE"])
def delete_user():
    data = request.json
    user_id = data["id"]
    result = mongo_db.users.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User and associated notes deleted"}), 200