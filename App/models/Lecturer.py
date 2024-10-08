from App.models import Staff
from App.database import db

class Lecturer(Staff):
    __tablename__ = 'lecturers'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True) 

    def assign_to_course(self, course):
        course.lecturer_id = self.id
