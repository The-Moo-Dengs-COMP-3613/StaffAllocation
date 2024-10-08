from App.models import Staff
from App.database import db

class TA(Staff):
    __tablename__ = 'tas'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)

    def assign_to_course(self, course):
        course.ta_id = self.id
