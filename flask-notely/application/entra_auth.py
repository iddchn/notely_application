import os

import jwt
from jwt import PyJWKClient

_jwks_client = None


def _get_jwks_client(tenant_id):
    # PyJWKClient caches Entra's signing keys between calls.
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(
            f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        )
    return _jwks_client


def validate_entra_token(token):
    """Validate an Entra ID token; returns its claims or raises on failure."""
    tenant_id = os.getenv("ENTRA_TENANT_ID")
    client_id = os.getenv("ENTRA_CLIENT_ID")
    if not tenant_id or not client_id:
        raise RuntimeError("ENTRA_TENANT_ID / ENTRA_CLIENT_ID are not configured")

    signing_key = _get_jwks_client(tenant_id).get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=client_id,
        issuer=f"https://login.microsoftonline.com/{tenant_id}/v2.0",
    )
