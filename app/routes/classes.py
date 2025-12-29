from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from ..models.class_ import Class
from ..extensions import db
from ..schemas import ClassSchema

bp = Blueprint("classes", __name__, url_prefix="/classes")
class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)


@bp.route("", methods=["GET"])
def list_classes():
    classes = Class.query.all()
    return jsonify(classes_schema.dump(classes))


@bp.route("/<int:class_id>", methods=["GET"])
def get_class(class_id):
    c = Class.query.get_or_404(class_id)
    return jsonify(class_schema.dump(c))


@bp.route("", methods=["POST"])
def create_class():
    try:
        data = class_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    c = Class(**data)
    db.session.add(c)
    db.session.commit()
    return jsonify(class_schema.dump(c)), 201


@bp.route("/<int:class_id>", methods=["PUT"])
def update_class(class_id):
    c = Class.query.get_or_404(class_id)
    try:
        data = class_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    for key, value in data.items():
        setattr(c, key, value)

    db.session.commit()
    return jsonify(class_schema.dump(c))


@bp.route("/<int:class_id>", methods=["DELETE"])
def delete_class(class_id):
    c = Class.query.get_or_404(class_id)
    db.session.delete(c)
    db.session.commit()
    return "", 204
