"""Subject schema."""

from marshmallow import Schema, fields
from ..models.enums import Color


class SubjectSchema(Schema):
    """Schema for Subject model."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    color = fields.Str(load_default=Color.BLUE)

    class Meta:
        """Meta options."""

        strict = True
