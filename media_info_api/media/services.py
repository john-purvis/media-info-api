# media_info_api/media/services.py

from sqlalchemy.exc import IntegrityError  # noqa: I001
from werkzeug.security import check_password_hash, generate_password_hash

from media_info_api.db import (
    catalog_to_dict,
    media_to_dict,
    join_with_media,
    update_catalog_from_dict,
    update_media_from_dict,
    update_user_from_dict,
    user_to_dict)
from media_info_api.extensions import media_db
from media_info_api.media.models import Catalog, Media, User


def s_health_check():
    media = (
        Media.query
        .first()
    )
    media = media_to_dict(media)
    if not media:
        return False, "not healthy"

    catalog = (
        Catalog.query
        .filter(
            Catalog.id == media["catalog_id"]
        )
        .first()
    )
    catalog = catalog_to_dict(catalog)
    if not catalog:
        return False, "not healthy"

    user = (
        User.query
        .filter(
            User.id == media["user_id"]
        )
        .first()
    )
    user = user_to_dict(user)
    if not user:
        return False, "not healthy"

    joined = join_with_media(media=media, catalog=catalog, user=user)
    return True, joined


# catalog services =============================================================
def s_catalog_get(catalog_id):
    catalog = (
        Catalog.query
        .filter(
            Catalog.id == catalog_id
        )
        .first()
    )
    if not catalog:
        return False, "catalog not found"

    return True, catalog_to_dict(catalog)

def s_catalog_list():
    catalog = (
        Catalog.query
        .order_by(Catalog.id)
        .all()
    )
    return True, [catalog_to_dict(c) for c in catalog]

def s_catalog_create(current_user_id, current_user_is_admin, data):
    new_catalog = Catalog(
        # id             = data.get("id", None), \
        media_id       = data.get("media_id", None), \
        date_created   = data.get("date_created", None), \
        date_archived  = data.get("date_archived", None), \
        location       = data.get("location", None), \
        label          = data.get("label", None), \
        file_media     = data.get("file_media", None), \
        file_media_nfo = data.get("file_media_nfo", None), \
        file_media_img = data.get("file_media_img", None), \
        path_media_rel = data.get("path_media_rel", None), \
        path_media_sub = data.get("path_media_sub", None), \
        path_media_img = data.get("path_media_img", None)
    )
    try:
        # media_id must exist in order to add a catalog
        if current_user_is_admin:
            # no filter if admin
            media = (
                Media.query
                .filter(
                    Media.id == new_catalog.media_id
                )
                .first()
            )
        else:
            # filer by user_id if not admin
            media = (
                Media.query
                .filter(
                    Media.id == new_catalog.media_id
                )
                .filter(
                    Media.user_id == current_user_id
                )
                .first()
            )
        if not media:
            return False, "media not found"

        media_db.session.add(new_catalog)
        media_db.session.commit()
    except IntegrityError:
        media_db.session.rollback()
        return False, "catalog already exists for that media"

    return True, catalog_to_dict(new_catalog)
    #return True, join_with_media(media_to_dict(new_media), catalog_to_dict(new_catalog))


def s_catalog_update(current_user_id, current_user_is_admin, catalog_id, data):
    catalog = (
        Catalog.query
        .filter(
            Catalog.id == catalog_id
        )
        .first()
    )
    if not catalog:
        return "catalog not found"

    # Helper method from db.py to update only valid fields
    # id and /or date_created are already excluded
    # You can include other fields to exclude using extra_excluded
    extra_excluded = []
    update_catalog_from_dict(catalog=catalog, data=data, extra_excluded=extra_excluded)

    try:
        media_db.session.commit()
    except IntegrityError:
        media_db.session.rollback()
        return False, "catalog with that imdb_id already exists"

    return True, catalog_to_dict(catalog)

def s_catalog_delete(current_user_id, current_user_is_admin, catalog_id):
    catalog = (
        Catalog.query
        .filter(
            Catalog.id == catalog_id
        )
        .first()
    )
    if not catalog:
        return False, "catalog not found"

    media_db.session.delete(catalog)
    media_db.session.commit()
    return True, "catalog deleted"

# media services ===============================================================

