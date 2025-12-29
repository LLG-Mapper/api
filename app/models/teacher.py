from ..extensions import db

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))

    classes = db.relationship("Class", back_populates="teacher")
    subject = db.relationship("Subject", back_populates="subject_teachers")