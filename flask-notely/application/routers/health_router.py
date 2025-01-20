from flask import Blueprint, jsonify

health_blueprint = Blueprint("Health", __name__)

@health_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200