# media_info_api/media/services/catalog.py

from sqlalchemy.exc import IntegrityError

from media_info_api.db import catalog_to_dict, update_catalog_from_dict
from media_info_api.extensions import media_db
from media_info_api.media.models.catalog import Catalog
from media_info_api.media.models.media import Media


# catalog services =============================================================
def s_catalog_get(current_user_id_str, current_user_is_admin, catalog_id):
    # TODO: get associated media
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all catalogs if admin
        catalog = (
            Catalog.query
            .first()
        )
    else:
        # filter catalogs by user id if not admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.user_id == current_user_id
            )
            .first()
        )
    if not catalog:
        return False, "catalog not found"

    return True, catalog_to_dict(catalog)
    #return True, join_with_media(media_to_dict(new_media), catalog_to_dict(new_catalog))

def s_catalog_list(current_user_id_str, current_user_is_admin, page = 1, per_page = 10):
    # TODO: list associated media
    # TODO: add pagination for catalogs
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all catalogs if admin
        catalog = (
            Catalog.query
            .order_by(Catalog.id)
            .all()
        )
    else:
        # filter catalogs by user id if not admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.user_id == current_user_id
            )
            .order_by(Catalog.id)
            .all()
        )
    if not catalog:
        return False, "catalog(s) not found"

    return True, [catalog_to_dict(c) for c in catalog]
    #return True, join_with_media(media_to_dict(new_media), catalog_to_dict(new_catalog))

def s_catalog_create(current_user_id_str, current_user_is_admin, data):
    # TODO: create associated media
    current_user_id = int(current_user_id_str)

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

def s_catalog_update(current_user_id_str, current_user_is_admin, catalog_id, data):
    # TODO: update associated media
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all catalogs if admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.id == catalog_id
            )
            .first()
        )
    else:
        # filter catalogs by user id if not admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.id == catalog_id
            )
            .filter(
                Catalog.user_id == current_user_id
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
    #return True, join_with_media(media_to_dict(new_media), catalog_to_dict(new_catalog))

def s_catalog_delete(current_user_id_str, current_user_is_admin, catalog_id):
    # TODO: delete associated media
    current_user_id = int(current_user_id_str)

    if current_user_is_admin:
        # show all catalogs if admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.id == catalog_id
            )
            .first()
        )
    else:
        # filter catalogs by user id if not admin
        catalog = (
            Catalog.query
            .filter(
                Catalog.id == catalog_id
            )
            .filter(
                Catalog.user_id == current_user_id
            )
            .first()
        )
    if not catalog:
        return False, "catalog not found"

    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    media_db.session.delete(catalog)
    media_db.session.commit()
    return True, "catalog deleted"
