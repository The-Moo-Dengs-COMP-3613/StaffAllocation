from App.database import db


class Course(db.Model):
    __tablename__ = 'courses'
    courseCode = db.Column(db.String(10), primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)
    
    # Foreign keys to staff members
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    ta_id = db.Column(db.Integer, db.ForeignKey('tas.id'))
    
    lecturer = db.relationship('Lecturer', backref='courses', foreign_keys=[lecturer_id])
    tutor = db.relationship('Tutor', backref='courses', foreign_keys=[tutor_id])
    ta = db.relationship('TA', backref='courses', foreign_keys=[ta_id])


def get_course(cls, course_code):
        """Fetch course by course code."""
        return cls.query.filter_by(courseCode=course_code).first() 

