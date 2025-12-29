from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from datetime import datetime

from ..models.room import Room
from ..models.feature import Feature
from ..extensions import db
from ..schemas import RoomSchema

bp = Blueprint("rooms", __name__, url_prefix="/rooms")
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)


@bp.route("", methods=["GET"])
def list_rooms():
    query = Room.query.options(selectinload(Room.classes))

    # Filters
    building_id = request.args.get("building_id", type=int)
    floor = request.args.get("floor", type=int)
    feature_codes = request.args.getlist("feature_codes")

    availability_at = (
        request.args.get(
            "availability_at",
            type=lambda v: datetime.fromisoformat(v)
        )
        if request.args.get("availability_at")
        else None
    )

    is_available = (
        request.args.get("is_available").lower() == "true"
        if request.args.get("is_available")
        else None
    )

    # SQL-level filters
    if building_id is not None:
        query = query.filter(Room.building_id == building_id)

    if floor is not None:
        query = query.filter(Room.floor == floor)

    if feature_codes:
        query = (
            query
            .join(Room.features)
            .filter(Feature.code.in_(feature_codes))
        )

    rooms = query.distinct().all()

    # Python-level availability logic
    result = []
    for room in rooms:
        room_dict = room_schema.dump(room)

        if availability_at is not None:
            availability = room.is_available_at(availability_at)
            room_dict["is_available"] = availability

            if is_available is not None and availability != is_available:
                continue

        result.append(room_dict)

    payload = (
        {"availability_at": availability_at.isoformat(), "rooms": result}
        if availability_at is not None
        else result
    )

    return jsonify(payload)


@bp.route("/<int:room_id>", methods=["GET"])
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return jsonify(room_schema.dump(room))


@bp.route("", methods=["POST"])
def create_room():
    try:
        data = room_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Extract feature_ids if provided separately
    feature_ids = request.get_json().get("feature_ids", [])

    room = Room(
        number=data["number"],
        name=data.get("name"),
        building_id=data["building_id"],
        floor=data["floor"],
        capacity=data.get("capacity"),
        is_open=data.get("is_open", True),
        type_id=data["type_id"],
        locationX=data["locationX"],
        locationY=data["locationY"],
        sizeX=data["sizeX"],
        sizeY=data["sizeY"],
    )

    if feature_ids:
        room.features = Feature.query.filter(
            Feature.id.in_(feature_ids)
        ).all()

    db.session.add(room)
    db.session.commit()

    return jsonify(room_schema.dump(room)), 201


@bp.route("/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    try:
        data = room_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for field in [
        "number", "name", "floor", "capacity", "is_open", "type_id",
        "locationX", "locationY", "sizeX", "sizeY"
    ]:
        if field in data:
            setattr(room, field, data[field])

    feature_ids = request.get_json().get("feature_ids")
    if feature_ids is not None:
        room.features = Feature.query.filter(
            Feature.id.in_(feature_ids)
        ).all()

    db.session.commit()
    return jsonify(room_schema.dump(room))


@bp.route("/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return "", 204