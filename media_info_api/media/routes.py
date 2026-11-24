# media_info_api/media/routes.py

from flask import Blueprint, g, jsonify, render_template, request, send_from_directory

from media_info_api.media.services import (
    s_health_check,
    s_media_create,
    s_media_delete,
    s_media_get,
    s_media_list,
    s_media_update,
    s_user_create,
    s_user_delete,
    s_user_get,
    s_user_list,
    s_user_login,
    s_user_update,
)
from media_info_api.middleware import (
    admin_required,
    create_access_token,
    get_revoked_tokens,
    revoke_access_token,
    token_accepted,
    token_required,
)

media_bp = Blueprint("media", __name__)
root_bp = Blueprint("root", __name__)
users_bp = Blueprint("users", __name__)

# media routes (register with "media" prefix) ==================================

@media_bp.route("", methods=["POST"])
@token_required
def media_create():
    """
    create new media in the database
    ---
    tags:
      - Registration
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
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]  # noqa: F841

    data = request.get_json(silent=True) or {}

    # replace any user_id with the current user id
    data["user_id"] = int(current_user_id_str)

    success, data = s_media_create(data)
    if not success:
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        return jsonify({"error": "an error has occurred - contact the administrator"}), 500

    return jsonify(data), 201

@media_bp.get("/<int:media_id>")
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
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_media_get(current_user_id_str, current_user_is_admin, media_id)
    if not success:
        return jsonify({"error": f"{data}"}), 404

    return jsonify(data), 200

@media_bp.get("")
@token_required
def r_media_list():
    """
    list all media
    ---
    tags:
      - Media
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
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
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, media = s_media_list(current_user_id_str, current_user_is_admin)  # noqa: RUF059
    return jsonify(media), 200

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
            password:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      200:
        description: Media updated successfully
        content:
          application/json:
            schema:
            type: object
            properties:
            id:
              type: integer
            email:
              type: string
            phone:
              type: string
            is_admin:
              type: boolean
      400:
        description: Invalid request body
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not the owner or an admin)
      404:
        description: Media not found
      409:
        description: Media with that title already exists
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "a JSON body is required"}), 400

    success, data = s_media_update(current_user_id_str, current_user_is_admin, media_id, data)

    if not success:
        if "nothing to update" in data:
            return jsonify({"error": "nothing to update"}), 400
        if "access denied" in data:
            return jsonify({"error": f"{data}"}), 403
        if "not found" in data:
            return jsonify({"error": f"{data}"}), 404
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        return jsonify({"error": f"{data}"}), 500

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
      403:
        description: Access denied (not the owner or an admin)
      404:
        description: Media not found
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_media_delete(current_user_id_str, current_user_is_admin, media_id)

    if not success:
      if data == "media_not_found":
          return jsonify({"error": "media not found"}), 404
      if data == "access_denied":
          return jsonify({"error": "access denied"}), 403

    return "", 204
#endregion

#region user routes (register with no prefix) ==================================

@root_bp.route("/register", methods=["POST"])
@token_accepted
def r_user_create():
    """
    User registration endpoint that creates a new user in the database.
    ---
    tags:
      - Registration
    security:
      - AuthKey: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Bad request
      409:
        description: Username already taken
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    data = request.get_json(silent=True) or {}

    if ("password_hash" in data):
        # confuse and/or foil attacker
        # do not complain or error
        # just make like the "pasword_hash" was passed as "password"
        # and continue as normal
        data["password"] = data["password_hash"]
        data.pop("password_hash")

    success, data = s_user_create(current_user_id_str, current_user_is_admin, data)

    if not success:
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        return jsonify({"error": "an error has occurred - contact the administrator"}), 500

    if current_user_is_admin is not True:
      if "password_hash" in data:
          data.pop("password_hash")
      if "is_admin" in data:
          data.pop("is_admin")
    return jsonify(data), 201

@root_bp.route("/login", methods=["POST"])
def r_user_login():
    """
    User login endpoint that authenticates a user and returns a JWT token.
    ---
    tags:
      - Login / Logout
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful, returns a JWT token
      400:
        description: Missing credentials
      401:
        description: Invalid username or password
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "missing credentials"}), 400

    success, data = s_user_login(data['username'], data['password'])

    if not success:
      return jsonify({"error": "login failed"}), 401

    # Generate token with (user id) identity and extra attributes
    token = create_access_token(user_id=data["id"], username=data["username"], role=data["role"], is_admin=data["is_admin"])

    return jsonify({"access_token": token}), 200

