from flask import request, jsonify
from App.database import db
from App.models import Course, Lecturer, Tutor, TA
from flask_jwt_extended import jwt_required

@app.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    
    # Validate request data
    course_code = data.get('course_code')
    course_name = data.get('course_name')
    lecturer_id = data.get('lecturer_id')
    tutor_id = data.get('tutor_id')
    ta_id = data.get('ta_id')
    
    if not course_code or not course_name:
        return jsonify({"error": "Course code and name are required."}), 400
    
    # Check if the course code already exists
    if Course.query.filter_by(courseCode=course_code).first():
        return jsonify({"error": "Course code already exists."}), 400
    
    # Create the new course
    course = Course(
        courseCode=course_code,
        courseName=course_name,
        lecturer_id=lecturer_id,
        tutor_id=tutor_id,
        ta_id=ta_id
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({"message": "Course created successfully."}), 201

@app.route('/courses/<course_code>', methods=['GET'])
@jwt_required()
def view_course(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()
    
    if not course:
        return jsonify({"error": "Course not found."}), 404

    course_details = {
        "course_code": course.courseCode,
        "course_name": course.courseName,
        "lecturer": course.lecturer.full_name() if course.lecturer else None,
        "tutor": course.tutor.full_name() if course.tutor else None,
        "ta": course.ta.full_name() if course.ta else None
    }
    
    return jsonify(course_details), 200
