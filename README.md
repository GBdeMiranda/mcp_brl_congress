# Brazilian Congress MCP Server

An MCP (Model Context Protocol) server that provides access to Brazilian Parliament legislative data, enabling the retrieval, search, and analysis of Senate bills, senator profiles, and legislative documents.

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GBdeMiranda/mcp_brl_congress.git
   cd mcp_brl_congress
   ```

2. **Install the MCP tool**:
   ```bash
   uv tool install -e .
   # or with pip
   pip install -e .
   ```

3. **Configure in your MCP Client**:
   Add to your MCP client configuration (e.g., Claude Desktop, Cursor):
   ```json
   {
     "mcpServers": {
       "mcp_brl_congress": {
         "command": "mcp_brl_congress"
       }
     }
   }
   ```

## Available Tools

The server registers the following MCP tools (all returning structured JSON):

1. **`getParliamentarianProfile(name, house, includeVotes, limit)`**:
   - Retrieves the unified bicameral profile of any Brazilian parliamentarian (Senator or Federal Deputy).
   - Consolidates civil name, parliamentary name, house (`Senado Federal` or `Câmara dos Deputados`), party, state (UF), email, photo, active committee assignments, and authored legislative proposals into a standardized JSON response.
   - `house`: `'auto'` (default), `'senado'`, or `'camara'`.

2. **`searchBills(keyword, year, limit)`**:
   - Searches for legislative proposals in the Brazilian Senate using keywords and year filters.

3. **`getBillText(number, year)`**:
   - Retrieves the metadata, status, primary document URL, and extracted text of a legislative bill (e.g., number `"2630"`, year `"2020"`). Automatically prioritizes the primary bill proposition and caps text size safely to avoid context overflow.

4. **`getParliamentarianExpenses(name, house, year, month, limit)`**:
   - Retrieves itemized and aggregated CEAP (parliamentary quota) expenditures.
   - Calculates total spending, categorical breakdown (airfare, housing, publicity, advisory), and top supplier receipts.

5. **`getParliamentarianActivity(name, house, startDate, endDate, limit)`**:
   - Retrieves institutional activity records including plenary sessions, committee deliberations, public hearings, and floor speeches.

6. **`getParliamentarianVotes(name, house, limit, year)`**:
   - Retrieves nominal roll-call voting records, detailing bill subjects and the legislator's specific vote positions (`Sim`, `Não`, `Abstenção`, `Obstrução`).

7. **`evaluateParliamentarian(name, house, year)`**:
   - Consolidates biographical data, CEAP expenses, committee assignments, authored proposals, institutional attendance, and roll-call votes into an objective qualitative evaluation dossier.

8. **`searchCongressionalThemes(theme, house, limit, year)`**:
   - Synthesizes congressional activity surrounding a public policy topic into a consolidated bicameral overview.
   - Aggregates relevant bills, floor speeches, public hearings, committee deliberations, and recent roll-call votes alongside an executive summary.

## API Details

- **Federal Senate**: `https://legis.senado.leg.br/dadosabertos`
- **Chamber of Deputies**: `https://dadosabertos.camara.leg.br/api/v2`
- **Data Format**: JSON with extracted document content
- **Document Processing**: PDF text extraction using PyMuPDF

## Dependencies

- **mcp[cli]**: Model Context Protocol implementation
- **httpx**: Async HTTP client for API requests
- **PyMuPDF**: PDF text extraction
- **Python 3.10+**: Supported runtime
