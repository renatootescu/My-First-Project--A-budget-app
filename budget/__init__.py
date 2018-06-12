# the __init__.py file tells Python that this is a package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # module to create the db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from budget.config import Config


db = SQLAlchemy()  # the database is created using SQLAlchemy
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from budget.users.routes import users  # this it the name of the variable in the users routes the is the instance of the Blueprint class
    from budget.posts.routes import posts
    from budget.main.routes import main
    from budget.errors.handlers import errors
    app.register_blueprint(users)  # registering the users blueprint
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app


db.create_all(app=create_app())
