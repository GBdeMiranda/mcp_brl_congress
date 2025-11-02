import sys

from mcp.server.fastmcp import FastMCP

from mcp_brl_congress.utils import make_request


mcp = FastMCP("senate")

API_BASE_URL = "https://legis.senado.leg.br/dadosabertos"


# TODO: refactor this into new architecture
@mcp.tool()
async def getSenatorProfile(
    name: str, startDate: str | None = None, endDate: str | None = None
) -> str:
    """
    Get the basic profile and, optionally, the voting history of a Brazilian senator.

    Args:
        name: The name of the senator to search for.
        startDate: The start date for the voting history search in YYYYMMDD format.
        endDate: The end date for the voting history search in YYYYMMDD format. If omitted, it defaults to the current date.
    """
    search_name = name.lower()
    list_url = f"{API_BASE_URL}/senador/lista/atual"

    data = await make_request(list_url)

    if not data or "ListaParlamentarEmExercicio" not in data:
        return "Could not fetch the list of senators from the API."

    senators = (
        data.get("ListaParlamentarEmExercicio", {})
        .get("Parlamentares", {})
        .get("Parlamentar", [])
    )

    found_senator_info = None
    for senator in senators:
        info = senator.get("IdentificacaoParlamentar", {})
        full_name = info.get("NomeCompletoParlamentar", "").lower()
        parliamentary_name = info.get("NomeParlamentar", "").lower()

        if search_name in full_name or search_name in parliamentary_name:
            found_senator_info = info
            break

    if not found_senator_info:
        return f"No senator found matching the name '{name}'."

    profile_parts = [
        f"Name: {found_senator_info.get('NomeCompletoParlamentar', 'N/A')}",
        f"Parliamentary Name: {found_senator_info.get('NomeParlamentar', 'N/A')}",
        f"Party: {found_senator_info.get('SiglaPartidoParlamentar', 'N/A')} - {found_senator_info.get('UfParlamentar', 'N/A')}",
        f"Email: {found_senator_info.get('EmailParlamentar', 'N/A')}",
        f"Senator Code: {found_senator_info.get('CodigoParlamentar', 'N/A')}",
    ]

    senator_code = found_senator_info.get("CodigoParlamentar")
    if senator_code and startDate:
        query_params = f"dataInicio={startDate}"
        if endDate:
            query_params += f"&dataFim={endDate}"

        votes_url = f"{API_BASE_URL}/senador/{senator_code}/votacoes?{query_params}"
        votes_data = await make_request(votes_url)

        if votes_data and "VotacaoParlamentar" in votes_data:
            votacoes = (
                votes_data.get("VotacaoParlamentar", {})
                .get("Parlamentar", {})
                .get("Votacoes", {})
                .get("Votacao", [])
            )

            if votacoes:
                profile_parts.append("\n--- Voting History ---")
                if not isinstance(votacoes, list):
                    votacoes = [votacoes]

                for voto in votacoes:
                    materia = voto.get("Materia", {})
                    materia_desc = f"{materia.get('Sigla', '')} {materia.get('Numero', '')}/{materia.get('Ano', '')}"
                    descricao_votacao = voto.get("DescricaoVotacao", "N/A")
                    voto_desc = voto.get("DescricaoVoto", "N/A").replace(
                        " (Voto Secreto)", ""
                    )
                    profile_parts.append(
                        f"- On {materia_desc}: Voted '{voto_desc}' ({descricao_votacao})"
                    )
            else:
                profile_parts.append(
                    f"\n--- Voting History ---\nNo votes found for the specified period."
                )
        else:
            profile_parts.append(
                f"\n--- Voting History ---\nCould not retrieve voting history."
            )

    return "\n".join(profile_parts)


def main():
    try:
        print("Iniciando servidor MCP...", file=sys.stderr)
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        raise
