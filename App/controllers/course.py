from App.models import Course, Lecturer, Tutor, TA
from App.database import db

def create_course(course_code, course_name, lecturer_id=None, tutor_id=None, ta_id=None):
    new_course = Course(courseCode=course_code, courseName=course_name)
    
    if lecturer_id:
        lecturer = Lecturer.query.get(lecturer_id)
        if lecturer:
            new_course.lecturer = lecturer
    
    if tutor_id:
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            new_course.tutor = tutor
    
    if ta_id:
        ta = TA.query.get(ta_id)
        if ta:
            new_course.ta = ta

    db.session.add(new_course)
    db.session.commit()
    return new_course

def view_course_details(course_code):
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return f'Course {course_code} not found.'

    lecturer_name = course.lecturer.full_name() if course.lecturer else "None"
    tutor_name = course.tutor.full_name() if course.tutor else "None"
    ta_name = course.ta.full_name() if course.ta else "None"

    details = {
        "Course Code": course.courseCode,
        "Course Name": course.courseName,
        "Lecturer": lecturer_name,
        "Tutor": tutor_name,
        "Teaching Assistant": ta_name
    }

    return details


def get_course(course_code):
    """Fetch course by course code."""
    return Course.query.filter_by(courseCode=course_code).first()
