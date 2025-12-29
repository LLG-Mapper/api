"""Building schema."""

from marshmallow import Schema, fields


class BuildingSchema(Schema):
    """Schema for Building model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    floor = fields.Int(load_default=0)

    class Meta:
        """Meta options."""

        strict = True
