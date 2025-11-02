from mcp_brl_congress.infrastructure import clients


async def handle_get_bill_text(
    senate_client: clients.SenateClient, number: str, year: str
) -> str:
    async with senate_client:
        processes = await senate_client.fetch_processes_by_number_and_year(number, year)

        if not processes:
            return f"Could not find a legislative process for bill {number}/{year}."

        all_bill_text = [
            p.conteudo_documento for p in processes if p.conteudo_documento
        ]

        if not all_bill_text:
            return (
                "Found documents, but could not extract any text. They may "
                "not exist, be empty or image-based."
            )

    return "\n\n--- (New Document) ---\n\n".join(all_bill_text)


async def handle_get_senator_profile(
    senate_client: clients.SenateClient,
    name: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    raise NotImplementedError("TODO: handle_get_senator_profile")


__all__ = [
    "handle_get_bill_text",
    "handle_get_senator_profile",
]
