<!-- media_info_api/README.md -->

# Media Info API for Maestro BE106


Owner: John Purvis

This backend manages media metadata records for movies and TV shows in a user’s personal collection. Each record stores basic details about the title along with where the files are stored, such as which disk or server. The owner uses this system to keep track of their library as drives fail or are migrated. The main action is to look up a movie or show they own and immediately see where to load it from.

## Setup


## Environment Variables

Listed below are the environment variables that must be setup in your .env file for the
application to run correctly in each environment: `"development"`, `"testing"`, and
`"production"`.  The environment must be passed in when you use the application factory
and call `create_app(config_name="development")`.

```python
[common]
PYTHONPATH=.
JSON_SORT_KEYS=False
SECRET_KEY=<FLASK SECRET KEY FOR SESSION COOKIES GOES HERE>
# Default is HS256 (can also be HS384, HS512, RS256, etc.)
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=<YOUR CRYPTOGRAPHIC KEY FOR JWT GOES HERE>
[development]
DEV_DEBUG=True
DEV_MEDIA_DATABASE=media-info-dev.db
DEV_MEDIA_BASE_PATH=/d/media
[testing]
TST_DEBUG=True
TST_MEDIA_DATABASE=media-info-tst.db
TST_MEDIA_BASE_PATH=/d/media
[production]
PRD_DEBUG=False
PRD_MEDIA_DATABASE=media-info.db
PRD_MEDIA_BASE_PATH=/d/media
```

### The SECRET KEY ###
Flask's SECRET_KEY (`app.config["SECRET_KEY"]`) is a cryptographic key used by core Flask and its extensions to digitally sign client-side data so users cannot tamper with it.
• What it protects. By default, Flask uses it to sign session cookies (`session["user_id"] = 1`), flash() messages, and CSRF tokens (via Flask-WTF).

### The JWT SECRET KEY
If you use symmetric signing (the default HS256 in Flask-JWT-Extended), the RFC 7518 security specification requires the secret key to be at least as long in bytes as the hash output:

| Algorithm | Minimum Key Length | Recommended Key Length |
| :--- | :--- | :--- |
| HS256 (Default) | 32 bytes (32 ASCII characters) | 32–64 bytes |
| HS384 | 48 bytes (48 ASCII characters) | 48–64 bytes
| HS512 | 64 bytes (64 ASCII characters) | 64+ bytes

• There are no forbidden characters in Python. Any UTF-8 character, letter, number, or symbol is valid because PyJWT encodes the string into UTF-8 bytes before signing.

