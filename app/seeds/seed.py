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
CLASSES = DATA / "classes.json"


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

    with open(CLASSES, encoding="utf-8") as f:
        classes = json.load(f)

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
        building = get_or_create(Building, code=b["code"], defaults={"name": b["name"]})

        for r in b.get("rooms", []):
            type_code = r.get("type", "CLASS")
            room_type = room_type_objs[type_code]

            print(r["floor"])
            room = Room(
                number=r["number"],
                floor=r["floor"],
                capacity=r.get("capacity"),
                name=r.get("name"),
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
    # -------------------------
    # Seed Classes
    # -------------------------
    from datetime import datetime

    for c in classes:
        room_code = c["room"]  # e.g. "M209"

        # ---- Parse structured room code ----
        building_code = room_code[0:-3]          # "M"
        floor = int(room_code[-3])             # 2
        number = int(room_code[-2:])                # "09"

        # ---- Fetch building ----
        building = Building.query.filter_by(code=building_code).first()
        if not building:
            print(f"Building {building_code} not found.")
            continue

        # ---- Fetch room ----
        room = Room.query.filter_by(
            building_id=building.id,
            floor=floor,
            number=number
        ).first()

        if not room:
            print(f"Room {room_code} not found in DB.")
            continue

        # ---- Avoid duplicates ----
        existing = Class.query.filter_by(
            room_id=room.id,
            start_time=datetime.strptime(c["start_time"], "%H:%M:%S").time(),
            weekday=c["weekday"]
        ).first()

        if existing:
            continue

        new_class = Class(
            room_id=room.id,
            teacher_id=1,  # Placeholder
            group_id=1,    # Placeholder
            subject_id=1,  # Placeholder
            start_date=datetime.strptime(c["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(c["end_date"], "%Y-%m-%d").date(),
            start_time=datetime.strptime(c["start_time"], "%H:%M:%S").time(),
            end_time=datetime.strptime(c["end_time"], "%H:%M:%S").time(),
            recurrence=c["recurrence"],  # e.g. "WEEKLY"
            weekday=c["weekday"],
        )

        db.session.add(new_class)

    db.session.commit()

    print("Database seeded successfully.")
