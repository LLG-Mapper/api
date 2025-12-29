from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from .room import RoomSchema
from .teacher import TeacherSchema
from .group import GroupSchema
from .subject import SubjectSchema
from ..models.enums import Frequency


class ClassSchema(Schema):
    """Schema for Class model."""

    id = fields.Int(dump_only=True)
    room = fields.Nested(RoomSchema, dump_only=True)
    room_id = fields.Int(load_only=True, required=True)
    teacher = fields.Nested(TeacherSchema, dump_only=True)
    teacher_id = fields.Int(load_only=True, required=True)
    group = fields.Nested(GroupSchema, dump_only=True)
    group_id = fields.Int(load_only=True, required=True)
    subject = fields.Nested(SubjectSchema, dump_only=True)
    subject_id = fields.Int(load_only=True, required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    # Dump API-friendly value, store enum name in DB
    recurrence = EnumField(Frequency, by_value=True, load_default=Frequency.WEEKLY)
    weekday = fields.Int()

    class Meta:
        strict = True

    @post_load
    def store_enum_name(self, data, **kwargs):
        """Convert API value to enum name for DB storage."""
        if "recurrence" in data:
            data["recurrence"] = Frequency(data["recurrence"]).name
        return data
