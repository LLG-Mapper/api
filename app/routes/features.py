# api/routes/buildings.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from ..models.feature import Feature
from ..extensions import db
from ..schemas import FeatureSchema

bp = Blueprint("features", __name__, url_prefix="/features")
feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)


@bp.route("", methods=["GET"])
def list_features():
    features = Feature.query.all()
    return jsonify(features_schema.dump(features))


@bp.route("", methods=["POST"])
def create_feature():
    try:
        data = feature_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    feature = Feature(**data)
    db.session.add(feature)
    db.session.commit()
    return jsonify(feature_schema.dump(feature)), 201


@bp.route("/<int:feature_id>", methods=["GET"])
def get_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    return jsonify(feature_schema.dump(feature))

@bp.route("/<int:feature_id>", methods=["PUT"])
def update_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    try:
        data = feature_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(feature, key, value)

    db.session.commit()
    return jsonify(feature_schema.dump(feature))


@bp.route("/<int:feature_id>", methods=["DELETE"])
def delete_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    db.session.delete(feature)
    db.session.commit()
    return "", 204
