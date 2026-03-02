from __future__ import annotations

import secrets

from fastapi import Header

from app.core.config import get_settings
from app.core.errors import AuthorizationError


async def verify_internal_api_key(
    x_internal_api_key: str | None = Header(default=None, alias="X-Internal-API-Key"),
) -> None:
    settings = get_settings()
    if x_internal_api_key is None:
        raise AuthorizationError("Missing internal API key.")
    if not secrets.compare_digest(x_internal_api_key, settings.internal_api_key):
        raise AuthorizationError("Invalid internal API key.")
