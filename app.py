
import sqlite3

from flask import Flask, jsonify, request

from database import (
    init_db,
    get_all_sessions,
    create_session,
    check_database
)

app = Flask(__name__)

init_db()


@app.route("/health", methods=["GET"])
def health_check():
    try:
        check_database()

        return jsonify({
            "status": "success",
            "message": "Ahoum Sessions API is ready"
        }), 200

    except sqlite3.Error:
        return jsonify({
            "status": "error",
            "message": "Database is unavailable"
        }), 503


@app.route("/sessions", methods=["GET"])
def list_sessions():
    sessions = get_all_sessions()

    return jsonify({
        "sessions": sessions,
        "count": len(sessions)
    }), 200


@app.route("/sessions", methods=["POST"])
def add_session():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object"
        }), 400

    required_fields = [
        "title",
        "description",
        "category",
        "duration"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    for field in ["title", "description", "category"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return jsonify({
                "error": f"{field} must be a non-empty string"
            }), 400

    duration = data["duration"]

    if (
        isinstance(duration, bool)
        or not isinstance(duration, int)
        or duration <= 0
    ):
        return jsonify({
            "error": "duration must be a positive integer"
        }), 400

    title = data["title"].strip()
    description = data["description"].strip()
    category = data["category"].strip()

    session_id = create_session(
        title,
        description,
        category,
        duration
    )

    return jsonify({
        "message": "Session created successfully",
        "session": {
            "id": session_id,
            "title": title,
            "description": description,
            "category": category,
            "duration": duration
        }
    }), 201


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
