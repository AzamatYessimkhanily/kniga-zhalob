from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from blog.models import User2
from blog.database import db





db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()



login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    @login_manager.user_loader
    def load_user(user_id):
        return User2.query.get(int(user_id))

    from blog.main.routes import main
    from blog.user.routes import users
    from blog.post.routes import posts


    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)


    return app

