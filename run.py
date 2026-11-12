# run Flask app (with Application Factory)

import os

from dotenv import load_dotenv

# check the environment BEFORE loading .env to prevent overriding production vars
env = os.environ.get("APP_ENV", "development").lower()
if env != "production":
    load_dotenv(override=True)
else:
    load_dotenv(override=False)

# import the Flask app or factory AFTER environment variables are loaded
from media_info_api import create_app

app = create_app()

# 3. Run the built-in development server only when executed directly
if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(host=host, port=port, debug=debug)
