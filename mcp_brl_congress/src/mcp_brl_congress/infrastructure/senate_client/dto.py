import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class SenateProcessData:
    id: int
    codigoMateria: int
    identificacao: str
    objetivo: str | None = None
    casaIdentificadora: str | None = None
    enteIdentificador: str | None = None
    tipoConteudo: str | None = None
    ementa: str | None = None
    tipoDocumento: str | None = None
    dataApresentacao: str | None = None
    autoria: str | None = None
    tramitando: str | None = None
    dataDeliberacao: str | None = None
    siglaTipoDeliberacao: str | None = None
    normaGerada: str | None = None
    ultimaInformacaoAtualizada: str | None = None
    dataUltimaAtualizacao: str | None = None
    urlDocumento: str | None = None


@dataclasses.dataclass(frozen=True, kw_only=True)
class SenateProcessDocumentContent:
    pass


__all__ = ["SenateProcessData", "SenateProcessDocumentContent"]
