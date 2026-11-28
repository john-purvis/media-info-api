# media_info_api/media/services/media.py

from sqlalchemy.exc import IntegrityError  # noqa: I001

from media_info_api.db import (
    media_to_dict,
    update_media_from_dict)
from media_info_api.extensions import media_db
from media_info_api.media.models.catalog import Catalog
from media_info_api.media.models.media import Media

# media services =============================================================
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
    except IntegrityError as ie:
        media_db.session.rollback()
        if "catalog.media_id" in ie._message():
            return False, f"a catalog already exists for media id: {new_media.id} - contact support"
        else:
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

def s_media_list(current_user_id_str, current_user_is_admin, page = 1, per_page = 10):
    current_user_id = int(current_user_id_str)

    # 1. Start with the base query
    query = Media.query

    # 2. Apply filter only if the user is not an admin
    if not current_user_is_admin:
        query = query.filter(Media.user_id == current_user_id)

    # 3. Order and paginate instead of calling .all()
    pagination = query.order_by(Media.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False  # Prevents 404 if page > total pages; returns empty items instead
    )

    # 4. Serialize only the current page's items
    media = [media_to_dict(m) for m in pagination.items]

    # 5. Return items + forward/backward pagination metadata
    data = {
        "media": media,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_prev": pagination.has_prev,
        "prev_num": pagination.prev_num,
        "has_next": pagination.has_next,
        "next_num": pagination.next_num,
    }

    return True, data

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
