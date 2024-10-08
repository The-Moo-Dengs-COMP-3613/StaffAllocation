from App.models import Staff
from App.database import db

class Tutor(Staff):
    __tablename__ = 'tutors'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)

    def assign_to_course(self, course):
        course.tutor_id = self.id
