

import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

# Lightweight in-memory blocklist for quick logout (use Redis in production)
REVOKED_TOKENS = set()

def create_access_token(user_id, username, role, is_admin):
    now = datetime.now(timezone.utc)  # noqa: UP017
    payload = {
        "sub": str(user_id),  # Standard claim: Subject (User ID)
        "jti": str(uuid.uuid4()),  # Standard claim: Unique Token ID (for logout)
        "iat": now,  # Standard claim: Issued At
        "exp": now + timedelta(minutes=int(current_app.config["JWT_EXPIRATION"])),  # Standard claim: Expiration
        # Custom claims
        "username": username,
        "role": role,
        "is_admin": is_admin,
    }
    return jwt.encode(payload=payload, key=current_app.config["JWT_SECRET_KEY"], \
                      algorithm=current_app.config["JWT_ALGORITHM"])

def get_revoked_tokens() -> set:
    return REVOKED_TOKENS

def revoke_access_token():
    jti = g.current_user.get("jti")
    REVOKED_TOKENS.add(jti)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Safety check in case @token_required was forgotten above this decorator
        current_user = getattr(g, "current_user", None)
        if not current_user:
            return jsonify({"error": "authentication required"}), 401

        # Verify the custom claim is explicitly True
        if not current_user.get("is_admin"):
            return jsonify({"error": "elevated privileges required"}), 403

        return f(*args, **kwargs)

    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        # Ensure header is formatted as "Bearer <token>"
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing or malformed authorization header"}), 401

        token = auth_header.split(" ", 1)[1]

        try:
            # PyJWT automatically validates 'exp' and signature
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=[current_app.config["JWT_ALGORITHM"]],
            )

            # Check if the token was logged out
            if payload.get("jti") in REVOKED_TOKENS:
                return jsonify({"error": "token has been revoked"}), 401

            # Store decoded claims in Flask's request context
            g.current_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

def token_accepted(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = {"sub": -1, "username": None, "is_admin": False }
        g.current_user = payload

        auth_header = request.headers.get("Authorization", "")

        # Ensure header is formatted as "Bearer <token>"
        if auth_header.startswith("Bearer "):

            token = auth_header.split(" ", 1)[1]
            try:
                # PyJWT automatically validates 'exp' and signature
                payload = jwt.decode(
                    token,
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms=[current_app.config["JWT_ALGORITHM"]],
                )

                # Check if the token was logged out
                if payload.get("jti") in REVOKED_TOKENS:
                    return f(*args, **kwargs)

                # Store decoded claims in Flask's request context
                g.current_user = payload

            except jwt.ExpiredSignatureError:
                return f(*args, **kwargs)
            except jwt.InvalidTokenError:
                return f(*args, **kwargs)

        return f(*args, **kwargs)

    return decorated


def validate_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False, "missing or malformed authorization header"

    token = auth_header.split(" ", 1)[1]

    try:
        # PyJWT automatically validates 'exp' and signature
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )

        # Check if the token was logged out
        if payload.get("jti") in REVOKED_TOKENS:
            return False, "token has been revoked"

        # Store decoded claims in Flask's request context
        g.current_user = payload

    except jwt.ExpiredSignatureError:
        return False, "token has expired"
    except jwt.InvalidTokenError:
        return False, "invalid token"

    return True, payload
