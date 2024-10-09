from App.database import db

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    
    # Base class method that will be inherited
    def assign_to_course(self, course):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def full_name(self):
        return f"{self.title} {self.firstName} {self.lastName}"

class Lecturer(Staff):
    __tablename__ = 'lecturers'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)

    def assign_to_course(self, course):
        course.lecturer = self  


class Tutor(Staff):
    __tablename__ = 'tutors'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)

    def assign_to_course(self, course):
        course.tutor = self 


class TA(Staff):
    __tablename__ = 'tas'
    id = db.Column(db.Integer, db.ForeignKey('staff.id'), primary_key=True)

    def assign_to_course(self, course):
        course.ta = self  



def get_staff(cls, staff_id):
        """Fetch staff by ID."""
        return cls.query.get(staff_id)

