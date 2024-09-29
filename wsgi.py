import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Course, Staff
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users, initialize, create_course, create_staff, assign_staff_to_course, view_course_details)

# This commands file allows you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    # Mock data: Create staff entries
    # Lecturers
    lecturer1 = Staff(title="Dr.", firstName="Jane", lastName="Villanueva", role="lecturer")
    lecturer2 = Staff(title="Prof.", firstName="Jackson", lastName="Duke", role="lecturer")
    lecturer3 = Staff(title="Dr.", firstName="Emily", lastName="Cooper", role="lecturer")
    lecturer4 = Staff(title="Prof.", firstName="Tony", lastName="Stark", role="lecturer")
    lecturer5 = Staff(title="Dr.", firstName="Camille", lastName="Wilson", role="lecturer")

    # Tutors
    tutor1 = Staff(title="Mr.", firstName="Robert", lastName="Pattinson", role="tutor")
    tutor2 = Staff(title="Ms.", firstName="Lindsay", lastName="Lohan", role="tutor")
    tutor3 = Staff(title="Mr.", firstName="James", lastName="Charles", role="tutor")
    tutor4 = Staff(title="Ms.", firstName="Steven", lastName="Harrison", role="tutor")
    tutor5 = Staff(title="Mr.", firstName="Kevin", lastName="Hart", role="tutor")

    # TAs
    ta1 = Staff(title="Mr.", firstName="Mark", lastName="Taylor", role="ta")
    ta2 = Staff(title="Ms.", firstName="Rachel", lastName="Adams", role="ta")
    ta3 = Staff(title="Mr.", firstName="Michael", lastName="Jordan", role="ta")
    ta4 = Staff(title="Ms.", firstName="Jessica", lastName="Alba", role="ta")
    ta5 = Staff(title="Mr.", firstName="Daniel", lastName="Radcliffe", role="ta")

    # Add all staff to the database
    db.session.add_all([
        lecturer1, lecturer2, lecturer3, lecturer4, lecturer5,
        tutor1, tutor2, tutor3, tutor4, tutor5,
        ta1, ta2, ta3, ta4, ta5
    ])
    db.session.commit()

    # Create mock courses, linking them with actual Staff objects
    course1 = Course(courseCode="COMP101", courseName="Introduction to Computer Science", lecturer=lecturer1, tutor=tutor1, ta=ta1)
    course2 = Course(courseCode="MATH102", courseName="Discrete Maths", lecturer=lecturer2, tutor=tutor2, ta=ta2)
    course3 = Course(courseCode="ELEC201", courseName="Electronics", lecturer=lecturer3, tutor=tutor3, ta=ta3)
    course4 = Course(courseCode="ENG101", courseName="Thermodynamics", lecturer=lecturer4, tutor=tutor4, ta=ta4)
    course5 = Course(courseCode="COMP102", courseName="Computer Programming", lecturer=lecturer5, tutor=tutor5, ta=ta5)

    # Add all courses to the database
    db.session.add_all([course1, course2, course3, course4, course5])
    db.session.commit()

    print('Database initialized with mock data')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Course Commands
'''
course_cli = AppGroup('course', help='Course object commands')

@course_cli.command("create", help="Creates a course")
@click.argument("course_code")
@click.argument("course_name")
@click.argument("lecturer_id")
@click.argument("tutor_id")
@click.argument("ta_id")
def create_course_command(course_code, course_name, lecturer_id, tutor_id, ta_id):
    course = create_course(course_code, course_name, lecturer_id, tutor_id, ta_id)

    # Fetch and display staff names
    lecturer = Staff.query.get(lecturer_id)
    tutor = Staff.query.get(tutor_id)
    ta = Staff.query.get(ta_id)

    lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
    tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
    ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"

    print(f'Course {course.courseCode} created with:')
    print(f'Lecturer: {lecturer_name}')
    print(f'Tutor: {tutor_name}')
    print(f'Teaching Assistant: {ta_name}')

@course_cli.command("assign", help="Assign staff to a course")
@click.argument("course_code")
@click.argument("lecturer_id", required=False)
@click.argument("tutor_id", required=False)
@click.argument("ta_id", required=False)
def assign_staff_command(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    success = assign_staff_to_course(course_code, lecturer_id, tutor_id, ta_id)
    if success:
        # Fetch and display staff names
        course = Course.query.filter_by(courseCode=course_code).first()
        lecturer = Staff.query.get(course.lecturer_id)
        tutor = Staff.query.get(course.tutor_id)
        ta = Staff.query.get(course.ta_id)

        lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
        tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
        ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"

        print(f'Staff assigned to course {course_code} successfully!')
        print(f'Lecturer: {lecturer_name}')
        print(f'Tutor: {tutor_name}')
        print(f'Teaching Assistant: {ta_name}')
    else:
        print(f'Course {course_code} not found!')

@course_cli.command("view", help="View course details")
@click.argument("course_code")
def view_course_command(course_code):
    details = view_course_details(course_code)
    if isinstance(details, str):
        print(details)
    else:
        print("Course Details:")
        for key, value in details.items():
            print(f"{key}: {value}")

app.cli.add_command(course_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Creates a staff member")
@click.argument("title")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("role")
def create_staff_command(title, first_name, last_name, role):
    staff = create_staff(title, first_name, last_name, role)
    print(f'Staff member {staff.firstName} {staff.lastName} created!')

app.cli.add_command(staff_cli)

'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
