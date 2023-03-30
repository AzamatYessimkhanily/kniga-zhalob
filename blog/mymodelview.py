from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

from blog import User2, db
from blog.models import Post2


# create custom view class
class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == 'admin':
            return True
        return False

# create admin and add your models
admin = Admin(name='My App', template_mode='bootstrap3')
admin.add_view(AdminView(User2, db.session))
admin.add_view(AdminView(Post2, db.session))
