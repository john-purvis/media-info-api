# media_info_api/common/db.py
import sqlite3

from flask import current_app, g

from media_info_api.media.models import Catalog, Media, User


def mock_user(id: int) -> dict:
    users = \
        [
            {
                "id": 0,
                "username": "",
                "password_hash": "",
                "is_admin": "",
                "email": "",
                "phone": ""
            },
            {
                "id": 1,
                "username": "admin",
                "password_hash": "scrypt:32768:8:1$uZa1xzDnKUa10bxS$1e7c06b8c608a4a19a378894af6b80abba5ff760e3f8b891e283b8614317b24dce03de0b6309a2c74fd56dcf5ed010a32d8fc4db943371529b232b94d62d641c",
                "is_admin": "True",
                "email": "admin@media_info.com",
                "phone": "5551231234"
            },
            {
                "id": 2,
                "username": "erica",
                "password_hash": "scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613687c3e0c476085339aa6",
                "is_admin": "False",
                "email": "erica@media_info.com",
                "phone": "5554444444"
            },
            {
                "id": 3,
                "username": "jerry",
                "password_hash": "scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613687c3e0c476085339aa6",
                "is_admin": "False",
                "email": "jerry@media_info.com",
                "phone": "5553333333"
            }
        ]
    return users[id]

def mock_media(id: int) -> dict:
    media = \
        [
            {
                "id": 0,
                "catalog_id": 0,
                "user_id": 0,
                "type": "",
                "title": "",
                "year": "",
                "duration": 0000,
                "certificate": "",
                "genres": "",
                "description": "",
                "imdb_id": "",
                "tmdb_id": "",
                "wiki_id": ""
            },
            {
                "id": 1,
                "catalog_id": 1,
                "user_id": 1,
                "type": "movie",
                "title": "The Matrix",
                "year": "1999",
                "duration": 8160,
                "certificate": "R",
                "genres": ["Action", "Sci-Fi"],
                "description": "A computer hacker discovers that his life is nothing more than an elaborate simulation run by an evil AI.",
                "imdb_id": "tt0133093",
                "tmdb_id": "603-the-matrix",
                "wiki_id": "The_Matrix"
            },
            {
                "id": 2,
                "catalog_id": 2,
                "user_id": 2,
                "type": "movie",
                "title": "Liger",
                "year": "2021",
                "duration": 8400,
                "certificate": "PG-13",
                "genres": ["Action", "Drama", "Romance"],
                "description": "A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.",
                "imdb_id": "tt4435072",
                "tmdb_id": "787163",
                "wiki_id": "Liger"
            }
        ]
    return media[id]

def mock_catalog(id: int) -> dict:
    catalog = \
        [
            {
                "id": 0,
                "media_id": 0,
                "date_created": "",
                "date_archived": "",
                "location": "",
                "label": "",
                "file_media": "",
                "file_media_nfo": "",
                "file_media_img": "",
                "path_media_rel": "",
                "path_media_sub": "",
                "path_media_img": ""
            },
            {
                "id": 1,
                "media_id": 1,
                "date_created": "",
                "date_archived": "",
                "location": "local",
                "label": "",
                "file_media": "The Matrix (1999) [1080P.AMZN.X265.DDP-5.1].mkv",
                "file_media_nfo": "The Matrix (1999).nfo",
                "file_media_img": "The Matrix (1999).jpg",
                "path_media_rel": "/movies/[M-N]/Matrix, The (1999)",
                "path_media_sub": "/movies/[M-N]/Matrix, The (1999)/subs",
                "path_media_img": "/movies/[M-N]/Matrix, The (1999)/screens"
            },
            {
                "id": 2,
                "media_id": 2,
                "date_created": "",
                "date_archived": "",
                "location": "archive",
                "label": "20261105-archive-disk-liger",
                "file_media": "Liger (2021) [1080P.WEBRIP.X265.AC3-5.1].mp4",
                "file_media_nfo": "Liger (2021).nfo",
                "file_media_img": "Liger (2021).jpg",
                "path_media_rel": "/media/movies/[K-L]/Liger (2021)",
                "path_media_sub": "/media/movies/[K-L]/Liger (2021)/subs",
                "path_media_img": "/media/movies/[K-L]/Liger (2021)/screens"
            }
        ]
    return catalog[id]


def media_to_dict(media: Media):
    if not media:
        return None

    return {
        "id": media.id,
        "type": media.type,
        "title": media.title,
        "year": media.year,
        "duration": media.duration,
        "certificate": media.certificate,
        "genres": media.genres,
        "description": media.description,
        "imdb_id": media.imdb_id,
        "tmdb_id": media.tmdb_id,
        "wiki_id": media.wiki_id,

        "catalog_id": media.catalog_id,
        "user_id": media.user_id,

    }

def catalog_to_dict(catalog: Catalog):
    if not catalog:
        return None

    return {
        "date_created": catalog.date_created,
        "date_archived": catalog.date_archived,
        "location": catalog.location,
        "label": catalog.label,
        "file_media": catalog.file_media,
        "file_media_nfo": catalog.file_media_nfo,
        "file_media_img": catalog.file_media_img,
        "path_media_rel": catalog.path_media_rel,
        "path_media_sub": catalog.path_media_sub,
        "path_media_img": catalog.path_media_img
    }

def user_to_dict(user: User):
    if not user:
        return None

    return {
        "id": user.id,
        "username": user.username,
        "password_hash": user.password_hash,
        "is_admin": user.is_admin,
        "email": user.email,
        "phone": user.phone
    }

def row_to_dict(row):
    """
    Convert a SQLite row object to a dictionary.
    This function dynamically builds a dictionary from the row's keys and values,
    ensuring that only the columns present in the row are included.
    """
    if not row:
        return None

    json_str = {key: row[key] for key in row.keys()}  # noqa: SIM118

    return json_str

def get_db():
    if "db" not in g:
        db_path = current_app.config["DATABASE"]
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db
