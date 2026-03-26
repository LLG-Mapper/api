from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from ..extensions import db

class Room(db.Model):
    __tablename__ = "rooms"
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50))
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer)
    is_open = db.Column(db.Boolean, default=True)
    type_id = db.Column(db.Integer, db.ForeignKey("room_types.id"), nullable=False, default=0)
    path = db.Column(db.String(255), nullable=False)
    
    building = db.relationship("Building", back_populates="rooms")
    type = db.relationship("RoomType", back_populates="rooms")
    features = db.relationship("Feature", secondary="room_features", back_populates="rooms")
    classes = db.relationship("Class", back_populates="room", lazy="selectin")

    @property
    def display_name(self):
        if self.name:
            return self.name
        return f"{self.building.code}{self.floor}{self.number:02d}"

    @hybrid_property
    def display_floor(self):
        floor = self.floor if self.floor is not None else 0
        building_floor = self.building.floor if self.building and self.building.floor is not None else 0
        return floor + building_floor
    
    @display_floor.expression
    def display_floor(cls):
        from .building import Building
        return cls.floor + func.coalesce(
            db.select(Building.floor).where(Building.id == cls.building_id).correlate(cls).scalar_subquery(),
            0
        )

    def is_available_at(self, dt):
        from app.services.availability_service import is_room_available
        return is_room_available(self, dt)
    
    def is_available_now(self):
        return self.is_available_at(datetime.now())