from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'hovedretter', 'ekstra', 'drikker', 'catering'
    image_filename = db.Column(db.String(100))
    webp_filename = db.Column(db.String(100))  # WebP version
    thumbnail_filename = db.Column(db.String(100))  # Thumbnail version
    alt_text = db.Column(db.String(200))  # Alt text for accessibility
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=True)  # Published status
    is_featured = db.Column(db.Boolean, default=False)  # Featured on homepage
    sort_order = db.Column(db.Integer, default=0)
    position = db.Column(db.Integer)  # For precise ordering
    allergens = db.Column(db.String(100))  # Comma-separated allergen numbers
    min_pax = db.Column(db.Integer)  # Minimum persons for catering
    features = db.Column(db.JSON)  # Features list for catering packages
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RestaurantInfo(db.Model):
    __tablename__ = 'restaurant_info'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)