# media_info_api/media/routes/admin.py

from flask import Blueprint, g, jsonify, render_template

from media_info_api.middleware import (
    admin_required,
    get_revoked_tokens,
    token_required,
)

admin_bp = Blueprint("admin", __name__)

# region: admin routes (register with "admin" prefix) =================================

# Serves the admin visual UI page
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html")


# Protected admin API endpoint called by the dashboard's JavaScript
@admin_bp.route("/stats", methods=["GET"])
@token_required
@admin_required
def admin_stats_api():
    return (
        jsonify(
            {
                "username": g.current_user["username"],
                "admin_id": g.current_user["sub"],
                "jti": g.current_user["jti"],
                "revoked_tokens_count": len(get_revoked_tokens()),
            }
        ),
        200,
    )


# endregion