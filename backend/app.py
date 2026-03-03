from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body, optional)
    return: The created student if successful
    """
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON body"}), 404

        name = data.get("name")
        course = data.get("course")
        mark = data.get("mark", 0)

        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Field 'name' is required and must be a non-empty string"}), 404
        if not isinstance(course, str) or not course.strip():
            return jsonify({"error": "Field 'course' is required and must be a non-empty string"}), 404

        if mark is None:
            mark = 0
        if isinstance(mark, bool):
            return jsonify({"error": "Field 'mark' must be an integer between 0 and 100"}), 404
        if not isinstance(mark, int):
            try:
                mark = int(mark)
            except (TypeError, ValueError):
                return jsonify({"error": "Field 'mark' must be an integer between 0 and 100"}), 404
        if mark < 0 or mark > 100:
            return jsonify({"error": "Field 'mark' must be between 0 and 100"}), 404

        new_student = db.insert_student(name.strip(), course.strip(), mark)
        return jsonify(new_student), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body, optional)
    param course: The course the student is enrolled in (from request body, optional)
    param mark: The mark the student received (from request body, optional)
    return: The updated student if successful
    """
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON body"}), 404

        name = data.get("name")
        course = data.get("course")
        mark = data.get("mark")

        if name is not None and (not isinstance(name, str) or not name.strip()):
            return jsonify({"error": "Field 'name' must be a non-empty string when provided"}), 404
        if course is not None and (not isinstance(course, str) or not course.strip()):
            return jsonify({"error": "Field 'course' must be a non-empty string when provided"}), 404

        if mark is not None:
            if isinstance(mark, bool):
                return jsonify({"error": "Field 'mark' must be an integer between 0 and 100"}), 404
            if not isinstance(mark, int):
                try:
                    mark = int(mark)
                except (TypeError, ValueError):
                    return jsonify({"error": "Field 'mark' must be an integer between 0 and 100"}), 404
            if mark < 0 or mark > 100:
                return jsonify({"error": "Field 'mark' must be between 0 and 100"}), 404

        updated = db.update_student(
            student_id,
            name=name.strip() if isinstance(name, str) and name.strip() else None,
            course=course.strip() if isinstance(course, str) and course.strip() else None,
            mark=mark,
        )
        if updated is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(updated), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        existing = db.get_student_by_id(student_id)
        if existing is None:
            return jsonify({"error": "Student not found"}), 404

        deleted = db.delete_student(student_id)
        if deleted is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(existing), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks = [s["mark"] for s in students if s.get("mark") is not None]

        count = len(marks)
        if count == 0:
            # Edge case: no marks available
            stats = {
                "count": 0,
                "average": None,
                "min": None,
                "max": None,
            }
        else:
            total = sum(marks)
            stats = {
                "count": count,
                "average": total / count,
                "min": min(marks),
                "max": max(marks),
            }

        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
