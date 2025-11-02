import dataclasses


@dataclasses.dataclass(frozen=True, kw_only=True)
class SenateProcessData:
    id: int  # id
    codigo_materia: int  # codigoMateria
    identificacao: str  # identificacao
    objetivo: str | None = None  # objetivo
    casa_identificadora: str | None = None  # casaIdentificadora
    ente_identificador: str | None = None  # enteIdentificador
    tipo_conteudo: str | None = None  # tipoConteudo
    ementa: str | None = None  # ementa
    tipo_documento: str | None = None  # tipoDocumento
    data_apresentacao: str | None = None  # dataApresentacao
    autoria: str | None = None  # autoria
    tramitando: str | None = None  # tramitando
    data_deliberacao: str | None = None  # dataDeliberacao
    sigla_tipo_deliberacao: str | None = None  # siglaTipoDeliberacao
    norma_gerada: str | None = None  # normaGerada
    ultima_informacao_atualizada: str | None = None  # ultimaInformacaoAtualizada
    data_ultima_atualizacao: str | None = None  # dataUltimaAtualizacao
    url_documento: str | None = None  # urlDocumento
    conteudo_documento: str | None = None


__all__ = ["SenateProcessData"]
