# common/utils.py
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


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

EASTERN_TZ = ZoneInfo("America/New_York")

def parse_to_naive_utc(
    date_str: str,
    assume_tz: ZoneInfo | timezone = EASTERN_TZ
) -> datetime | None:
    """
    Validates 'YYYY-MM-DD HH:MM:SS' or ISO 8601 strings.
    - If the string includes an offset (e.g. 'Z' or '-05:00'), it respects that offset.
    - If the string is naive (no offset), it assumes `assume_tz` (defaults to US Eastern).
    - Converts the result to UTC and strips tzinfo for SQLite/SQLAlchemy compatibility.
    """
    if not isinstance(date_str, str) or len(date_str) < 19:
        return None

    try:
        dt = datetime.fromisoformat(date_str)

        if dt.tzinfo is None:
            # Attach US Eastern; Python automatically picks EST (-5) or EDT (-4) based on the date
            dt = dt.replace(tzinfo=assume_tz)

        # Convert to UTC and strip tzinfo to match CURRENT_TIMESTAMP
        return dt.astimezone(timezone.utc).replace(tzinfo=None)  # noqa: UP017
    except ValueError:
        return None