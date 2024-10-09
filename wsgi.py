import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import TA, Lecturer, Tutor, User, Course, Staff
from App.main import create_app

from App.controllers.user import create_user, get_all_users_json, get_all_users

#Import initializing controller
from App.controllers.initialize import initialize

# Import course controller
from App.controllers.course import create_course, view_course_details

# Import staff controller
from App.controllers.staff import create_lecturer, create_tutor, create_ta, assign_staff_to_course


# This commands file allows you to create convenient CLI commands for testing controllers
app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    # Mock data: Create staff entries using Lecturer, Tutor, and TA models
    # Lecturers
    lecturer1 = Lecturer(title="Dr.", firstName="Jane", lastName="Villanueva")
    lecturer2 = Lecturer(title="Prof.", firstName="Jackson", lastName="Duke")
    lecturer3 = Lecturer(title="Dr.", firstName="Emily", lastName="Cooper")
    lecturer4 = Lecturer(title="Prof.", firstName="Tony", lastName="Stark")
    lecturer5 = Lecturer(title="Dr.", firstName="Camille", lastName="Wilson")

    # Tutors
    tutor1 = Tutor(title="Mr.", firstName="Robert", lastName="Pattinson")
    tutor2 = Tutor(title="Ms.", firstName="Lindsay", lastName="Lohan")
    tutor3 = Tutor(title="Mr.", firstName="James", lastName="Charles")
    tutor4 = Tutor(title="Ms.", firstName="Steven", lastName="Harrison")
    tutor5 = Tutor(title="Mr.", firstName="Kevin", lastName="Hart")

    # TAs
    ta1 = TA(title="Mr.", firstName="Mark", lastName="Taylor")
    ta2 = TA(title="Ms.", firstName="Rachel", lastName="Adams")
    ta3 = TA(title="Mr.", firstName="Michael", lastName="Jordan")
    ta4 = TA(title="Ms.", firstName="Jessica", lastName="Alba")
    ta5 = TA(title="Mr.", firstName="Daniel", lastName="Radcliffe")

    # Add all staff to the database
    db.session.add_all([
        lecturer1, lecturer2, lecturer3, lecturer4, lecturer5,
        tutor1, tutor2, tutor3, tutor4, tutor5,
        ta1, ta2, ta3, ta4, ta5
    ])
    db.session.commit()

    # Create mock courses, linking them with actual Lecturer, Tutor, and TA objects
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
    # Check for existing course
    existing_course = Course.query.filter_by(courseCode=course_code).first()
    if existing_course:
        print(f'Error: A course with the code {course_code} already exists.')
        return

    # Fetch staff members
    lecturer = Lecturer.query.get(lecturer_id)
    tutor = Tutor.query.get(tutor_id)
    ta = TA.query.get(ta_id)

    if not lecturer:
        print(f'Error: Lecturer ID {lecturer_id} not found!')
        return
    if not tutor:
        print(f'Error: Tutor ID {tutor_id} not found!')
        return
    if not ta:
        print(f'Error: TA ID {ta_id} not found!')
        return

    # Create the course object
    course = Course(courseCode=course_code, courseName=course_name, lecturer=lecturer, tutor=tutor, ta=ta)
    
    # Add the course to the session
    db.session.add(course)
    db.session.commit()  # Save changes to the database

    lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}"
    tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}"
    ta_name = f"{ta.title} {ta.firstName} {ta.lastName}"

    print(f'Course {course.courseCode} created with:')
    print(f'Lecturer: {lecturer_name}')
    print(f'Tutor: {tutor_name}')
    print(f'Teaching Assistant: {ta_name}')





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
    if role.lower() == "lecturer":
        staff = create_lecturer(title, first_name, last_name)
    elif role.lower() == "tutor":
        staff = create_tutor(title, first_name, last_name)
    elif role.lower() == "ta":
        staff = create_ta(title, first_name, last_name)
    else:
        print(f"Role {role} not recognized. Please use 'lecturer', 'tutor', or 'ta'.")
        return
    print(f'Staff member {staff.firstName} {staff.lastName} created!')

app.cli.add_command(staff_cli)





@staff_cli.command("assign", help="Assign staff to a course")
@click.argument("course_code")
@click.argument("lecturer_id", required=False)
@click.argument("tutor_id", required=False)
@click.argument("ta_id", required=False)
def assign_staff_command(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    # Fetch course by course_code
    course = Course.query.filter_by(courseCode=course_code).first()
    if not course:
        print(f'Error: Course {course_code} not found!')
        return

    # Fetch and assign lecturer if provided
    if lecturer_id:
        lecturer = Lecturer.query.get(lecturer_id)
        if not lecturer:
            print(f'Error: Lecturer ID {lecturer_id} not found!')
            return
        course.lecturer = lecturer

    # Fetch and assign tutor if provided
    if tutor_id:
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            print(f'Error: Tutor ID {tutor_id} not found!')
            return
        course.tutor = tutor

    # Fetch and assign TA if provided
    if ta_id:
        ta = TA.query.get(ta_id)
        if not ta:
            print(f'Error: TA ID {ta_id} not found!')
            return
        course.ta = ta

    db.session.commit()  # Save changes to the database

    lecturer_name = course.lecturer.full_name() if course.lecturer else "None"
    tutor_name = course.tutor.full_name() if course.tutor else "None"
    ta_name = course.ta.full_name() if course.ta else "None"

    print(f'Staff assigned to course {course_code} successfully!')
    print(f'Lecturer: {lecturer_name}')
    print(f'Tutor: {tutor_name}')
    print(f'Teaching Assistant: {ta_name}')





'''
Commands to run to display ids for staff
'''


@staff_cli.command("list_lecturers", help="Lists all lecturers in the database")
def list_lecturers_command():
    lecturers = Lecturer.query.all()
    for lecturer in lecturers:
        print(f'Lecturer ID: {lecturer.id}, Name: {lecturer.full_name()}')

@staff_cli.command("list_tutors", help="Lists all tutors in the database")
def list_tutors_command():
    tutors = Tutor.query.all()
    for tutor in tutors:
        print(f'Tutor ID: {tutor.id}, Name: {tutor.full_name()}')

@staff_cli.command("list_tas", help="Lists all teaching assistants in the database")
def list_tas_command():
    tas = TA.query.all()
    for ta in tas:
        print(f'TA ID: {ta.id}, Name: {ta.full_name()}')




'''
Test Commands
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTest", "-s"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTest", "-s"]))
    else:
        sys.exit(pytest.main(["-k", "App", "-s"]))

app.cli.add_command(test)