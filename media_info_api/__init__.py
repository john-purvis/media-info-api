# media_info_api/__init__.py
import os

from dotenv import load_dotenv
from flask import Flask

from media_info_api.config import DevelopmentConfig, ProductionConfig, TestingConfig
from media_info_api.media.models import Catalog, Media, User
from media_info_api.media.routes import media_bp


def create_app(config_name="development"):
    # read the OS environment variable BEFORE loading .env
    env = os.environ.get("APP_ENV", "development").lower()

    # only overwrite existing variables when not in production
    if env != "production":
        load_dotenv(override=True)
    else:
        load_dotenv(override=False)

    print("Media info starting...")
    media_app = Flask(__name__)

    config_classes = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    media_app.config.from_object(config_classes[config_name])
    DEBUG                      = media_app.config["DEBUG"]
    JSON_SORT_KEYS             = media_app.config["JSON_SORT_KEYS"]
    DATABASE                   = media_app.config["DATABASE"]
    SQLALCHEMY_DATABASE_URI    = media_app.config["SQLALCHEMY_DATABASE_URI"]
    DATA_BASE_PATH             = media_app.config["DATA_BASE_PATH"]
    MEDIA_BASE_PATH            = media_app.config["MEDIA_BASE_PATH"]

    if DEBUG:
        print(f"Environment                      = {config_name}")
        print(f"    DEBUG                        = {DEBUG}")
        print(f"    JSON_SORT_KEYS               = {JSON_SORT_KEYS}")
        print(f"    DATABASE                     = {DATABASE}")
        print(f"    SQLALCHEMY_DATABASE_URI      = {SQLALCHEMY_DATABASE_URI}")
        print(f"    DATA_BASE_PATH               = {DATA_BASE_PATH}")
        print(f"    MEDIA_BASE_PATH              = {MEDIA_BASE_PATH}")

    media_app.json.sort_keys = JSON_SORT_KEYS

    from media_info_api.common.extensions import media_db, migrate
    if DEBUG:
        print("Initializing SQLAchemy...")
    media_db.init_app(media_app)
    if DEBUG:
        print("    enabling migrations...")
    migrate.init_app(media_app, media_db)
    if DEBUG:
        print("Registering Blueprints...")
    media_app.register_blueprint(media_bp, url_prefix="/media")

    @media_app.teardown_appcontext
    def close_db(exception: Exception):
        from flask import g
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @media_app.shell_context_processor
    def make_shell_context():
        return {"db": media_db, "Media": Media, "User": User, "Catalog": Catalog}

    @media_app.cli.command("seed-db")
    def seed_db():
        import click
        # prevent duplicate entries if run twice
        if User.query.filter_by(username="admin").first():
            click.echo("Database already seeded.")
            return

        users = \
            [
                User(
                    username = "admin",
                    password_hash = "scrypt:32768:8:1$uZa1xzDnKUa10bxS$1e7c06b8c608a4a19a378894af6b80abba5ff760e3f8b891e283b8614317b24dce03de0b6309a2c74fd56dcf5ed010a32d8fc4db943371529b232b94d62d641c",
                    is_admin = "True",
                    email = "admin@media_info.com",
                    phone = "5555555555"
                ),
                User(
                    id = 2,
                    username = "erica",
                    password_hash = "scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613687c3e0c476085339aa6",
                    is_admin = "False",
                    email = "erica@media_info.com",
                    phone = "5554444444"
                ),
                User(
                    id = 3,
                    username = "jerry",
                    password_hash = "scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613687c3e0c476085339aa6",
                    is_admin = "False",
                    email = "jerry@media_info.com",
                    phone = "5553333333"
                )
            ]
        media = \
            [
                Media(
                    id = 1,
                    catalog_id = 1,
                    user_id = 1,
                    type = "movie",
                    title = "The Matrix",
                    year = "1999",
                    duration = 8160,
                    certificate = "R",
                    genres = ["Action", "Sci-Fi"],
                    description = "A computer hacker discovers that his life is nothing more than an elaborate simulation run by an evil AI.",
                    imdb_id = "tt0133093",
                    tmdb_id = "603-the-matrix",
                    wiki_id = "The_Matrix"
                ),
                Media(
                    id = 2,
                    catalog_id = 2,
                    user_id = 2,
                    type = "movie",
                    title = "Liger",
                    year = "2021",
                    duration = 8400,
                    certificate = "PG-13",
                    genres = ["Action", "Drama", "Romance"],
                    description = "A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.",
                    imdb_id = "tt4435072",
                    tmdb_id = "787163",
                    wiki_id = "Liger"
                )
            ]
        catalog = \
            [
                Catalog(
                    id = 1,
                    media_id = 1,
                    date_created = "",
                    date_archived = "",
                    location = "local",
                    label = "",
                    file_media = "The Matrix (1999) [1080P.AMZN.X265.DDP-5.1].mkv",
                    file_media_nfo = "The Matrix (1999).nfo",
                    file_media_img = "The Matrix (1999).jpg",
                    path_media_rel = "/movies/[M-N]/Matrix, The (1999)",
                    path_media_sub = "/movies/[M-N]/Matrix, The (1999)/subs",
                    path_media_img = "/movies/[M-N]/Matrix, The (1999)/screens"
                ),
                Catalog(
                    id = 2,
                    media_id = 2,
                    date_created = "",
                    date_archived = "",
                    location = "archive",
                    label = "20261105-archive-disk-liger",
                    file_media = "Liger (2021) [1080P.WEBRIP.X265.AC3-5.1].mp4",
                    file_media_nfo = "Liger (2021).nfo",
                    file_media_img = "Liger (2021).jpg",
                    path_media_rel = "/media/movies/[K-L]/Liger (2021)",
                    path_media_sub = "/media/movies/[K-L]/Liger (2021)/subs",
                    path_media_img = "/media/movies/[K-L]/Liger (2021)/screens"
                )
            ]

        media_db.session.add_all(users)
        media_db.session.add_all(media)
        media_db.session.add_all(catalog)
        media_db.session.commit()
        click.echo("Database seeded successfully!")

    return media_app