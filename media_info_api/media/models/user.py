# media_info_api/media/models/user.py
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import validates

from media_info_api.extensions import media_db
from media_info_api.utils import parse_to_naive_utc


class User(media_db.Model):
    __tablename__ = "users"
    id = media_db.Column(media_db.Integer, primary_key=True)
    username = media_db.Column(media_db.Text, nullable=False, unique=True)
    password_hash = media_db.Column(media_db.Text, nullable=False, server_default="")
    role = media_db.Column(media_db.Text, nullable=False, server_default="user")
    is_admin = media_db.Column(media_db.Integer, nullable=False, server_default="0")
    email = media_db.Column(media_db.Text, nullable=False, unique=True)
    phone = media_db.Column(media_db.Text, nullable=True, unique=False)
    date_created = media_db.Column(media_db.DateTime, nullable=False, server_default=func.now())

    # Optional: access a user's media via user.media_items
    media_items = media_db.relationship("Media", back_populates="user")

    @validates("date_created")
    def validate_date_created(self, key, value):
        # Allow actual datetime objects to pass straight through
        if isinstance(value, datetime):
            return value
        parsed = parse_to_naive_utc(value)
        if not parsed:
            raise ValueError(f"user date_created -> invalid datetime string: {value}")
        return parsed
