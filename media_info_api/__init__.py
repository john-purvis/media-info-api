# media_info_api/__init__.py
import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from werkzeug.security import generate_password_hash

from media_info_api.config import DevelopmentConfig, ProductionConfig, TestingConfig
from media_info_api.media.models import Catalog, Media, User
from media_info_api.media.routes import media_bp, root_bp, users_bp


def create_app(config_name="development"):
    # read the OS environment variable BEFORE loading .env
    # APP_ENV should be set if running in 'production'
    env = os.environ.get("APP_ENV", config_name).lower()

    # only overwrite existing variables when not in production
    if env != "production":
        load_dotenv(override=True)
    else:
        load_dotenv(override=False)

    media_app = Flask(__name__)
    if env != "production":
        print("Flask started")

    config_classes = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    media_app.config.from_object(config_classes[config_name])

    DEBUG                      = media_app.config["DEBUG"]
    JSON_SORT_KEYS             = media_app.config["JSON_SORT_KEYS"]
    SECRET_KEY                 = media_app.config["SECRET_KEY"]
    # Default is HS256 (can also be HS384, HS512, RS256, etc.)
    JWT_ALGORITHM              = media_app.config["JWT_ALGORITHM"]
    JWT_SECRET_KEY             = media_app.config["JWT_SECRET_KEY"]
    JWT_EXPIRATION             = media_app.config["JWT_EXPIRATION"]
    DATABASE                   = media_app.config["DATABASE"]
    SQLALCHEMY_DATABASE_URI    = media_app.config["SQLALCHEMY_DATABASE_URI"]
    DATA_BASE_PATH             = media_app.config["DATA_BASE_PATH"]
    MEDIA_BASE_PATH            = media_app.config["MEDIA_BASE_PATH"]
    media_app.json.sort_keys   = JSON_SORT_KEYS

    if DEBUG:
        print(f"Environment                      = {config_name}")
        print(f"    DEBUG                        = {DEBUG}")
        print(f"    JSON_SORT_KEYS               = {JSON_SORT_KEYS}")
        print(f"    SECRET_KEY                   = {SECRET_KEY}")
        print(f"    JWT_ALGORITHM                = {JWT_ALGORITHM}")
        print(f"    JWT_SECRET_KEY               = {JWT_SECRET_KEY}")
        print(f"    JWT_EXPIRATION               = {JWT_EXPIRATION}")
        print(f"    DATABASE                     = {DATABASE}")
        print(f"    SQLALCHEMY_DATABASE_URI      = {SQLALCHEMY_DATABASE_URI}")
        print(f"    DATA_BASE_PATH               = {DATA_BASE_PATH}")
        print(f"    MEDIA_BASE_PATH              = {MEDIA_BASE_PATH}")

    from media_info_api.extensions import media_db, migrate
    media_db.init_app(media_app)
    if DEBUG:
        print("SQLAchemy initialized")

    with media_app.app_context():
        if media_db.engine.url.drivername == 'sqlite':
            # enable batch mode for sqlite to help solve
            # SQlite's ALTER TABLE and constraint limitations
            migrate.init_app(media_app, media_db, render_as_batch=True)
        else:
            migrate.init_app(media_app, media_db)
    if DEBUG:
        print("Migrations enabled")

    media_app.register_blueprint(root_bp)
    media_app.register_blueprint(media_bp, url_prefix="/media")
    media_app.register_blueprint(users_bp, url_prefix="/users")
    if DEBUG:
        print("Blueprints registered")

    # The securityDefinition below is used by Swagger to describe the
    # authentication mechanism for the API.
    # It creates the Authorize button and input box in the Swagger interface,
    # allowing users to input their JWT token for authenticated requests.
    swagger_data = {
        "swagger": "2.0",
        "info": {
            "title": "Recipe Book API",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "AuthKey": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your JWT token with the 'Bearer' prefix. Example: 'Bearer eyJhbGciOi...'",
                "example": "Bearer "
            }
        }
    }
    print("Initializing Swagger Docs...")
    swagger = Swagger(media_app, template=swagger_data)  # noqa: F841

    @media_app.teardown_appcontext
    def close_db(exception: Exception):
        from flask import g
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @media_app.shell_context_processor
    def make_shell_context():
        return {"db": media_db, "Media": Media, "User": User, "Catalog": Catalog}

    import click
    from flask.cli import with_appcontext
    # flask --app media_info_api get-hash <password>
    @media_app.cli.command("get-hash")
    @click.argument("password")
    @with_appcontext
    def get_hash(password):
        print(generate_password_hash(password))

    import click
    from flask.cli import with_appcontext
    # flask --app media_info_api seed-db
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
                    password_hash = "scrypt:32768:8:1$5R7INDNQbky3BuU4$412d8580f60609b886942f9891f7bbba8f17271a9fffd72d7d75bed5e52dddd650cdf3f2e6a592e7a63a2c966ad382908bb7222c0855eb58722cc447d438006a",
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
                    genres = "Action, Sci-Fi",
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
                    genres = "Action, Drama, Romance",
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
                    date_created = None,
                    date_archived = None,
                    location = "local",
                    label = "",
                    file_media = "The Matrix (1999) [1080P.BRRIP.X264].mp4",
                    file_media_nfo = "The Matrix (1999).nfo",
                    file_media_img = "The Matrix (1999).jpg",
                    path_media_rel = "/movies/[M-N]/Matrix, The (1999)",
                    path_media_sub = "/movies/[M-N]/Matrix, The (1999)/subs",
                    path_media_img = "/movies/[M-N]/Matrix, The (1999)/screens"
                ),
                Catalog(
                    id = 2,
                    media_id = 2,
                    date_created = None,
                    date_archived = None,
                    location = "archive",
                    label = "20261105-archive-disk-liger",
                    file_media = "Liger (2021) [XVID.HQ.AC3].avi",
                    file_media_nfo = "Liger (2021).nfo",
                    file_media_img = "Liger (2021).jpg",
                    path_media_rel = "/movies/[K-L]/Liger (2021)",
                    path_media_sub = "/movies/[K-L]/Liger (2021)/subs",
                    path_media_img = "/movies/[K-L]/Liger (2021)/screens"
                )
            ]

        media_db.session.add_all(users)
        media_db.session.add_all(media)
        media_db.session.add_all(catalog)
        media_db.session.commit()
        click.echo("Database seeded successfully!")

    # somewhere that runs after media_db and User are defined,
    # usually in the same file where you create the Flask app
    import click
    from flask.cli import with_appcontext
    @media_app.cli.command("promote-user")
    @click.argument("username")
    @with_appcontext
    def promote_user(username):
        """Promote a user to admin by username."""
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f"User '{username}' not found.")
            return

        user.is_admin = 1         # or True, depending how you store it
        user.role = "admin"       # keep role in sync
        media_db.session.commit()

        click.echo(f"User '{username}' promoted to admin.")

    import click
    from flask.cli import with_appcontext
    @media_app.cli.command("demote-user")
    @click.argument("username")
    @with_appcontext
    def demote_user(username):
        """Demote a user from admin by username."""
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f"User '{username}' not found.")
            return

        user.is_admin = 0         # or False, depending how you store it
        user.role = "user"       # keep role in sync
        media_db.session.commit()

        click.echo(f"User '{username}' demoted to user.")
    return media_app
