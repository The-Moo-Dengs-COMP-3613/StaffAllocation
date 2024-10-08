from App.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseCode = db.Column(db.String(100), nullable=False, unique=True)
    courseName = db.Column(db.String(100), nullable=False)
    
    # Foreign keys linking to the respective roles
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    ta_id = db.Column(db.Integer, db.ForeignKey('tas.id'))
    
    # Relationships
    lecturer = db.relationship('Lecturer', foreign_keys=[lecturer_id])
    tutor = db.relationship('Tutor', foreign_keys=[tutor_id])
    ta = db.relationship('TA', foreign_keys=[ta_id])
