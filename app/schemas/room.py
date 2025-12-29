"""Room schema."""

from marshmallow import Schema, fields, post_dump

from .building import BuildingSchema
from .feature import FeatureSchema
from .room_type import RoomTypeSchema


class RoomSchema(Schema):
    """Schema for Room model."""

    id = fields.Int(dump_only=True)
    number = fields.Int(required=True)
    name = fields.Str(dump_only=True)  # Will be replaced by display_name if empty
    building = fields.Nested(BuildingSchema, dump_only=True)
    building_id = fields.Int(load_only=True, required=True)
    floor = fields.Int(required=True)
    capacity = fields.Int()
    is_open = fields.Bool(load_default=True)
    type = fields.Nested(RoomTypeSchema, dump_only=True)
    type_id = fields.Int(load_only=True, required=True)
    locationX = fields.Int(required=True)
    locationY = fields.Int(required=True)
    sizeX = fields.Int(required=True)
    sizeY = fields.Int(required=True)
    features = fields.Nested(FeatureSchema, many=True, dump_only=True)
    display_name = fields.Str(dump_only=True)

    class Meta:
        """Meta options."""
        strict = True

    @post_dump
    def format_data(self, data, **kwargs):
        """Format location/size as lists and set name from display_name if empty."""
        # Format location
        if "locationX" in data and "locationY" in data:
            data["location"] = [data.pop("locationX"), data.pop("locationY")]
        # Format size
        if "sizeX" in data and "sizeY" in data:
            data["size"] = [data.pop("sizeX"), data.pop("sizeY")]
        # Set name to display_name if name is empty
        if not data.get("name") and data.get("display_name"):
            data["name"] = data["display_name"]
        return data


class RoomListSchema(Schema):
    """Schema for room list response with optional availability."""

    rooms = fields.Nested(RoomSchema, many=True)
    availability_at = fields.DateTime()

    class Meta:
        """Meta options."""
        strict = True