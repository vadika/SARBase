from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))
    def __repr__(self):
        return self.username

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return self.name  # This is so that when we print the Role class, it will print the name instead of the object memory address


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
    search_manager = db.relationship('User', backref=db.backref('sar_calls', lazy=True))

class SARCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name  # Assuming 'name' is the field you want to display

class SARResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name  # Assuming 'name' is the field you want to display

class SARStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    def __repr__(self):
        return self.name  # Assuming 'name' is the field you want to display

class GPSTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(7))  # Stores the color as a HEX code like #FF5733
    sar_call_id = db.Column(db.Integer, db.ForeignKey('sar_call.id'), nullable=False)
    sar_call = db.relationship('SARCall', backref=db.backref('gps_tracks', lazy=True))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    gpx_data = db.Column(db.Text (length=4294967295) , nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    sar_call_id = db.Column(db.Integer, db.ForeignKey('sar_call.id'), nullable=False)
    sar_call = db.relationship('SARCall', backref=db.backref('comments', lazy=True))
