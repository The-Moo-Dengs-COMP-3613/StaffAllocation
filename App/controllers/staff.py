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


def assign_staff_to_course(course_code, lecturer_id, tutor_id, ta_id):
    course = Course.query.filter_by(courseCode=course_code).first()
    
    if not course:
        return False  # Course not found
    
    # Check lecturer
    if lecturer_id:
        lecturer = Lecturer.query.get(lecturer_id)
        if not lecturer:
            print(f"Lecturer with ID {lecturer_id} not found.")
            return False  # Lecturer ID is invalid
    
    # Check tutor
    if tutor_id:
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            print(f"Tutor with ID {tutor_id} not found.")
            return False  # Tutor ID is invalid

    # Check TA
    if ta_id:
        ta = TA.query.get(ta_id)
        if not ta:
            print(f"TA with ID {ta_id} not found.")
            return False  # TA ID is invalid

    # Assign staff to the course
    course.lecturer = lecturer if lecturer_id else course.lecturer
    course.tutor = tutor if tutor_id else course.tutor
    course.ta = ta if ta_id else course.ta
    db.session.commit()
    
    return True  # Assignment successful


def get_staff(cls, staff_id):
    """Fetch staff by ID."""
    return cls.query.get(staff_id)

# def assign_staff_to_course(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
#     course = Course.query.filter_by(courseCode=course_code).first()
#     if not course:
#         return False  # Course not found

#     if lecturer_id:
#         lecturer = Lecturer.query.get(lecturer_id)
#         if lecturer:
#             lecturer.assign_to_course(course)
    
#     if tutor_id:
#         tutor = Tutor.query.get(tutor_id)
#         if tutor:
#             tutor.assign_to_course(course)

#     if ta_id:
#         ta = TA.query.get(ta_id)
#         if ta:
#             ta.assign_to_course(course)

#     db.session.commit()
#     return True

