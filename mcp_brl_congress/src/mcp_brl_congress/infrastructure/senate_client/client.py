import typing

import fitz  # PyMuPDF
import httpx
from pymupdf.mupdf import types

from mcp_brl_congress.infrastructure.senate_client import dto
from mcp_brl_congress.infrastructure import exceptions

DEFAULT_BASE_URL = "https://legis.senado.leg.br/dadosabertos"


class SenateClient(typing.Protocol):
    async def fetch_processes_by_number_and_year(
        self,
    ) -> list[dto.SenateProcessData]: ...

    async def fetch_process_document_content(
        self, process_data: dto.SenateProcessData
    ) -> dto.SenateProcessDocumentContent: ...


class HttpxSenateClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self._base_url = base_url
        self._process_data_url = f"{base_url}/processo"

        self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError(
                "Client context is not open. Make sure to use the context manager."
            )

        return self._client

    async def fetch_processes_by_number_and_year(
        self, number: str, year: str
    ) -> list[dto.SenateProcessData]:
        response = await self._request(
            "GET", self._process_data_url, params={"numero": number, "ano": year}
        )
        response_data = response.json()

        return [dto.SenateProcessData(**pd) for pd in response_data]

    async def fetch_process_document_content(
        self, process_data: dto.SenateProcessData
    ) -> dto.SenateProcessDocumentContent:
        raise NotImplementedError("TODO")

    async def _request(self, method: str, url: str, *args, **kwargs) -> httpx.Response:
        try:
            response = await self.client.request(method, url, *args, **kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise exceptions.ClientStatusError(
                "Senate client request failed.",
                request_url=url,
                status=e.response.status_code,
            ) from e
        except httpx.TimeoutException as e:
            raise exceptions.ClientRequestTimeoutError(
                "Senate client request failed after a timeout.",
                request_url=url,
            ) from e
        except Exception as e:
            raise exceptions.ClientError(
                "Senate client request failed unexpectedly",
                request_url=url,
            ) from e
        else:
            return response

    async def __aenter__(self) -> typing.Self:
        if self._client is not None:
            raise RuntimeError("Client context is already open.")

        self._client = httpx.AsyncClient(
            headers={"Accept": "application/json"}, timeout=30.0, follow_redirects=True
        )

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ) -> None:
        if self._client is None:
            return

        await self._client.aclose()
        self._client = None


__all__ = ["SenateClient", "HttpxSenateClient"]
