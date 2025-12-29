from ..extensions import db

class Feature(db.Model):
    __tablename__ = "features"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    code = db.Column(db.String(10), nullable=False, unique=True)

    rooms = db.relationship("Room", secondary="room_features", back_populates="features")

    room_features = db.Table(
        "room_features",
        db.Column("room_id", db.Integer, db.ForeignKey("rooms.id"), primary_key=True),
        db.Column("feature_id", db.Integer, db.ForeignKey("features.id"), primary_key=True)
    )