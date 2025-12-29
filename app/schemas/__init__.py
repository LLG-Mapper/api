"""Marshmallow schemas for API serialization/deserialization."""

from .building import BuildingSchema
from .feature import FeatureSchema
from .room_type import RoomTypeSchema
from .room import RoomSchema, RoomListSchema
from .teacher import TeacherSchema
from .subject import SubjectSchema
from .group import GroupSchema
from .class_ import ClassSchema

__all__ = [
    "BuildingSchema",
    "FeatureSchema",
    "RoomTypeSchema",
    "RoomSchema",
    "RoomListSchema",
    "TeacherSchema",
    "SubjectSchema",
    "GroupSchema",
    "ClassSchema",
]
