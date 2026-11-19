# media_info_api/config.py
import os
from pathlib import Path


class Config:
    JSON_SORT_KEYS = os.environ.get("JSON_SORT_KEYS") == "True"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # Default is HS256 (can also be HS384, HS512, RS256, etc.)
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_EXPIRATION = os.environ.get("JWT_EXPIRATION")
class DevelopmentConfig(Config):
    DEBUG = os.environ.get("DEV_DEBUG") == "True"
    db_name = os.environ.get("DEV_MEDIA_DATABASE")
    if not db_name:
        raise RuntimeError("DEV_MEDIA_DATABASE environment variable is required")
    # Force absolute path to root ignoring any crazy instance logic
    DATA_BASE_PATH = Path(__file__).resolve().parent.parent
    DATABASE = DATA_BASE_PATH / db_name
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_BASE_PATH = os.environ.get("DEV_MEDIA_BASE_PATH")
    if not MEDIA_BASE_PATH:
        raise RuntimeError("DEV_MEDIA_BASE_PATH environment variable is required")

class TestingConfig(Config):
    DEBUG = os.environ.get("TST_DEBUG") == "True"
    db_name = os.environ.get("TST_MEDIA_DATABASE")
    if not db_name:
        raise RuntimeError("TST_MEDIA_DATABASE environment variable is required")
    # Force absolute path to root ignoring any instance logic
    DATA_BASE_PATH = Path(__file__).resolve().parent.parent
    DATABASE = DATA_BASE_PATH / db_name
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_BASE_PATH = os.environ.get("TST_MEDIA_BASE_PATH")
    if not MEDIA_BASE_PATH:
        raise RuntimeError("TST_MEDIA_BASE_PATH environment variable is required")

class ProductionConfig(Config):
    DEBUG = os.environ.get("PRD_DEBUG") == "False"
    db_name = os.environ.get("PRD_MEDIA_DATABASE")
    if not db_name:
        raise RuntimeError("PRD_MEDIA_DATABASE environment variable is required")
    # Force absolute path to root ignoring any instance logic
    DATA_BASE_PATH = Path(__file__).resolve().parent.parent
    DATABASE = DATA_BASE_PATH / db_name
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_BASE_PATH = os.environ.get("PRD_MEDIA_BASE_PATH")
    if not MEDIA_BASE_PATH:
        raise RuntimeError("PRD_MEDIA_BASE_PATH environment variable is required")
