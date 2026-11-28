# media_info_api/media/services/catalog.py

from media_info_api.db import (
    catalog_to_dict,
    join_with_media,
    media_to_dict,
    user_to_dict,
)
from media_info_api.media.models.catalog import Catalog
from media_info_api.media.models.media import Media
from media_info_api.media.models.user import User


# catalog services =============================================================
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
