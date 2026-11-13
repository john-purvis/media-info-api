# common/utils.py
import os


def clear_console():
    # 'nt' represents Windows; 'clear' handles macOS and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_console_ansi():
    # \033[H moves cursor to the top-left; \033[J clears the screen downward
    print("\033[H\033[J", end="")

def create_password_hash(password: str) -> str:
    # generates password hashes for use in our database
    # and is needed to seed the user data for application prep
    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)
    return password_hash

def create_sqlite_style_sample_date() -> str:
    # generates a SQLite style date format compatible with SQLite func.now()
    # this is also compatible with PostgreSQL DateTime(timezone=True)
    from datetime import datetime, timezone
    sqlite_style_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")  # noqa: UP017
    return sqlite_style_date