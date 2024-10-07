from App.models import User, Course, Staff
from App.database import db


def create_staff(title, first_name, last_name, role):
    """Create a new staff member and add them to the database."""
    new_staff = Staff(title=title, firstName=first_name, lastName=last_name, role=role)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff


def assign_staff_to_course(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    """Assign staff to an existing course."""
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return False  # Course not found


    if lecturer_id:
        course.lecturer_id = lecturer_id
    if tutor_id:
        course.tutor_id = tutor_id
    if ta_id:
        course.ta_id = ta_id


    db.session.commit()
    return True
