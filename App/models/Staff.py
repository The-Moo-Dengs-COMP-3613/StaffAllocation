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
