from flask import request, jsonify
from App.database import db
from App.models import Staff, Course, Lecturer, Tutor, TA
from flask_jwt_extended import jwt_required

@app.route('/staff', methods=['POST'])
@jwt_required()
def create_staff():
    data = request.get_json()

    title = data.get('title')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')

    if not title or not first_name or not last_name or not role:
        return jsonify({"error": "Title, first name, last name, and role are required."}), 400

    # Determine role and create appropriate staff type
    if role == "Lecturer":
        staff = Lecturer(title=title, firstName=first_name, lastName=last_name)
    elif role == "Tutor":
        staff = Tutor(title=title, firstName=first_name, lastName=last_name)
    elif role == "TA":
        staff = TA(title=title, firstName=first_name, lastName=last_name)
    else:
        return jsonify({"error": "Invalid role. Must be Lecturer, Tutor, or TA."}), 400

    db.session.add(staff)
    db.session.commit()

    return jsonify({"message": "Staff created successfully."}), 201

@app.route('/courses/<course_code>/assign', methods=['PUT'])
@jwt_required()
def assign_staff_to_course(course_code):
    data = request.get_json()
    
    # Get the course by course code
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return jsonify({"error": "Course not found."}), 404

    # Assign lecturer, tutor, or TA if provided
    lecturer_id = data.get('lecturer_id')
    tutor_id = data.get('tutor_id')
    ta_id = data.get('ta_id')

    if lecturer_id:
        course.lecturer_id = lecturer_id
    if tutor_id:
        course.tutor_id = tutor_id
    if ta_id:
        course.ta_id = ta_id

    db.session.commit()
    
    return jsonify({"message": "Staff assigned successfully."}), 200