# media_info_api/media/services/user.py

from sqlalchemy.exc import IntegrityError  # noqa: I001
from werkzeug.security import check_password_hash, generate_password_hash

from media_info_api.db import (
    update_user_from_dict,
    user_to_dict)
from media_info_api.extensions import media_db
from media_info_api.media.models.user import User

# user services =============================================================
def s_user_login(username: str, password: str):
    user = (
        User.query
        .filter(
            User.username == username
        )
        .first()
    )
    if not user:
        return False, "user not found"

    if user and check_password_hash(user.password_hash, password):
        user = user_to_dict(user)
        return True, user
    else:
        return False, "invalid username or password"

def s_user_logout(current_user_id):
    user = (
        User.query
        .filter(
            User.id == current_user_id
        )
        .first()
    )
    if not user:
        return False, "user not found"

    user = user_to_dict(user)
    # remove password hash from user
    if "password_hash" in user:
        user.pop("password_hash")
    # remove is_admin from user
    if "is_admin" in user:
        user.pop("is_admin")
    return True, user

def s_user_create(current_user_id, current_user_is_admin, data):

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    phone = data.get("phone")
    is_admin = data.get("is_admin")

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        phone=phone,
        password_hash=password_hash,
        is_admin=is_admin,
    )
    media_db.session.add(user)

    try:
        media_db.session.commit()
    except IntegrityError as ie:
        media_db.session.rollback()
        # Investigate the reason for the error and report
        if "NOT NULL constraint" in ie._message():
            if "email" in ie._message():
                return False, "a valid email address is required"
            if "username" in ie._message():
                return False, "a valid username is required"
            if "phone" in ie._message():
                return False, "a valid phone number is required"
        if "UNIQUE constraint" in ie._message():
            if "username" in ie._message():
                return False, "a user with that username already exists"
            if "email" in ie._message():
                return False, "a user with that email already exists"
            if "phone" in ie._message():
                return False, "a user with that phone number already exists"
        return False, "an error has occurred - contact the adminstrator"
    except Exception:  # noqa: BLE001
        return False, "an error has occurred - contact the adminstrator"

    user = user_to_dict(user)
    if current_user_is_admin is not True:
        # remove password hash from user
        if "password_hash" in user:
            user.pop("password_hash")
        # remove is_admin from user
        if "is_admin" in user:
            user.pop("is_admin")
    return True, user

def s_user_get(current_user_id, current_user_is_admin, user_id):
    if current_user_is_admin:
        user = (
            User.query
            .filter(
                User.id == user_id
            )
            .first()
        )
    elif str(current_user_id) == str(user_id):
        user = (
            User.query
            .filter(
                User.id == current_user_id
            )
            .first()
        )
    else:
        return False, "user not found"

    if not user:
        return False, "user not found"

    user = user_to_dict(user)
    return True, user

def s_user_list(current_user_id_str, current_user_is_admin):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        users = (
            User.query
            .order_by(User.username)
            .all()
        )
        users = [user_to_dict(u) for u in users]
    else:
        users = (
            User.query
            .filter(
                User.id == current_user_id
            )
            .order_by(User.username)
            .all()
        )
        users = [user_to_dict(u) for u in users]
    return True, users

def s_user_update(current_user_id_str, current_user_is_admin, user_id, data):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show requested user if admin
        user = (
            User.query
            .filter(
                User.id == user_id
            )
            .first()
        )
    else:
        # filter user by current user id if not admin
        if user_id == current_user_id:
            user = (
                User.query
                .filter(
                    User.id == current_user_id
                )
                .first()
            )
        else:
            user = None

    if not user:
        return False, "user not found"

    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    # IF WE GET HERE THEN WE ARE AUTHENTICATED and AUTHORIZED
    # ...and have a user object

    # Helper method from db.py to update only valid fields
    # id and /or date_created are already excluded
    # You can include other fields to exclude using extra_excluded
    extra_excluded = []
    update_user_from_dict(user=user, data=data, extra_excluded=extra_excluded)

    try:
        media_db.session.commit()
        user = user_to_dict(user)
        return True, user
    except IntegrityError as ie:
        media_db.session.rollback()
        # Investigate the reason for the error and report
        if "email" in ie._message():
            return False, "a user with that email already exists"
        if "phone" in ie._message():
            return False, "a user with that phone number already exists"
        return False, "an error has occurred - contact the adminstrator"
    except Exception:  # noqa: BLE001
        media_db.session.rollback()
        return False, "an error has occurred - contact the adminstrator"

def s_user_delete(current_user_id_str, current_user_is_admin, user_id):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # get requested user if admin
        user = (
            User.query
            .filter(
                User.id == user_id
            )
            .first()
        )
    else:
        # filter user by current user id if not admin
        if user_id == current_user_id:
            user = (
                User.query
                .filter(
                    User.id == current_user_id
                )
                .first()
            )
        else:
            user = None

    if not user:
        return False, "user not found"

    media_db.session.delete(user)
    try:
        media_db.session.commit()
        return True, "user deleted"
    except Exception:  # noqa: BLE001
        media_db.session.rollback()
        return False, "an error has occurred - contact the adminstrator"