def s_media_create(data):
    try:
        # 1. Insert the first record with the foreign key left as None (NULL)
        new_media = Media(
            # id          = data.get("id", None), \
            # catalog_id  = data.get("catalog_id", None), \
            catalog_id  = None, \
            user_id     = data.get("user_id", None), \
            type        = data.get("type", None), \
            title       = data.get("title", None), \
            year        = data.get("year", None), \
            duration    = data.get("duration", None), \
            certificate = data.get("certificate", None), \
            genres      = data.get("genres", None), \
            description = data.get("description", None), \
            imdb_id     = data.get("imdb_id", None), \
            tmdb_id     = data.get("tmdb_id", None), \
            wiki_id     = data.get("wiki_id", None)
        )
        media_db.session.add(new_media)

        # 2. Flush sends the INSERT to the DB and populates new_catalog.id
        media_db.session.flush()

        # 3. Use the newly generated ID for the second record
        new_catalog = Catalog(
            # id             = data.get("id", None), \
            # media_id       = data.get("media_id", None), \
            media_id       = new_media.id, \
            # date_created   = data.get("date_created", None), \
            # date_archived  = data.get("date_archived", None), \
            location       = data.get("location", None), \
            label          = data.get("label", None), \
            file_media     = data.get("file_media", None), \
            file_media_nfo = data.get("file_media_nfo", None), \
            file_media_img = data.get("file_media_img", None), \
            path_media_rel = data.get("path_media_rel", None), \
            path_media_sub = data.get("path_media_sub", None), \
            path_media_img = data.get("path_media_img", None)
        )
        media_db.session.add(new_catalog)

        # 4. Flush sends the INSERT to the DB and populates new_media.id
        media_db.session.flush()

        # 5. Assign the second ID back to the first record
        new_media.catalog_id = new_catalog.id

        # 6. Commit executes the final UPDATE and saves everything atomically
        media_db.session.commit()
    except IntegrityError as ie:  # noqa: F841
        media_db.session.rollback()
        return False, "media with that title already exists"
    except Exception as e:  # noqa: BLE001
         return False, f"{e._message()}"

    return True, media_to_dict(new_media)
    # return True, join_with_media(media_to_dict(new_media), catalog_to_dict(new_catalog))

def s_media_get(current_user_id_str, current_user_is_admin, media_id):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all media if admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .first()
        )
    else:
        # filter media by user id if not admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .filter(
                Media.user_id == current_user_id
            )
            .first()
        )
    if not media:
        return False, "media not found"

    return True, media_to_dict(media)

def s_media_list(current_user_id_str, current_user_is_admin):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all media if admin
        media = (
            Media.query
            .order_by(Media.id)
            .all()
        )
    else:
        # filter media by user id if not admin
        media = (
            Media.query
            .filter(Media.user_id == current_user_id)
            .order_by(Media.id)
            .all()
        )
        if not media:
            # no media returned, return empty list
            return True, []

    return True, [media_to_dict(m) for m in media]

def s_media_update(current_user_id_str, current_user_is_admin, media_id, data):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all media if admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .first()
        )
    else:
        # filter media by user id if not admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .filter(
                Media.user_id == current_user_id
            )
            .first()
        )
    if not media:
        return False, "media not found"

    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    # Helper method from db.py to update only valid fields
    # id and /or date_created are already excluded
    # You can include other fields to exclude using extra_excluded
    extra_excluded = []
    update_media_from_dict(media, data=data, extra_excluded=extra_excluded)

    try:
        media_db.session.commit()
    except IntegrityError as ie:
        media_db.session.rollback()
        # Interrogate the error and report error properly
        if "NOT NULL constraint" in ie._message():
            if "user_id" in ie._message():
                return False, "user_id is required"
            if "type" in ie._message():
                return False, "type is required"
            if "title" in ie._message():
                return False, "title is required"
        if "UNIQUE constraint" in ie._message():
            if "title" in ie._message():
                return False, "media with that title already exists"
            if "imdb_id" in ie._message():
                return False, "media with that imdb_id already exists"
            if "tmdb_id" in ie._message():
                return False, "media with that tmdb_id already exists"
            if "wiki_id" in ie._message():
                return False, "media with that wiki_id already exists"
            if "catalog_id" in ie._message():
                return False, "media with that catalog_id already exists"
    except Exception as e:  # noqa: BLE001
         # This could happen if the database is locked
         return False, f"{e._message()}"

    return True, media_to_dict(media)

def s_media_delete(current_user_id_str, current_user_is_admin, media_id):
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all media if admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .first()
        )
    else:
        # filter media by user id if not admin
        media = (
            Media.query
            .filter(
                Media.id == media_id
            )
            .filter(
                Media.user_id == current_user_id
            )
            .first()
        )
    if not media:
        return False, "media not found"

    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    media_db.session.delete(media)
    try:
        media_db.session.commit()
    except Exception as e:  # noqa: BLE001
         # This could happen if the database is locked
         return False, f"{e._message()}"

    return True, "media deleted"

# user services ================================================================

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