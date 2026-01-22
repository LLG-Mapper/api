from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},  # dev only
        supports_credentials=False,
    )

    from .routes import (
        rooms_bp,
        classes_bp,
        buildings_bp,
        features_bp,
        # room_types_bp,
        # teachers_bp,
        # groups_bp,
        health_bp,
    )

    for bp in [
        rooms_bp,
        classes_bp,
        buildings_bp,
        features_bp,
        # room_types_bp,
        # teachers_bp,
        # groups_bp,
        health_bp,
    ]:
        app.register_blueprint(bp)

    return app
