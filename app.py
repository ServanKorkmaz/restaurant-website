import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_proto=1, x_host=1
)  # needed for url_for to generate with https

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

# Initialize extensions
db = SQLAlchemy(app, model_class=Base)
login_manager = LoginManager(app)
login_manager.login_view = "admin.login"


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


# Create tables
with app.app_context():
    import models  # noqa: F401

    db.create_all()
    logging.info("Database tables created")

# Import routes to register them
import routes  # noqa: F401

# Import and register admin blueprint
from admin_routes import admin_bp
app.register_blueprint(admin_bp)
