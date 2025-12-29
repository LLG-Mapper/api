from datetime import datetime, date
from app.models.enums import Frequency


def is_room_available(room, dt: datetime) -> bool:
    school_year_start = date(
        dt.year if dt.month >= 9 else dt.year - 1,
        9,
        1
    )
    week_index = ((dt.date() - school_year_start).days // 7)

    for cls in room.classes:
        # Time overlap
        if not (cls.start_time <= dt.time() <= cls.end_time):
            continue

        # Date range
        if cls.start_date > dt.date():
            continue
        if cls.end_date and dt.date() > cls.end_date:
            continue

        # One-off
        if cls.recurrence == Frequency.ONCE and cls.start_date == dt.date():
            return False

        # Day mismatch
        if cls.weekday != dt.weekday():
            continue

        # Weekly
        if cls.recurrence == Frequency.WEEKLY:
            return False

        # Biweekly
        if cls.recurrence == Frequency.BIWEEKLY_A and week_index % 2 == 0:
            return False
        if cls.recurrence == Frequency.BIWEEKLY_B and week_index % 2 == 1:
            return False

    return True