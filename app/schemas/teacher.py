"""Teacher schema."""

from marshmallow import Schema, fields, post_dump

from .subject import SubjectSchema


class TeacherSchema(Schema):
    """Schema for Teacher model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    gender = fields.Bool(required=True)
    subject = fields.Nested(SubjectSchema, dump_only=True)
    subject_id = fields.Int(load_only=True)

    class Meta:
        """Meta options."""

        strict = True

    @post_dump
    def format_name(self, data, **kwargs):
        """Format teacher name with gender prefix."""
        if "name" in data and "surname" in data and "gender" in data:
            gender_prefix = "M" if data["gender"] else "Mme."
            data["name"] = f"{gender_prefix} {data['surname']} {data['name']}"
        return data
