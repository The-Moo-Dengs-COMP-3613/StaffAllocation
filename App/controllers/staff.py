from App.models import Course, Lecturer, Tutor, TA
from App.database import db

def create_lecturer(title, first_name, last_name):
    new_lecturer = Lecturer(title=title, firstName=first_name, lastName=last_name)
    db.session.add(new_lecturer)
    db.session.commit()
    return new_lecturer

def create_tutor(title, first_name, last_name):
    new_tutor = Tutor(title=title, firstName=first_name, lastName=last_name)
    db.session.add(new_tutor)
    db.session.commit()
    return new_tutor

def create_ta(title, first_name, last_name):
    new_ta = TA(title=title, firstName=first_name, lastName=last_name)
    db.session.add(new_ta)
    db.session.commit()
    return new_ta

def assign_staff_to_course(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        return False  # Course not found

    if lecturer_id:
        lecturer = Lecturer.query.get(lecturer_id)
        if lecturer:
            lecturer.assign_to_course(course)
    
    if tutor_id:
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            tutor.assign_to_course(course)

    if ta_id:
        ta = TA.query.get(ta_id)
        if ta:
            ta.assign_to_course(course)

    db.session.commit()
    return True