@root_bp.route("/logout", methods=["POST"])
@token_required
def r_user_logout():
    """
    User logout endpoint in a stateless JWT system.

    This uses a temporary in-memory set to store revoked tokens in
    development.  In production, this would be REDIS.
    ---
    tags:
      - Login / Logout
    security:
      - AuthKey: []
    responses:
      200:
        description: Logout acknowledged; client should discard token
      401:
        description: Unauthorized (no valid token provided)
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]  # noqa: F841
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]  # noqa: F841

    revoke_access_token()
    return jsonify({"message": "user logged out"}), 200

#endregion

#region user routes (register with "users" prefix) =============================

@users_bp.route("/me", methods=["GET"])
@token_required
def me_get():
    """
    Get users own profile
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    responses:
      200:
        description: Successfully returned user
        content:
          application/json:
            schema:
            type: object
            properties:
                username:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                date_created:
                  type: str
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_user_get(current_user_id_str, current_user_is_admin, current_user_id_str)
    if not success:
        if "not found" in data:
            return jsonify(data), 404
        else:
            return jsonify(data), 500

    if "id" in data:
        data.pop("id")
    if "password_hash" in data:
        data.pop("password_hash")
    if "role" in data:
        data.pop("role")
    if "is_admin" in data:
        data.pop("is_admin")
    return jsonify(data), 200

@users_bp.route("/me", methods=["PATCH"])
@token_required
def me_update():
    """
    Update users own details
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            password:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      200:
        description: User updated successfully
        content:
          application/json:
            schema:
            type: object
            properties:
                username:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                date_created:
                  type: str
      400:
        description: Invalid request body
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not the owner or an admin)
      404:
        description: User not found
      409:
        description: A user with that email already exists
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "a JSON body is required"}), 400

    allowed = {"email", "phone"}
    allowed_ordered = {key: data[key] for key in allowed if key in data}

    success, data = s_user_update(current_user_id_str, current_user_is_admin, current_user_id_str, allowed_ordered)

    if not success:
        if "nothing to update" in data:
            return jsonify({"error": f"{data}"}), 400
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "access denied" in data:
            return jsonify({"error": f"{data}"}), 403
        if "not found" in data:
            return jsonify({"error": f"{data}"}), 404
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        return jsonify({"error": "an error has occurred - contact the administrator"}), 500

    if "id" in data:
        data.pop("id")
    if "password_hash" in data:
        data.pop("password_hash")
    if "role" in data:
        data.pop("role")
    if "is_admin" in data:
        data.pop("is_admin")
    return jsonify(data), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
@token_required
@admin_required
def r_user_get(user_id):
    """
    Get user by id
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not an admin)
      404:
        description: User not found
      200:
        description: Successfully returned user
        content:
          application/json:
            schema:
            type: object
            properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                date_created:
                  type: str
                is_admin:
                  type: boolean
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_user_get(current_user_id_str, current_user_is_admin, user_id)
    if not success:
        if "not found" in data:
            return jsonify(data), 404
        else:
            return jsonify(data), 500

    if current_user_is_admin is not True:
      if "password_hash" in data:
          data.pop("password_hash")
      if "is_admin" in data:
          data.pop("is_admin")
    return jsonify(data), 200

