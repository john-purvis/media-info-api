# media_info_api/extensions.py

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, event
from sqlalchemy.engine import Engine

# Define the convention template
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Instantiate SQLAlchemy WITH the metadata/convention right away
metadata = MetaData(naming_convention=convention)

media_db = SQLAlchemy(metadata=metadata)

# NOTE: migration batch mode COULD be enabled here to help
# SQlite's ALTER TABLE and constraint limitations using

# Migrate(app=app, db=media_db, render_as_batch=True)
# Migrate(db=media_db, render_as_batch=True)

# HOWEVER, we need the app for that AND enabling it here
# would enable it for SQLite, PostgreSQL, etc
# So it is usually done in _init_.py so it can be enabled
# only for SQLite...see _init_.py
migrate = Migrate()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
  cursor = dbapi_connection.cursor()
  cursor.execute("PRAGMA foreign_keys=ON")
  cursor.close()