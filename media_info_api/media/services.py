# media_info_api/media/services.py

from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from media_info_api.common.db import media_to_dict, user_to_dict
from media_info_api.common.extensions import media_db
from media_info_api.media.models import Media, User


def get_media_service(media_id):
    media = (
        Media.query
        .filter(
            Media.id == media_id
        )
        .first()
    )
    return media_to_dict(media)

def list_media_service():
    media = (
        Media.query
        .order_by(Media.id)
        .all()
    )
    return [media_to_dict(m) for m in media]

def create_media_service(data):
    media = Media(
        imdb_id=data["imdb_id"],
        title=data["title"],
        year=data["year"],
        media_type=data.get("media_type"),
    )
    media_db.session.add(media)

    try:
        media_db.session.commit()
    except IntegrityError:
        media_db.session.rollback()
        return None, "media with that title already exists"

    return media_to_dict(media), None

def update_media_service(media_id, data):
    media = (
        Media.query
        .filter(
            Media.id == media_id
        )
        .first()
    )
    if not media:
        return "media_not_found"

    if "title" in data:
        media.title = data["title"]
    if "year" in data:
        media.year = data["year"]
    if "imdb_id" in data:
        media.imdb_id = data["imdb_id"]
    if "media_type" in data:
        media.media_type = data["media_type"]

    try:
        media_db.session.commit()
    except IntegrityError:
        media_db.session.rollback()
        return None, "a media with that imdb_id already exists"

    return media_to_dict(media), None

def delete_media_service(media_id):
    media = (
        Media.query
        .filter(
            Media.id == media_id
        )
        .first()
    )
    if not media:
        return "media_not_found"

    media_db.session.delete(media)
    media_db.session.commit()
    return None

def authenticate_user(username: str, password: str):
    user = (
        User.query
        .filter(
            User.username == username
        )
        .first()
    )
    if user and check_password_hash(user.password_hash, password):
        return user_to_dict(user)
    return None

def register_user(username, password, email, phone):
    password_hash = generate_password_hash(password)
    user = User(
        username=username,
        email=email,
        phone=phone,
        password_hash=password_hash,
        is_admin=False,
    )
    media_db.session.add(user)

    try:
        media_db.session.commit()
    except IntegrityError:
        return False, "username taken"
    return True, f"registered {username}"

def list_users_for_user(current_user_id, is_admin):
    if is_admin:
        users = (
            User.query
            .order_by(User.username)
            .all()
        )
        return [user_to_dict(u) for u in users]
    else:
        users = (
            User.query
            .filter(
                User.id == current_user_id
            )
            .order_by(User.username)
            .all()
        )
        return [user_to_dict(u) for u in users]

def update_user_for_user(current_user_id, is_admin, user_id, data):
    fields = []
    for column in ("password", "email", "phone", is_admin):
        if column in data:
            fields.append(f"{column}, ")
    if not fields:
        return None, "nothing_to_update"

    # Fetch user
    user = (
        User.query
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:
        return None, "user_not_found"

    if str(user.id) != str(current_user_id) and is_admin is not True:
        return None, "access_denied"

    if "password" in data:
        # check for blank password
        if data["password"].strip() == "":
            return None, "password_is_empty"
        user.password_hash = generate_password_hash(data["password"])
    if "email" in data:
        user.email = data["email"]
    if "phone" in data:
        user.phone = data["phone"]
    if "is_admin" in data and is_admin is True:
        # only update is_admin if current user is admin
        # do not report the error, just silently fail to update
        # so as not to give a potential attacker more information
        user.is_admin = 1 if data["is_admin"] else 0

    try:
        media_db.session.commit()
    except IntegrityError:
        media_db.session.rollback()

        if data.get("email"):
            return user_to_dict(user), "duplicate_email"


    return user_to_dict(user), None

def delete_user_for_user(current_user_id, is_admin, user_id, data):
    user = (
        User.query
        .filter(
            User.id == user_id
        )
        .first()
    )
    if not user:
        return "user_not_found"

    if not is_admin:
        return "access_denied"

    media_db.session.delete(user)
    media_db.session.commit()
    return None