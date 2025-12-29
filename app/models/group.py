from ..extensions import db
from .enums import Grade

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Enum(Grade, name="class_frequency"), nullable=False)

    classes = db.relationship("Class", back_populates="group")