• However, watch out for .env parsing rules. While Python accepts any character, python-dotenv treats unquoted # characters as comments and $ characters as variable interpolation.
```python
     • Safe practice
     Either wrap your key in single quotes in your .env file
     (JWT_SECRET_KEY='your-secret-here') or generate a URL-safe
     alphanumeric/hex string that contains no #, $, or spaces.
```
• You can generate a secure JWT SECRET KEY by running one of these one-liners in the terminal using Python's built-in secrets module to generate a cryptographically secure, .env-safe key:
```python
     • Hexadecimal string (64 characters / 32 bytes)
     python -c "import secrets; print(secrets.token_hex(32))"
```
```python
     • URL-safe Base64 string (43 characters / 32 bytes)
     python -c "import secrets; print(secrets.token_urlsafe(32))"
```
(Note: Keep JWT_SECRET_KEY separate from Flask's general SECRET_KEY. Changing JWT_SECRET_KEY immediately invalidates all currently active user tokens and forces everyone to log in again.)

## Migrations

### SQLite and PostgreSQL

If you use both SQLite (for development) and PostgreSQL (for production), refer to `MIGRATIONS - CONSIDERATIONS.md` for details on naming conventions and batch mode.

### Initial baseline setup (run once on this project)

On a fresh clone, before any other migrations:

1. Run the initial migration setup:
   ```bash
   flask db init
   ```
2. Apply the required edits to `migrations/alembic.ini` and `migrations/env.py` described in [MIGRATIONS - CONSIDERATIONS.md](<./MIGRATIONS%20-%20CONSIDERATIONS.md>).
3. Create the baseline revision:
   ```bash
   alembic -c migrations/alembic.ini revision --autogenerate -m "database baseline"
   ```
4. Apply the baseline to the database:
   ```bash
   alembic -c migrations/alembic.ini upgrade head
   ```

If you encounter errors in this process, see [MIGRATIONS - TROUBLESHOOTING.md](<./MIGRATIONS%20-%20TROUBLESHOOTING.md>).

### Ongoing migrations after model changes

After you change models:

```bash
flask db migrate -m "describe your change"
flask db upgrade
```

## Users (initial and test):

     user    : admin
     password: g0dM0d3
     hash    : scrypt:32768:8:1$5R7INDNQbky3BuU4$412d8580f60609b886942f9891f7bbba8f17
               271a9fffd72d7d75bed5e52dddd650cdf3f2e6a592e7a63a2c966ad382908bb7222c08
               55eb58722cc447d438006a


     user    : erica
     password: Pa55w0rd
     hash    : scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5
               de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613
               687c3e0c476085339aa6

     user    : jerry
     password: Pa55w0rd
     hash    : scrypt:32768:8:1$ZM6uOe9B6k14nGNN$b678a395cca1c960d8090719d2795d11b28a5
               de691dede7c24095b5daaca0c12fa2e3d79c1ba3f7979feded66c6d8e1c5fd4259fc613
               687c3e0c476085339aa6


## Endpoints

| Path | Method | Purpose | Success | Errors | Access |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/register` | POST | Create user account | 201 | 400 | public |
| `/login` | POST | Get auth token | 200 | 400, 401 | public |
| `/profile` | GET | Get personal profile | 200 | 400, 401 | logged in only |
| `/media` | GET | List media | 200 | 400, 401 | public |
| | POST | Create media | 201 | 400, 401, 403 | logged in only |
| `/media<id>` | GET | Get media by ID | 200 | 400, 401, 404 | public |
| | PUT | Update media by ID | 200 | 400, 401, 403, 404 | logged in only |
| | PATCH | Update media by ID | 200 | 400, 401, 403, 404 | logged in only |
| | DELETE | Delete media by ID | 204 | 400, 401, 403, 404 | logged in only |
| `/search` | GET | Search by data in body | 200 | 400, 401, 404 | public |

"logged in only" (Bearer <Authkey> required)


## Status codes

| Status | Meaning |
| :--- | :--- |
| 200 | OK |
| 201 | Created |
| 204 | No Content / Deleted |
| 400 | Bad Request / Missing Data |
| 401 | Unauthorized / Unauthenticated |
| 403 | Forbidden / No Access |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests |
| 500 | Internal Server Error |


## Try it

An authorization key is obtained via successful login and then must be included as
'-H "Authorization: Bearer <AuthKey>' for all other requests except registration.

================================================================================

Display the API landing page:
```
curl -i -X GET http://127.0.0.1:5000/
```
EXPECT:
     200 OK with html file contents

================================================================================

Display the API docs:
```
curl -i -X GET http://127.0.0.1:5000/apidocs/
```
EXPECT:
     200 OK with html doc contents

================================================================================

Register (create a user):
```
curl -i -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" \
     -d "{'username': 'testuser', 'password': 'test', 'email': 'test@testytester.com', 'phone': '5558675309'}"
```
EXPECT:
     200 OK with the user in JSON

================================================================================

Login to obtain a JWT token (used in following methods):
```
curl -i -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" \
     -d "{'username': 'testuser', 'password': 'test'}"
```
EXPECT:
     200 OK with token
     Note the token that is returned by login.  You will need this for routes requiring authorization.
     The token will look something like 'eyJhbGciOiJIUzI1NiIsInR5...'

================================================================================

Profile (get current user):
```
curl -i -X GET http://127.0.0.1:5000/profile -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES>'
```
Replace <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES> with your token returned by login

EXPECT:
     200 OK and the currently logged in user in JSON
     404 if not logged in (no token)

================================================================================

List media:
```
curl -i -X GET http://127.0.0.1:5000/media -H "Content-Type: application/json"
```
EXPECT:
     200 OK
     A list of the available media in JSON

================================================================================

Create your own media:
```
curl -i -X POST http://127.0.0.1:5000/media -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES>"
     -d "{'type': 'movie', 'IMDB_id': 'tt0133093', 'title': 'The Matrix', 'year': '1999', 'description': 'A computer hacker discovers that his life is nothing more than an elaborate simulation run by an evil AI.', 'genres': ['Action', 'Sci-Fi'], 'duration': 8160, 'certificate': 'R', 'location': 'disk', 'date:' '', 'disk': '', 'label': '', 'path': /media/movies/[M-N]/Matrix, The (1999)', 'file': 'The Matrix (1999) [1080P.AMZN.X265.DDP-5.1].mkv'}"

curl -i -X POST http://127.0.0.1:5000/media -H "Content-Type: application/json" \
     -H "Authorization: Bearer <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES>"
     -d "{'type': 'movie', 'IMDB_id': 'tt4435072', 'title': 'Liger', 'year': '2021', 'description': 'A story about martial arts, dreams and star crossed lovers. Liger is an MMA fighter who trains hard and rises up the ranks with one goal in mind, to fight like his idol, world renowned MMA fighter Mark Anderson and get noticed by him.', 'genres': ['Action', 'Drama', 'Romance'], 'duration': 8400, 'certificate': 'PG-13', 'location': 'backup', 'date:' '20261005', 'disk': '10', 'label': '2026105_10', 'path': '', 'file': ''}"
```
Replace <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES> with your token returned by login

EXPECT:
     201 with the newly created media in JSON

================================================================================

Get one media item:
```
curl -i -X GET http://127.0.0.1:5000/media/1
```
EXPECT:
     200 with media item in JSON


Get one media item (private):
```
curl -i -X GET http://127.0.0.1:5000/media/999
```
EXPECT:
     404 NOT FOUND

================================================================================

Update media item:
```
curl -i -X PATCH "http://localhost:5000/media/2" \
     -H "accept: application/json" \
     -H "Authorization: Bearer <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES>" \
     -H "Content-Type: application/json" -d "{'year': 2022 }"
```
EXPECT:
     200 and media item (if the current user owns the media item or is_admin)
     403 FORBIDDEN (if the current user does not own the media item)

================================================================================

Delete media item:
```
curl -i -X DELETE http://127.0.0.1:5000/media/2
     -H "accept: application/json" \
     -H "Authorization: Bearer <YOUR_TOKEN_FROM_LOGIN_WITHOUT_QUOTES>"
```
EXPECT:
     204 (if the current user owns the media item or is_admin)
     403 FORBIDDEN (if the current user does not own the media item)

================================================================================

Search media:
```
curl -i -X GET "http://localhost:5000/users" \
     -H "accept: application/json" \
     -d "{'type': 'movie', 'title': 'Liger', 'year': '2021'}"
```
EXPECT:
     200 OK and a list of media that matches search criteria

================================================================================

## Swagger Docs

http://localhost:5000/apidocs/

## Postman

https://www.postman.com/

## Development Notes

* If this environment is copied or moved then the environment variables must be
  changed in the python config files.
* Edit the `pyvenv.cfg` file and edit as needed all scripts in the
  `./venv/Scripts` folder.
* Use `./venv/Scripts/deactivate` to deactivate the incorrect environment.
* Use `./venv/Scripts/Activate.ps1` to set the new environment.
* Use `$env:VIRTUAL_ENV -split ';'` in powershell to view the environment variable
  that should point to the correct environment location.
* Use `pip install -r requirements.txt` if the libraries need to be installed
  once the correct virtual environment is set.
* dates are of the format '2026-11-12 00:35:34'


## SQlAlchemy, PostGres, SQLite considerations

Migrating from SQLite to PostgreSQL later requires planning for strict data typing, timezone-aware timestamps, database-specific SQL functions, and schema migrations. While SQLite uses flexible "dynamic typing" (storing almost anything as text or numbers under the hood), PostgreSQL strictly enforces column types, constraints, and transactional rules.

1. Timestamps and Timezones

• Use DateTime(timezone=True) in SQLAlchemy. SQLite has no native DATETIME type and stores dates as text strings, whereas PostgreSQL has dedicated TIMESTAMP and TIMESTAMPTZ (timestamp with time zone) types. Defining Column(DateTime(timezone=True)) ensures PostgreSQL stores timezone-aware UTC values properly.
• Avoid SQLite-specific functions in server_default. Functions like func.strftime(...) work in SQLite but will fail in PostgreSQL. Stick to server_default=func.now(), which SQLAlchemy compiles to CURRENT_TIMESTAMP in both SQLite and PostgreSQL.
• Beware of string-based dates. If you store timestamps as String columns in SQLite, PostgreSQL will reject date math, interval queries, or casting unless you explicitly convert the column type during migration.

2. Data Types and Strict Constraints

• String lengths (String(255)). SQLite ignores length limits on VARCHAR(50) and allows strings of any size. PostgreSQL strictly throws a StringDataRightTruncation error if an inserted string exceeds the declared length.
• Booleans (Boolean). SQLite stores booleans as integers (0 and 1), while PostgreSQL enforces a true BOOLEAN type (true/false). Always use SQLAlchemy's Boolean column type rather than Integer flags so queries like WHERE is_active = 1 do not break on PostgreSQL.
• Auto-incrementing primary keys. SQLite uses INTEGER PRIMARY KEY AUTOINCREMENT, while PostgreSQL uses SERIAL or IDENTITY sequences. If you copy existing rows with explicit IDs from SQLite into PostgreSQL, you must manually reset PostgreSQL's ID sequences afterward (setval()), or future inserts will fail with duplicate key errors.

3. Case Sensitivity and Queries

• Case-sensitive LIKE queries. In SQLite, LIKE is case-insensitive for ASCII characters by default ('apple' LIKE 'Apple' is true). In PostgreSQL, LIKE is strictly case-sensitive; use SQLAlchemy's .ilike() or func.lower() if you want case-insensitive matching on both databases.
• Group By strictness. SQLite allows selecting non-aggregated columns in a GROUP BY query without listing them in the GROUP BY clause. PostgreSQL strictly forbids this and raises a GroupingError.

4. Schema Migrations and Tooling

• Use Alembic from day one. SQLite has limited ALTER TABLE support (for example, older versions struggle to drop or alter columns), whereas PostgreSQL supports full ALTER TABLE operations. Using Flask-Migrate (Alembic) with render_as_batch=True lets your migrations run smoothly on SQLite during development and cleanly on PostgreSQL in production.
• Keep local development close to production. Even if you start with SQLite for speed, consider running a local PostgreSQL instance (such as via Docker) before deploying so you catch strict typing or query issues early.
