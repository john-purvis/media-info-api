# media_info_api/media/models.py
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import validates

from media_info_api.extensions import media_db
from media_info_api.utils import parse_to_naive_utc


class Media(media_db.Model):
    __tablename__ = "media"
    id = media_db.Column(media_db.Integer, primary_key=True)
    catalog_id = media_db.Column(media_db.Integer, nullable=True, unique=True) # must be nullable for media create and catalog create
    user_id = media_db.Column(media_db.Integer, nullable=False)
    type = media_db.Column(media_db.Text, nullable=False)                       # movie, tv_series, tv_episode
    title = media_db.Column(media_db.Text, nullable=False, unique=True)
    year = media_db.Column(media_db.Integer, nullable=True)
    duration = media_db.Column(media_db.Integer, nullable=True)                 # duration in seconds
    certificate = media_db.Column(media_db.Text, nullable=True)                 # "R", PG-13, TV-MA, etc
    genres = media_db.Column(media_db.Text, nullable=True)                      # comma delimited list of genres "Action", "Sci-Fi", etc
    description = media_db.Column(media_db.Text, nullable=True)                 # short description or plot
    imdb_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # IMDB id
    tmdb_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # TMDB id
    wiki_id = media_db.Column(media_db.Text, nullable=True, unique=True)        # Wikipedia id

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

    @validates("date_created")
    def validate_date_created(self, key, value):
        # Allow actual datetime objects to pass straight through
        if isinstance(value, datetime):
            return value
        parsed = parse_to_naive_utc(value)
        if not parsed:
            raise ValueError(f"user date_created -> invalid datetime string: {value}")
        return parsed

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