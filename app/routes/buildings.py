# api/routes/buildings.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from ..models.building import Building
from ..extensions import db
from ..schemas import BuildingSchema

bp = Blueprint("buildings", __name__, url_prefix="/buildings")
building_schema = BuildingSchema()
buildings_schema = BuildingSchema(many=True)


@bp.route("", methods=["GET"])
def list_buildings():
    buildings = Building.query.all()
    return jsonify(buildings_schema.dump(buildings))


@bp.route("", methods=["POST"])
def create_building():
    try:
        data = building_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    building = Building(**data)
    db.session.add(building)
    db.session.commit()
    return jsonify(building_schema.dump(building)), 201


@bp.route("/<int:building_id>", methods=["GET"])
def get_building(building_id):
    building = Building.query.get_or_404(building_id)
    return jsonify(building_schema.dump(building))


@bp.route("/<int:building_id>", methods=["PUT"])
def update_building(building_id):
    building = Building.query.get_or_404(building_id)
    try:
        data = building_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(building, key, value)

    db.session.commit()
    return jsonify(building_schema.dump(building))


@bp.route("/<int:building_id>", methods=["DELETE"])
def delete_building(building_id):
    building = Building.query.get_or_404(building_id)
    db.session.delete(building)
    db.session.commit()
    return "", 204
