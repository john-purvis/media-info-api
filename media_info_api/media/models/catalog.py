# media_info_api/media/models/catalog.py
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import validates

from media_info_api.extensions import media_db
from media_info_api.utils import parse_to_naive_utc


class Catalog(media_db.Model):
    __tablename__ = "catalog"
    id = media_db.Column(media_db.Integer, primary_key=True)
    media_id = media_db.Column(media_db.Integer, nullable=True, unique=True)            # must be nullable for catalog create and media create
    date_created = media_db.Column(media_db.DateTime, nullable=False, server_default=func.now())
    date_archived = media_db.Column(media_db.DateTime, nullable=True)
    location = media_db.Column(media_db.Text, nullable=True, unique=False)              # "archive", "local", "cloud"
    label = media_db.Column(media_db.Text, nullable=True, unique=False)                 # DVDR disc label, BVR disc label, disk volume label, or tape label
    # if location is "archived" this points to where it was when archived
    # if location is "local" then this is where it is currently
    file_media = media_db.Column(media_db.Text, nullable=True, unique=False)            # "The Matrix (1999) [1080P.AMZN.X265.DDP-5.1].mkv",
    file_media_nfo = media_db.Column(media_db.Text, nullable=True, unique=False)        # "The Matrix (1999).nfo",
    file_media_img = media_db.Column(media_db.Text, nullable=True, unique=False)        # The Matrix (1999).jpg"
    path_media_rel = media_db.Column(media_db.Text, nullable=True, unique=False)        # "/movies/[M-N]/Matrix, The (1999)"
    path_media_sub = media_db.Column(media_db.Text, nullable=True, unique=False)        # /movies/[M-N]/Matrix, The (1999)/subs
    path_media_img = media_db.Column(media_db.Text, nullable=True, unique=False)        # /movies/[M-N]/Matrix, The (1999)/screens

    @validates("date_created")
    def validate_date_created(self, key, value):
        # Allow actual datetime objects to pass straight through
        if isinstance(value, datetime):
            return value
        parsed = parse_to_naive_utc(value)
        if not parsed:
            raise ValueError(f"catalog date_created -> invalid datetime string: {value}")
        return parsed

    @validates("date_archived")
    def validate_date_archived(self, key, value):
        # Allow actual datetime objects to pass straight through
        if isinstance(value, datetime):
            return value
        parsed = parse_to_naive_utc(value)
        if not parsed:
            raise ValueError(f"catalog date_archived -> invalid datetime string: {value}")
        return parsed