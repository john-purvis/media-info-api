# media_info_api/media/routes/root.py

from flask import Blueprint, jsonify, send_from_directory

from media_info_api.media.services.common import s_health_check

root_bp = Blueprint("root", __name__)

# region: root routes (register with no prefix) =================================

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
    path = root_bp.root_path + "\\..\\"
    return send_from_directory(path, "index.html")


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
            content:
            application/json:
                schema:
                    type: object
                    properties:
                        status:
                            type: boolean
    """
    success, data = s_health_check()
    if not success:
        return jsonify({"error": False}), 200

    return jsonify({"status": True}), 200

#endregion
