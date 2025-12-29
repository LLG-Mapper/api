"""RoomType schema."""

from marshmallow import Schema, fields


class RoomTypeSchema(Schema):
    """Schema for RoomType model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)

    class Meta:
        """Meta options."""

        strict = True
