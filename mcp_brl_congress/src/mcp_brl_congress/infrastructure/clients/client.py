import io
import typing

import fitz  # PyMuPDF
import httpx
from pymupdf.mupdf import types

from mcp_brl_congress.infrastructure.clients import dto
from mcp_brl_congress.infrastructure import exceptions

DEFAULT_BASE_URL = "https://legis.senado.leg.br/dadosabertos"


# implicit interface for a Senate API Client
class SenateClient(typing.Protocol):
    async def fetch_processes_by_number_and_year(
        self, number: str, year: str
    ) -> list[dto.SenateProcessData]: ...

    async def fetch_process_document_content(self, document_url: str) -> str: ...

    async def __aenter__(self) -> typing.Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ) -> None: ...


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

        return [await self._process_data_to_dto(pd) for pd in response_data]

    async def fetch_process_document_content(self, document_url: str) -> str:
        response = await self._request("GET", document_url)
        document_bytes = response.content

        try:
            with fitz.open(stream=io.BytesIO(document_bytes), filetype="pdf") as doc:
                full_text = "".join(page.get_text() for page in doc)
            return full_text.strip()
        except Exception:
            return ""

    async def _process_data_to_dto(
        self, process_data: dict[str, typing.Any]
    ) -> dto.SenateProcessData:
        try:
            document_url = process_data.get("urlDocumento")
            document_content = (
                await self.fetch_process_document_content(document_url)
                if document_url
                else None
            )
            return dto.SenateProcessData(
                id=process_data["id"],
                codigo_materia=process_data["codigoMateria"],
                identificacao=process_data["identificacao"],
                objetivo=process_data.get("objetivo"),
                casa_identificadora=process_data.get("casaIdentificadora"),
                ente_identificador=process_data.get("enteIdentificador"),
                tipo_conteudo=process_data.get("tipoConteudo"),
                ementa=process_data.get("ementa"),
                tipo_documento=process_data.get("tipoDocumento"),
                data_apresentacao=process_data.get("dataApresentacao"),
                autoria=process_data.get("autoria"),
                tramitando=process_data.get("tramitando"),
                data_deliberacao=process_data.get("dataDeliberacao"),
                sigla_tipo_deliberacao=process_data.get("siglaTipoDeliberacao"),
                norma_gerada=process_data.get("normaGerada"),
                ultima_informacao_atualizada=process_data.get(
                    "ultimaInformacaoAtualizada"
                ),
                data_ultima_atualizacao=process_data.get("dataUltimaAtualizacao"),
                url_documento=document_url,
                conteudo_documento=document_content,
            )
        except KeyError as e:
            raise exceptions.ClientError(
                "Senate client failed to parse process data response.",
            ) from e

    async def _request(self, method: str, url: str, *args, **kwargs) -> httpx.Response:
        try:
            response = await self.client.request(method, url, *args, **kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise exceptions.ClientStatusError(
                "Senate client request failed.",
                status=e.response.status_code,
                request_url=url,
            ) from e
        except httpx.TimeoutException as e:
            raise exceptions.ClientRequestTimeoutError(
                "Senate client request failed after a timeout.",
                request_url=url,
            ) from e
        except Exception as e:
            raise exceptions.ClientError(
                "Senate client request failed unexpectedly.",
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
