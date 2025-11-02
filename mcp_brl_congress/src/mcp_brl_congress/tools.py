import asyncio

from mcp_brl_congress import server
from mcp_brl_congress.infrastructure import clients
from mcp_brl_congress.service import handlers


@server.mcp.tool()
async def get_bill_text(number: str, year: str) -> str:
    """
    Get the text of a legislative bill from the Brazilian Senate.

    Args:
        number: The number of the bill.
        year: The year of the bill.
    """
    senate_client = clients.HttpxSenateClient()  # TODO: should be injected
    return await handlers.handle_get_bill_text(senate_client, number, year)


@server.mcp.tool()
async def get_senator_profile(
    name: str, start_date: str | None = None, end_date: str | None = None
) -> str:
    """
    Get the basic profile and, optionally, the voting history of a Brazilian senator.

    Args:
        name: The name of the senator to search for.
        startDate: The start date for the voting history search in YYYYMMDD format.
        endDate: The end date for the voting history search in YYYYMMDD format. If omitted, it defaults to the current date.
    """
    senate_client = clients.HttpxSenateClient()  # TODO: should be injected
    return await handlers.handle_get_senator_profile(
        senate_client, name, start_date, end_date
    )


# TODO: just for testing... remove later
async def main() -> None:
    text = await get_bill_text(number="680", year="2024")
    print(text)

    print()

    profile = await get_senator_profile(name="", start_date="", end_date="")
    print(profile)


if __name__ == "__main__":
    asyncio.run(main())
