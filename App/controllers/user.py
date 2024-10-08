from App.models import User, Course, Staff
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


# Functions for command logic - moved to separate controllers

# def create_course(course_code, course_name, lecturer_id, tutor_id, ta_id):
#     """Create a new course and add it to the database."""
#     new_course = Course(courseCode=course_code, courseName=course_name, 
#                         lecturer_id=lecturer_id, tutor_id=tutor_id, ta_id=ta_id)
#     db.session.add(new_course)
#     db.session.commit()
#     return new_course

# def create_staff(title, first_name, last_name, role):
#     """Create a new staff member and add them to the database."""
#     new_staff = Staff(title=title, firstName=first_name, lastName=last_name, role=role)
#     db.session.add(new_staff)
#     db.session.commit()
#     return new_staff

# def assign_staff_to_course(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
#     """Assign staff to an existing course."""
#     course = Course.query.filter_by(courseCode=course_code).first()
#     if not course:
#         return False  # Course not found

#     if lecturer_id:
#         course.lecturer_id = lecturer_id
#     if tutor_id:
#         course.tutor_id = tutor_id
#     if ta_id:
#         course.ta_id = ta_id

#     db.session.commit()
#     return True

# def view_course_details(course_code):
#     """Retrieve details for a specific course with staff names."""
#     course = Course.query.filter_by(courseCode=course_code).first()
#     if not course:
#         return f'Course {course_code} not found.'

#     lecturer = Staff.query.get(course.lecturer_id)
#     tutor = Staff.query.get(course.tutor_id)
#     ta = Staff.query.get(course.ta_id)

#     lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
#     tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
#     ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"

#     details = {
#         "Course Code": course.courseCode,
#         "Course Name": course.courseName,
#         "Lecturer": lecturer_name,
#         "Tutor": tutor_name,
#         "Teaching Assistant": ta_name
#     }
    
#     return details
