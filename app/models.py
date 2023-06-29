from app import db, ma
from dataclasses import dataclass


@dataclass
class Cities(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    country: str = db.Column(db.Text)
    name: str = db.Column(db.Text)
    lat: str = db.Column(db.Text)
    lng: str = db.Column(db.Text)
    area: str = db.Column(db.Text)

class CitiesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cities
