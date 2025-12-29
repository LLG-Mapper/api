from ..extensions import db

class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)
    floor = db.Column(db.Integer, default=0)

    rooms = db.relationship("Room", back_populates="building")