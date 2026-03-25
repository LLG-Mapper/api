import json
from pathlib import Path
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import (
    Building,
    Room,
    RoomType,
    Feature,
    Class,
)

app = create_app()

DATA = Path(__file__).parent.parent.parent / "data"
ROOM_TYPES = DATA / "room_types.json"
FEATURES = DATA / "features.json"
ROOMS = DATA / "rooms.json"


def get_or_create(model, defaults=None, **kwargs):
    """Helper: get or create an object by filter."""
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    params = dict(**kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    db.session.commit()
    return instance


with app.app_context():
    # Load JSONs
    with open(ROOM_TYPES, encoding="utf-8") as f:
        room_types = json.load(f)

    with open(FEATURES, encoding="utf-8") as f:
        features = json.load(f)

    with open(ROOMS, encoding="utf-8") as f:
        rooms = json.load(f)

    # -------------------------
    # Seed RoomTypes
    # -------------------------
    room_type_objs = {}
    for rt in room_types:
        obj = get_or_create(RoomType, code=rt["code"], defaults={"name": rt["name"]})
        room_type_objs[obj.code] = obj

    # -------------------------
    # Seed Features
    # -------------------------
    feature_objs = {}
    for f_data in features:
        obj = get_or_create(Feature, code=f_data["code"], defaults={"name": f_data["name"]})
        feature_objs[obj.code] = obj

    # -------------------------
    # Seed Buildings and Rooms
    # -------------------------
    for b in rooms:
        building = get_or_create(Building, code=b["code"], defaults={"name": b["name"], "floor": b.get("floor", 0)})
        print(f"Seeding rooms for building {building.name}...")
        for r in b.get("rooms", []):
            type_code = r.get("type", "CLASS")
            room_type = room_type_objs[type_code]

            room = Room(
                number=r["number"],
                floor=r["floor"],
                capacity=r.get("capacity", 0),
                name=r.get("name", None),
                building=building,
                type=room_type,
                is_open=r.get("is_open", True),
                path=r.get("path", "")
            )
            db.session.add(room)
            db.session.commit()

            # Assign features
            room.features = [
                feature_objs[f_code]
                for f_code in r.get("features", [])
                if f_code in feature_objs
            ]
            db.session.commit()
    
    db.session.commit()

    print("Rooms seeded successfully.")
