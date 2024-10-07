from App.models import User, Course, Staff
from App.database import db


def create_course(course_code, course_name, lecturer_id, tutor_id, ta_id):
    """Create a new course and add it to the database."""
    new_course = Course(courseCode=course_code, courseName=course_name,
                        lecturer_id=lecturer_id, tutor_id=tutor_id, ta_id=ta_id)
    db.session.add(new_course)
    db.session.commit()
    return new_course


def view_course_details(course_code):
    """Retrieve details for a specific course with staff names."""
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return f'Course {course_code} not found.'


    lecturer = Staff.query.get(course.lecturer_id)
    tutor = Staff.query.get(course.tutor_id)
    ta = Staff.query.get(course.ta_id)


    lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
    tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
    ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"


    details = {
        "Course Code": course.courseCode,
        "Course Name": course.courseName,
        "Lecturer": lecturer_name,
        "Tutor": tutor_name,
        "Teaching Assistant": ta_name
    }
   
    return details
