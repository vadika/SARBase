from datetime import datetime

from flask_login import UserMixin

from app import db


class SARCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    start_date = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.Integer, db.ForeignKey('sar_category.id'), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('sar_status.id'), nullable=False)
    result = db.Column(db.Integer, db.ForeignKey('sar_result.id'), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude_found = db.Column(db.Float, nullable=True)
    longitude_found = db.Column(db.Float, nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    description_hidden = db.Column(db.Text, nullable=True)
    search_officer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    coordination_officer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    search_officer = db.relationship('User', back_populates='search_sar_calls', foreign_keys=[search_officer_id])
    coordination_officer = db.relationship('User', back_populates='coordination_sar_calls',
                                           foreign_keys=[coordination_officer_id])

    def __repr__(self):
        return self.title


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    username = db.Column(db.String(150), unique=True, nullable=False)
    full_name = db.Column(db.String(301), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')
    search_sar_calls = db.relationship('SARCall', back_populates='search_officer',
                                       foreign_keys=[SARCall.search_officer_id])
    coordination_sar_calls = db.relationship('SARCall', back_populates='coordination_officer',
                                             foreign_keys=[SARCall.coordination_officer_id])

    def __repr__(self):
        return self.username


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return self.name  # Assuming 'name' is the field you want to display


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
    file_name = db.Column(db.String(255), nullable=False)
    gpx_name = db.Column(db.Text, nullable=True)
    gpx_data = db.Column(db.Text(length=4294967295), nullable=True)
    color = db.Column(db.String(7))  # Stores the color as a HEX code like #FF5733
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    comment = db.relationship('Comment', backref=db.backref('gps_track', lazy=True))
    sar_call_id = db.Column(db.Integer, db.ForeignKey('sar_call.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    text = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    sar_call_id = db.Column(db.Integer, db.ForeignKey('sar_call.id'), nullable=False)
    sar_call = db.relationship('SARCall', backref=db.backref('comments', lazy=True))


class FileAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)

    def is_image(self):
        return self.file_type in ['image/jpeg', 'image/png', 'image/gif']