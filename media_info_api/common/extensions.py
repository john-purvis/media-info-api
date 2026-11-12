# media_info_api/common/extensions.pyd

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

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
migrate = Migrate()
