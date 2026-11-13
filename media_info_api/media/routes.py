# media_info_api/media/routes.py
from flask import Blueprint, jsonify

from media_info_api.media.services import (
    db_health_check,
    get_media_service,
    list_media_service,
)

media_bp = Blueprint("media", __name__)
root_bp = Blueprint("root", __name__)

# media routes (register with /media prefix)

@media_bp.get("")
def list_media():
    media = list_media_service()
    return jsonify(media), 200

@media_bp.get("/<int:media_id>")
def get_movie(media_id):
    movie = get_media_service(media_id)
    if movie is None:
        return jsonify({"error": "media not found"}), 404
    return jsonify(movie), 200

# root routes (register with no prefix)

@root_bp.get("/health")
def health_check():
    merged = db_health_check()
    if merged:
        return jsonify({"status": "up"}), 200
    else:
        return jsonify({"status": "down"}), 200