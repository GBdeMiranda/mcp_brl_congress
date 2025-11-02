# tools/utils.py
# TODO: remove this module

from typing import Any
import httpx


async def make_request(url: str) -> dict[str, Any] | None:
    """Makes a generic request to an API for JSON data."""
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=headers, timeout=30.0, follow_redirects=True
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
