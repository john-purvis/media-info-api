# media_info_api/media/routes/media.py

from flask import (
    Blueprint,
    g,
    jsonify,
    request,
    url_for,
)

from media_info_api.media.services.media import (
    s_media_create,
    s_media_delete,
    s_media_get,
    s_media_list,
    s_media_update,
)
from media_info_api.middleware import (
    token_required,
)

media_bp = Blueprint("media", __name__)

# media routes (register with "media" prefix) ==================================

@media_bp.route("", methods=["POST"])
@token_required
def media_create():
    """
    create new media in the database
    ---
    tags:
      - Media
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
                catalog_id:
                    type: integer
                user_id:
                    type: integer
                type:
                    type: string
                title:
                    type: string
                year:
                    type: string
                duration:
                    type: integer
                certificate:
                    type: string
                genres:
                    type: string
                description:
                    type: string
                imdb_id:
                    type: string
                tmdb_id:
                    type: string
                wiki_id:
                    type: string
    responses:
      201:
        description: media created successfully
      400:
        description: bad request
      409:
        description: title already taken
    """
    # get custom claims from "g"
    current_user_id_str = g.current_user["sub"]
    current_username = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]  # noqa: F841

    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({"error": "a JSON body is required"}), 400
    if "user_id" in data:  # noqa: SIM102
        if data["user_id"] == None or data["user_id"].strip() == "":
            return jsonify({"error": "user_id is required"}), 400
    if "type" in data:  # noqa: SIM102
        if data["type"] == None or data["type"].strip() == "":
            return jsonify({"error": "type is required"}), 400
    if "title" in data:  # noqa: SIM102
        if data["title"] == None or data["title"].strip() == "":
            return jsonify({"error": "title is required"}), 400

    # replace any user_id with the current user id
    data["user_id"] = int(current_user_id_str)

    success, data = s_media_create(data)
    if not success:
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        if "database is locked" in data:
            return jsonify(
                {"error": "the database is locked - contact the administrator"}
            ), 500

        return jsonify(
            {"error": "an error has occurred - contact the administrator"}
        ), 500

    return jsonify(data), 201


@media_bp.route("/<int:media_id>", methods=["GET"])
@token_required
def r_get_media(media_id):
    """
    get media by id
    ---
    tags:
      - Media
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: media_id
        in: path
        type: integer
        required: true
    responses:
      401:
        description: unauthorized (not logged in)
      403:
        description: access denied (not an admin)
      200:
        description: successfully returned media
        content:
          application/json:
            schema:
            type: object
            properties:
                id:
                    type: integer
                type:
                    type: string
                title:
                    type: string
                year:
                    type: string
                duration:
                    type: integer
                certificate:
                    type: string
                genres:
                    type: string
                description:
                    type: string
                imdb_id:
                    type: string
                tmdb_id:
                    type: string
                wiki_id:
                    type: string
                catalog_id:
                    type: integer
                user_id:
                    type: integer
    """
    # get custom claims from "g"
    current_user_id_str = g.current_user["sub"]
    current_username = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_media_get(current_user_id_str, current_user_is_admin, media_id)
    if not success:
        return jsonify({"error": f"{data}"}), 404

    return jsonify(data), 200


@media_bp.route("", methods=["GET"])
@token_required
def r_media_list():
    """
    list all media
    ---
    tags:
      - Media
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
                    type:
                        type: string
                    title:
                        type: string
                    year:
                        type: string
                    duration:
                        type: integer
                    certificate:
                        type: string
                    genres:
                        type: string
                    description:
                        type: string
                    imdb_id:
                        type: string
                    tmdb_id:
                        type: string
                    wiki_id:
                        type: string
                    catalog_id:
                        type: integer
                    user_id:
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

    success, data = s_media_list(
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


@media_bp.route("/<int:media_id>", methods=["PATCH"])
@token_required
def r_media_update(media_id):
    """
    Update the details for media in the database.
    ---
    tags:
      - Media
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: media_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            year:
              type: integer
            duration:
              type: string
            certificate:
              type: string
            genres:
              type: string
            description:
              type: string
            imdb_id:
              type: string
            tmdb_id:
              type: string
            wiki_id:
              type: string
            catalog_id:
              type: integer
    responses:
      200:
        description: Media updated successfully
        content:
          application/json:
            schema:
            type: object
            properties:
            title:
              type: string
            year:
              type: integer
            duration:
              type: string
            certificate:
              type: string
            genres:
              type: string
            description:
              type: string
            imdb_id:
              type: string
            tmdb_id:
              type: string
            wiki_id:
              type: string
            catalog_id:
              type: integer
      400:
        description: Invalid request body
      401:
        description: Unauthorized (not logged in)
      404:
        description: Media not found
      409:
        description: Media with that title already exists
    """
    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    # get custom claims from "g"
    current_user_id_str = g.current_user["sub"]
    current_username = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "a JSON body is required"}), 400
    if "user_id" in data:  # noqa: SIM102
        if data["user_id"] == None or data["user_id"].strip() == "":
            return jsonify({"error": "user_id is required"}), 400
    if "type" in data:  # noqa: SIM102
        if data["type"] == None or data["type"].strip() == "":
            return jsonify({"error": "type is required"}), 400
    if "title" in data:  # noqa: SIM102
        if data["title"] == None or data["title"].strip() == "":
            return jsonify({"error": "title is required"}), 400

    success, data = s_media_update(
        current_user_id_str, current_user_is_admin, media_id, data
    )

    if not success:
        if "nothing to update" in data:
            return jsonify({"error": "nothing to update"}), 400
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "not found" in data:
            return jsonify({"error": f"{data}"}), 404
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        if "database is locked" in data:
            return jsonify(
                {"error": "the database is locked - contact the administrator"}
            ), 500

        return jsonify(
            {"error": "an error has occurred - contact the administrator"}
        ), 500

    return jsonify(data), 200


@media_bp.route("/<int:media_id>", methods=["DELETE"])
@token_required
def r_media_delete(media_id):
    """
    Delete media from the database.
    ---
    tags:
      - Media
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: media_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Media deleted successfully
      401:
        description: Unauthorized (not logged in)
      404:
        description: Media not found
    """
    # Filter by owner handles ownership check to maintain consistency and
    # not leak information.  An attacker receiving 404 for GET, but 403 on
    # UPDATE and DELETE would deduce that the ID existed. No 403 required here.

    # get custom claims from "g"
    current_user_id_str = g.current_user["sub"]
    current_username = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_media_delete(current_user_id_str, current_user_is_admin, media_id)

    if not success:
        if "media not found" in data:
            return jsonify({"error": "media not found"}), 404
        if "database is locked" in data:
            return jsonify(
                {"error": "the database is locked - contact the administrator"}
            ), 500

        return jsonify(
            {"error": "an error has occurred - contact the administrator"}
        ), 500

    return "", 204


# endregion
