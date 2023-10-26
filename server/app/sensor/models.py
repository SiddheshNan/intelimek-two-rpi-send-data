from app.extensions import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    values = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(DateTime(timezone=True), server_default=func.now())

    def serialize(self):
        return {'name': self.name, 'values': self.values, 'timestamp': self.timestamp}

    def __repr__(self):
        return f'<Sensor {self.serialize()}>'
