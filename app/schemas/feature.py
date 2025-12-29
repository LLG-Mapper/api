"""Feature schema."""

from marshmallow import Schema, fields


class FeatureSchema(Schema):
    """Schema for Feature model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)

    class Meta:
        """Meta options."""

        strict = True
