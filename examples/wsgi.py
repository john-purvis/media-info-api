import os

from dotenv import load_dotenv

# load .env safely before importing the app
# Only override existing variables when NOT in production
if os.environ.get("APP_ENV", "development").lower() != "production":
    load_dotenv(override=True)
else:
    load_dotenv(override=False)

# import the application factory and instantiate the WSGI callable
from media_info_api import create_app

app = create_app()

# allow running locally with `python wsgi.py`
if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
