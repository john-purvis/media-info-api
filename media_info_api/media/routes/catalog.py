# media_info_api/media/routes/catalog.py

from flask import (
    Blueprint,
    g,
    jsonify,
    request,
    url_for,
)

from media_info_api.media.services.catalog import (
    s_catalog_create,  # noqa: F401
    s_catalog_delete,  # noqa: F401
    s_catalog_get,  # noqa: F401
    s_catalog_list,
    s_catalog_update,  # noqa: F401
)
from media_info_api.middleware import (
    token_required,
)

catalog_bp = Blueprint("catalog", __name__)

# catalog routes (register with "catalog" prefix) ==================================

@catalog_bp.route("", methods=["GET"])
@token_required
def r_catalog_list():
    """
    list all catalog(s)
    ---
    tags:
      - Catalog
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: The page number to retrieve
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of items per page
    responses:
      401:
        description: unauthorized (not logged in)
      403:
        description: access denied (not an admin)
      200:
        description: successfully returned a list of media
        content:
          application/json:
            schema:
            type: array
            items:
                type: object
                properties:
                    id:
                        type: integer
                    media_id:
                        type: integer
                    date_created:
                        type: datetime
                    date_archived:
                        type: datetime
                    location:
                        type: string
                    label:
                        type: string
                    file_media:
                        type: string
                    file_media_nfo:
                        type: string
                    file_media_img:
                        type: string
                    path_media_rel:
                        type: string
                    path_media_sub:
                        type: string
                    path_media_img:
                        type: integer
    """
    MAX_PER_PAGE = 400

    # get custom claims from "g"
    current_user_id_str = g.current_user["sub"]
    current_username = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if not isinstance(page, int) or page == None or page < 1:
        return jsonify({"error": f"page must be a number between 1 and {MAX_PER_PAGE}"}), 400
    if not isinstance(page, int) or (per_page < 1 or per_page > MAX_PER_PAGE):
        return jsonify(
            {"error": f"per_page must be a number between 1 and {MAX_PER_PAGE}"}
        ), 400

    success, data = s_catalog_list(
        current_user_id_str, current_user_is_admin, page, per_page
    )

    if success:
        # Attach ready-to-use forward/backward URLs
        data["prev_url"] = (
            url_for(request.endpoint, page=data["prev_num"], per_page=per_page)
            if data["has_prev"]
            else None
        )
        data["next_url"] = (
            url_for(request.endpoint, page=data["next_num"], per_page=per_page)
            if data["has_next"]
            else None
        )

    return jsonify(data), 200


# endregion
