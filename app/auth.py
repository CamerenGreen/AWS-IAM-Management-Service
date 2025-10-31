from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import os

# Header name for API key
API_KEY_HEADER_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)


def require_api_key(api_key: str = Security(api_key_header)):
    """Dependency that enforces an API key when `API_KEY` env var is set.

    Behavior:
    - If `API_KEY` is not set in the environment, this dependency is a no-op (for local/dev/testing).
    - If `API_KEY` is set, the request must include the same key in the X-API-Key header.
    """
    configured = os.getenv("API_KEY")
    if not configured:
        # auth disabled
        return True

    if not api_key or api_key != configured:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

    return True
