# myapp/seed_calendar.py
from datetime import date
from myapp.__main__ import app, db, Colleague, CalendarEntry

def seed_calendar():
    with app.app_context():
        # Suppose colleague_id=1 is "Christoph Hilling"
        # We'll mark Jan 5th as "Holiday" for demonstration
        holiday = CalendarEntry(
            colleague_id=1,
            date=date(2025, 1, 5),
            entry_type="Holiday",
            notes="Personal day"
        )
        db.session.add(holiday)
        db.session.commit()

        print("Seeded calendar entries!")

if __name__ == "__main__":
    seed_calendar()
