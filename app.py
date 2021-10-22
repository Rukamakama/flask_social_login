from flask import Flask
from flask_migrate import Migrate

from extensions import db
from views import auth_blueprint, app_blueprint


def create_app(testing=False):
    """Application factory, used to Flask application
    """
    app = Flask("Google Login App")
    app.config.from_object("config")
    if testing:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)
    return app


def configure_extensions(app):
    """configure flask extensions
    """
    from models import User, ConnectionHistory

    db.init_app(app)
    migrate = Migrate(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(app_blueprint)


if __name__ == '__main__':
    create_app().run()
