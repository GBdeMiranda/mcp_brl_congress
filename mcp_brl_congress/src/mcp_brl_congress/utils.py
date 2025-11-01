# tools/utils.py
import io
from typing import Any
import httpx
import fitz  # PyMuPDF


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


async def fetch_document_content(url: str) -> bytes | None:
    """Make a request to fetch raw PDF content."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            response.raise_for_status()
            return response.content
        except Exception:
            return None


def extract_text_from_pdf(pdf_bytes: bytes) -> str | None:
    """Extracts all text from a PDF given its byte content."""
    try:
        with fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf") as doc:
            full_text = "".join(page.get_text() for page in doc)
        return full_text.strip()
    except Exception:
        return None

