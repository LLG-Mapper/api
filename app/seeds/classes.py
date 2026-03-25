import json
from pathlib import Path
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import (
    Building,
    Room,
    Class,
)

app = create_app()

DATA = Path(__file__).parent.parent.parent / "data"
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
    with open(CLASSES, encoding="utf-8") as f:
        classes = json.load(f)

    # -------------------------
    # Seed Classes
    # -------------------------
    from datetime import datetime

    for c in classes:
        room_code = c["room"]  # e.g. "M209"

        # ---- Parse structured room code ----
        building_code = room_code[0:-3]             # "M"
        floor = int(room_code[-3])                  # 2
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
            print(f"Room {room_code} in {building.name} on the {floor}th floor: {number}. Not found in DB.")
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

    print("Classes seeded successfully.")