from flask import Blueprint, request, jsonify
from App.database import db
from App.models import Staff, Course, Lecturer, Tutor, TA
from flask_jwt_extended import jwt_required

staff_bp = Blueprint('staff', __name__)

# create Lecturer
@staff_bp.route('/staff/lecturer', methods=['POST'])
@jwt_required()
def create_lecturer():
    data = request.get_json()

    title = data.get('title')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not title or not first_name or not last_name:
        return jsonify({"error": "Title, first name, and last name are required."}), 400

    lecturer = Lecturer(title=title, firstName=first_name, lastName=last_name)

    db.session.add(lecturer)
    db.session.commit()

    return jsonify({"message": "Lecturer created successfully."}), 201

#create tutor
@staff_bp.route('/staff/tutor', methods=['POST'])
@jwt_required()
def create_tutor():
    data = request.get_json()

    title = data.get('title')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not title or not first_name or not last_name:
        return jsonify({"error": "Title, first name, and last name are required."}), 400

    tutor = Tutor(title=title, firstName=first_name, lastName=last_name)

    db.session.add(tutor)
    db.session.commit()

    return jsonify({"message": "Tutor created successfully."}), 201


#create ta
@staff_bp.route('/staff/ta', methods=['POST'])
@jwt_required()
def create_ta():
    data = request.get_json()

    title = data.get('title')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not title or not first_name or not last_name:
        return jsonify({"error": "Title, first name, and last name are required."}), 400

    ta = TA(title=title, firstName=first_name, lastName=last_name)

    db.session.add(ta)
    db.session.commit()

    return jsonify({"message": "TA created successfully."}), 201


# assign staff to course
@staff_bp.route('/courses/<course_code>/assign', methods=['PUT'])
@jwt_required()
def assign_staff_to_course(course_code):
    data = request.get_json()
    
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return jsonify({"error": "Course not found."}), 200

    lecturer_id = data.get('lecturer_id')
    tutor_id = data.get('tutor_id')
    ta_id = data.get('ta_id')

    if lecturer_id:
        lecturer = Lecturer.get_staff(lecturer_id)
        if not lecturer:
            return jsonify({"error": "Lecturer not found."}), 404
        lecturer.assign_to_course(course)
        
    if tutor_id:
        tutor = Tutor.get_staff(tutor_id)
        if not tutor:
            return jsonify({"error": "Tutor not found."}), 404
        tutor.assign_to_course(course)
        
    if ta_id:
        ta = TA.get_staff(ta_id)
        if not ta:
            return jsonify({"error": "TA not found."}), 404
        ta.assign_to_course(course)

    db.session.commit()

    return jsonify({"message": "Staff assigned successfully."}), 200
