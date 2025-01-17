from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from init_app import mongo_db
from datetime import datetime

note_blueprint = Blueprint("notes", __name__)

@note_blueprint.route("", methods=["POST"])
def create_note():
    data = request.json
    required_fields = ["user_id", "header", "body"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing field: {field}"}), 400

    new_note = {
        "user_id": ObjectId(data["user_id"]),
        "header": data["header"],
        "body": data["body"],
        "created_at": datetime.utcnow()
    }
    result = mongo_db.notes.insert_one(new_note)
    return jsonify({"message": "Note created successfully", "note_id": str(result.inserted_id)}), 201

@note_blueprint.route("/all/<user_id>", methods=["GET"])
def get_notes(user_id):
    try:
        user_id = ObjectId(user_id)
    except Exception:
        return jsonify({"message": "Invalid note ID"}), 400

    notes = mongo_db.notes.find({"user_id": ObjectId(user_id)})
    if notes:
        notes_list = []
        for note in notes:
            note["_id"] = str(note["_id"])
            note["user_id"] = str(note["user_id"])
            notes_list.append(note)

        return jsonify(notes_list), 200

    return jsonify({"message": "Notes not found"}), 404

@note_blueprint.route("/<note_id>", methods=["PUT"])
def update_note(note_id):
    try:
        note_id = ObjectId(note_id)
    except Exception:
        return jsonify({"message": "Invalid note ID"}), 400

    data = request.json
    required_fields = ["header", "body"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing field: {field}"}), 400

    updated_note = {
        "header": data["header"],
        "body": data["body"],
        "created_at": datetime.utcnow()
    }
    result = mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": updated_note})
    if result.matched_count == 0:
        return jsonify({"message": "Note not found"}), 404
    return jsonify({"message": "Note updated successfully"}), 200

@note_blueprint.route("/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    try:
        note_id = ObjectId(note_id)
    except Exception:
        return jsonify({"message": "Invalid note ID"}), 400

    result = mongo_db.notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        return jsonify({"message": "Note not found"}), 404
    return jsonify({"message": "Note deleted successfully"}), 200