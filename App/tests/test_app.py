import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Course, Staff
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    # create_course,
    # create_lecturer,
    # create_tutor,
    # create_ta,
    # assign_staff_to_course,
    # view_course_details
)
from App.controllers.course import create_course
from App.controllers.staff import create_lecturer
from App.controllers.staff import create_ta
from App.controllers.staff import create_tutor
from App.controllers.course import view_course_details
from App.controllers.staff import assign_staff_to_course



LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    
    def test_create_course(session):
        # Create the lecturer, tutor, and TA here instead of using fixtures
        lecturer = create_lecturer("Dr.", "Heinz", "Doofenshmirtz")
        tutor = create_tutor("Mr.", "Jim", "Halpert")
        ta = create_ta("Ms.", "Pam", "Beesly")
        
        course = create_course("COMP200", "Advanced Programming", lecturer.id, tutor.id, ta.id)
        assert course.courseCode == "COMP200"
        assert course.courseName == "Advanced Programming"
        assert course.lecturer_id == lecturer.id
        assert course.tutor_id == tutor.id
        assert course.ta_id == ta.id

    def test_create_lecturer(session):
        staff = create_lecturer("Dr.", "Heinz", "Doofenshmirtz")
        assert staff.title == "Dr."
        assert staff.firstName == "Heinz"
        assert staff.lastName == "Doofenshmirtz"
      
    def test_create_tutor(session):
        staff = create_tutor("Mr.", "Jim", "Halpert")
        assert staff.title == "Mr."
        assert staff.firstName == "Jim"
        assert staff.lastName == "Halpert"
      

    def test_create_ta(session):
        staff = create_ta("Ms.", "Pam", "Beesly")
        assert staff.title == "Ms."
        assert staff.firstName == "Pam"
        assert staff.lastName == "Beesly"
        
    def test_assign_staff_to_course(session):
        # Create the course, lecturer, tutor, and TA here instead of using fixtures
        lecturer = create_lecturer("Dr.", "Heinz", "Doofenshmirtz")
        tutor = create_tutor("Mr.", "Jim", "Halpert")
        ta = create_ta("Ms.", "Pam", "Beesly")
        
        create_course("COMP101", "Intro to Programming")
        result = assign_staff_to_course("COMP101", lecturer.id, tutor.id, ta.id)
        assert result is True
        course = Course.query.filter_by(courseCode="COMP101").first()
        assert course is not None
        assert course.lecturer_id == lecturer.id
        assert course.tutor_id == tutor.id
        assert course.ta_id == ta.id

    def test_view_course_staff(session):
        # Create the lecturer, tutor, and TA here instead of using fixtures
        lecturer = create_lecturer("Dr.", "Heinz", "Doofenshmirtz")
        tutor = create_tutor("Mr.", "Jim", "Halpert")
        ta = create_ta("Ms.", "Pam", "Beesly")
        
        create_course("COMP300", "Advanced Programming")
        assign_staff_to_course("COMP300", lecturer.id, tutor.id, ta.id)
        details = view_course_details("COMP300")
        assert details["Course Code"] == "COMP300"
        assert details["Course Name"] == "Advanced Programming"
        assert details["Lecturer"] == f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}"
        assert details["Tutor"] == f"{tutor.title} {tutor.firstName} {tutor.lastName}"
        assert details["Teaching Assistant"] == f"{ta.title} {ta.firstName} {ta.lastName}"

        

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

