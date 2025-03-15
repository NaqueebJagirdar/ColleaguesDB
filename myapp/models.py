# myapp/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Colleague(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    country = db.Column(db.String(50))

class CalendarEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colleague_id = db.Column(db.Integer, db.ForeignKey('colleague.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    entry_type = db.Column(db.String(50))  # holiday, business_trip, etc.
    notes = db.Column(db.Text)