@users_bp.route("", methods=["GET"])
@token_required
@admin_required
def r_user_list():
    """
    List all users.
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    responses:
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not an admin)
      200:
        description: Successfully returned a list of users
        content:
          application/json:
            schema:
            type: array
            items:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                date_created:
                  type: str
                is_admin:
                  type: boolean
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    success, data = s_user_list(current_user_id_str, current_user_is_admin)  # noqa: RUF059

    # strip out any sensitive fields if not admin
    # before sending it back
    if current_user_is_admin is not True:
      if "password_hash" in data:
          data = [d.pop("password_hash") for d in data]
      if "is_admin" in data:
          data = [d.pop("is_admin") for d in data]

    return jsonify(data), 200

@users_bp.route("/<int:user_id>", methods=["PATCH"])
@token_required
@admin_required
def r_user_update(user_id):
    """
    Update the details and / or password for a user in the database.
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            password:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      200:
        description: User updated successfully
        content:
          application/json:
            schema:
            type: object
            properties:
            id:
              type: integer
            email:
              type: string
            phone:
              type: string
            is_admin:
              type: boolean
      400:
        description: Invalid request body
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not the owner or an admin)
      404:
        description: User not found
      409:
        description: A user with that email already exists
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "a JSON body is required"}), 400

    if not user_id:
      return jsonify({"error": "nothing to update"}), 400

    success, data = s_user_update(current_user_id_str, current_user_is_admin, user_id, data)

    if not success:
        if "nothing to update" in data:
            return jsonify({"error": f"{data}"}), 400
        if "required" in data:
            return jsonify({"error": f"{data}"}), 400
        if "access denied" in data:
            return jsonify({"error": f"{data}"}), 403
        if "not found" in data:
            return jsonify({"error": f"{data}"}), 404
        if "already exists" in data:
            return jsonify({"error": f"{data}"}), 409
        return jsonify({"error": "an error has occurred - contact the administrator"}), 500

    # strip out any sensitive fields if not admin
    # before sending it back
    if current_user_is_admin is not True:
      if "password_hash" in data:
          data.pop("password_hash")
      if "is_admin" in data:
          data.pop("is_admin")
    return jsonify(data), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
@token_required
@admin_required
def r_user_delete(user_id):
    """
    Delete a user from the database.
    ---
    tags:
      - Users
    security:
      - AuthKey: []  # <--- Tells Swagger to fetch the token from the lock box
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: User deleted successfully
      401:
        description: Unauthorized (not logged in)
      403:
        description: Access denied (not the owner or an admin)
      404:
        description: User not found
    """
    # get custom claims from "g"
    current_user_id_str   = g.current_user["sub"]
    current_username      = g.current_user["username"]  # noqa: F841
    current_user_is_admin = g.current_user["is_admin"]

    if not user_id:
      return jsonify({"error": "nothing to delete"}), 400

    success, data = s_user_delete(current_user_id_str, current_user_is_admin, user_id)

    if not success:
      if "not found" in data:
          return jsonify({"error": f"{data}"}), 404
      if "access denied" in data:
          return jsonify({"error": f"{data}"}), 403

    return "", 204

#endregion

#region: root routes (register with no prefix) =================================

@root_bp.route("/", methods=["GET"])
def index():
    """
    Serve the homepage of the Media Info API.
    ---
    tags:
    - Home
    responses:
        200:
            description: The homepage of the Media Info API
            content:
            text/html:
                schema:
                type: string
                example: "<html><body><h1>Welcome to the Media Info API</h1></body></html>"
    """
    return send_from_directory(root_bp.root_path, "index.html")

# Serves the admin visual UI page
@root_bp.route("/admin/dashboard", methods=["GET"])
def admin_dashboard_page():
    return render_template("admin_dashboard.html")

# Serves the admin visual UI page
@root_bp.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html")

# Protected admin API endpoint called by the dashboard's JavaScript
@root_bp.route("/api/admin/stats", methods=["GET"])
@token_required
@admin_required
def admin_stats_api():
    return (
        jsonify({
            "username": g.current_user["username"],
            "admin_id": g.current_user["sub"],
            "jti": g.current_user["jti"],
            "revoked_tokens_count": len(get_revoked_tokens()),
        }),
        200,
    )

@root_bp.route("/health", methods=["GET"])
def r_health_check():
    """
    Check the status of the Media Info API.
    ---
    tags:
    - Home
    responses:
        200:
            description: The status of the Media Info API
    """
    success, data = s_health_check()
    if not success:
        return jsonify({"error": f"{data}"}), 200

    return jsonify({"status": f"{data}"}), 200

#endregion