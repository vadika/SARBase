from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import User, SARCall, SARCategory, GPSTrack

admin = Admin(app, name='SAR Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(SARCall, db.session))
admin.add_view(ModelView(SARCategory, db.session))
admin.add_view(ModelView(GPSTrack, db.session))
