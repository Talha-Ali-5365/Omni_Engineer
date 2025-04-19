# Omni_Engineer

Omni_Engineer is a versatile platform integrating various developer tools through a FastAPI‑based microservice architecture. It provides capabilities for web searching (via Tavily), result summarization (using Google Generative AI), IDE control (JetBrains), database interaction (Supabase), version control management (GitHub), and team communication (Slack), all exposed via simple HTTP APIs.

## Features
- Search the web with Tavily Search API (Search Tool)
- Summarize and enhance results with Google Generative AI (Gemini)
- Clean, minimal FastAPI interface
- Automatic MCP (Microservice Provider) mounting
- JetBrains IDE Control Tool
- Supabase Control Tool
- GitHub Control Tool
- Slack Tool

## Prerequisites
- Python 3.9+
- Pip

## Installation

1. Clone the repo  
   ```bash
   git clone https://github.com/Talha-Ali-5365/Omni_Engineer.git
   cd Omni_Engineer
   ```
2. Install dependencies  
   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```

## Configuration

Create a `.env` or export environment variables:

```bash
export TAVILY_API_KEY=your_tavily_key
export GOOGLE_API_KEY=your_google_key
```

## Usage

Start the server:

```bash
uvicorn mcps.search_scrape_mcp.main:app --host 0.0.0.0 --port 8004
```
```bash
npx -y supergateway --stdio "mcp-proxy http://0.0.0.0:8004/mcp" --port 8005 --baseUrl http://localhost:8005 --ssePath /sse --messagePath /message --cors
```

## License

MIT © Talha Ali
