from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# this line from stack overflow fixed a weird autoflush issue
db = SQLAlchemy(session_options={"autoflush": False})
# the passed in parameter allows
# type changes for model/class type changes
migrate = Migrate(compare_type=True)
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # import models for Alembic Setup
    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints Here
    from app.routes import video_bp
    app.register_blueprint(video_bp)

    from app.routes import customer_bp
    app.register_blueprint(customer_bp)

    from app.routes import rental_bp
    app.register_blueprint(rental_bp)

    return app
