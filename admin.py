from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db
from models import User, Role, SARCall, Comment, SARCategory, GPSTrack, SARStatus, SARResult, FileAttachment

class AdminModelView(ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated and current_user.role.name == "admin"
        return True


class UserModelView(AdminModelView):
    # Display human-readable names for foreign keys
    column_list = ('id', 'username', 'full_name', "email", "phone_number", "role.name", "password")
    column_labels = {'role.name': 'user role'}

    # Allow searching and filtering by related fields
    column_searchable_list = ('role.name', 'username', 'full_name', "email", "phone_number")
    column_filters = ('role.name', 'username', 'full_name', "email", "phone_number")



admin = Admin(app, name='SAR Admin', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(AdminModelView(SARCall, db.session))
admin.add_view(AdminModelView(Comment, db.session))
admin.add_view(AdminModelView(GPSTrack, db.session))
admin.add_view(AdminModelView(FileAttachment, db.session))
admin.add_view(AdminModelView(Role, db.session, category="Dictionaries"))
admin.add_view(AdminModelView(SARCategory, db.session, category="Dictionaries"))
admin.add_view(AdminModelView(SARStatus, db.session, category="Dictionaries"))
admin.add_view(AdminModelView(SARResult, db.session, category="Dictionaries"))
