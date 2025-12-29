from ..extensions import db
from .enums import Frequency

class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)

    # Date range
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # NULL = one-off

    # Time (same every occurrence)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # Recurrence
    recurrence = db.Column(db.Enum(Frequency, values_callable=lambda x: [e.name for e in x]), default=Frequency.WEEKLY.name)

    # 0 = Monday, 6 = Sunday
    weekday = db.Column(db.Integer)

    room = db.relationship("Room", back_populates="classes")
    teacher = db.relationship("Teacher", back_populates="classes")
    group = db.relationship("Group", back_populates="classes")
    subject = db.relationship("Subject", back_populates="classes")