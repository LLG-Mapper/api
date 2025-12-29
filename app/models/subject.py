from ..extensions import db
from .enums import Color

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    color = db.Column(db.Enum(Color, name="color_palette"), nullable=False, default=Color.BLUE)

    classes = db.relationship("Class", back_populates="subject")
    subject_teachers = db.relationship("Teacher", back_populates="subject")