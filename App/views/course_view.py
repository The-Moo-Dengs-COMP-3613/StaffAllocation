from flask import Blueprint, request, jsonify
from App.database import db
from App.models import Course
from flask_jwt_extended import jwt_required

course_bp = Blueprint('courses', __name__)

# create course
@course_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    
    course_code = data.get('course_code')
    course_name = data.get('course_name')
    lecturer_id = data.get('lecturer_id')
    tutor_id = data.get('tutor_id')
    ta_id = data.get('ta_id')
    
    if not course_code or not course_name:
        return jsonify({"error": "Course code and name are required."}), 400
    
    if Course.query.filter_by(courseCode=course_code).first():
        return jsonify({"error": "Course code already exists."}), 400
    
    course = Course(
        courseCode=course_code,
        courseName=course_name,
        lecturer_id=lecturer_id,
        tutor_id=tutor_id,
        ta_id=ta_id
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({"message": "Course created successfully."}), 200  


# view course
@course_bp.route('/courses/<course_code>', methods=['GET'])
@jwt_required()
def view_course(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()

    if not course:
        return jsonify({"error": "Course not found."}), 200

    course_details = {
        "course_code": course.courseCode,
        "course_name": course.courseName,
        "lecturer": course.lecturer.full_name() if course.lecturer else None,
        "tutor": course.tutor.full_name() if course.tutor else None,
        "ta": course.ta.full_name() if course.ta else None
    }

    return jsonify(course_details), 404


