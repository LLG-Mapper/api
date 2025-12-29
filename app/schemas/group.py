"""Group schema."""

from marshmallow import Schema, fields


class GroupSchema(Schema):
    """Schema for Group model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    grade = fields.Int(required=True)

    class Meta:
        """Meta options."""

        strict = True
