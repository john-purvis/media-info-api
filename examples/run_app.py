# run Flask app (No Application Factory)

import os

from dotenv import load_dotenv

if os.environ.get("APP_ENV", "development").lower() != "production":
    load_dotenv(override=True)

from media_info_api import app  # Imports the already-initialized Flask instance

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)