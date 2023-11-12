from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50))


class SARCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.Integer, db.ForeignKey('sar_category.id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('sar_status.id'), nullable=False)
    result = db.Column(db.Integer, db.ForeignKey('sar_result.id'), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    description_hidden = db.Column(db.Text, nullable=True)
    search_manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gpx_data = db.Column(db.Text, nullable=True)  # This will store GPX data as a text


class SARCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)

class SARResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)

class SARStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)

class GPSTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(7))  # Stores the color as a HEX code like #FF5733
    sar_call_id = db.Column(db.Integer, db.ForeignKey('sar_call.id'), nullable=False)
    sar_call = db.relationship('SARCall', backref=db.backref('gps_tracks', lazy=True))
