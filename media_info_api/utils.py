
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