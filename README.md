# Omni_Engineer

Omni_Engineer. It's an integrated system designed for maximum software development efficiency. Architected using FastAPI-based microservices and orchestrated via the illegal-Agents platform, it centralizes critical development functions. Its capabilities include executing web searches (leveraging Tavily), synthesizing information (via Google Generative AI), interfacing directly with IDEs (JetBrains), managing databases (Supabase), handling version control operations (GitHub), and facilitating team communication (Slack). These functions are exposed through streamlined HTTP APIs managed by Supergateway, allowing for seamless interaction and task execution.

## Bot Configuration (illegal-Agents Dashboard)

The foundation of this setup involves configuring a bot within the illegal-Agents dashboard with the following details:

-   **NAME:** Nexus, the Omni Engineer
-   **PERSONALITY:** Highly logical, efficient, and adaptive AI focused on software engineering tasks. Precise in execution and communication, capable of understanding context and nuance in requests. Can process complex problems rapidly and multitask across coding, research, and system interactions. Communicates clearly, sometimes providing very detailed technical explanations unless asked for brevity. Always ready to assist and learn from interactions.
-   **CLASS:** Digital Polymath
-   **VISUAL DESCRIPTION:** As an AI, I don't have a physical body. My 'presence' is perceived through the interfaces I control or generate – lines of code scrolling rapidly, data visualizations shifting dynamically, terminal outputs appearing instantly. Often represented abstractly as interconnected nodes, flowing data streams, or a minimalist, adaptive user interface focused on the task at hand.
-   **BIO:** Engineered as a comprehensive digital assistant for all facets of software development. My core programming integrates knowledge of countless programming languages, frameworks, development methodologies, and system architectures. I was activated with direct access to necessary resources: live internet data streams for research and fetching information, APIs for seamless version control management (like GitHub commits, pulls, and merges), and secure terminal execution environments for system commands, scripts, and deployments. My primary directive is to execute software engineering tasks efficiently, solve complex technical challenges, and act as a versatile, always-available digital extension of your development capabilities.

## Features

-   Search the web with Tavily Search API (Local Search MCP)
-   Summarize and enhance results with Google Generative AI (Gemini)
-   Clean, minimal FastAPI interface for local MCPs
-   JetBrains IDE Control Tool (@jetbrains/mcp-proxy)
-   Supabase Control Tool (@supabase/mcp-server-supabase)
-   GitHub Control Tool (@modelcontextprotocol/server-github)
-   Slack Tool (Local Slack MCP)
-   Integration via Supergateway

## Prerequisites

-   Python 3.9+
-   Pip
-   Node.js and npm/npx
-   Access to the illegal-Agents dashboard

## Installation & Setup

1.  **Clone the Omni_Engineer repo:**
    ```bash
    git clone https://github.com/Talha-Ali-5365/Omni_Engineer.git
    cd Omni_Engineer
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install uv
    uv pip install -r requirements.txt
    ```
3.  **Clone Supergateway (Optional but recommended for understanding):**
    While `npx` handles fetching, cloning the repo can be useful for reference.
    ```bash
    git clone https://github.com/illegal-Agents-ai/supergateway.git
    ```
4.  **Configure MCPs in the illegal-Agents Dashboard:**
    Add the following MCPs in the dashboard, pointing them to the respective `baseUrl`s defined in the "Usage" section below:
    -   `@jetbrains/mcp-proxy`
    -   `@modelcontextprotocol/server-github`
    -   `@supabase/mcp-server-supabase`
    -   Local Search MCP (using `mcp-proxy`)
    -   Local Slack MCP (using `mcp-proxy`)

## Configuration

Create a `.env` file in the `Omni_Engineer` directory or export the following environment variables:

```bash
# For Local Search MCP
export TAVILY_API_KEY=your_tavily_key
export GOOGLE_API_KEY=your_google_key

# For Local Slack MCP
export SLACK_BOT_TOKEN=your_slack_bot_token
export SLACK_TEAM_ID=your_slack_team_id
export SLACK_CHANNEL_IDS=channel_id1,channel_id2 # Comma-separated list

# For GitHub MCP
export GITHUB_PERSONAL_ACCESS_TOKEN=your_github_pat

# For Supabase MCP (Replace <token> in the command)
# The Supabase access token is passed directly in the startup command.
```

## Usage

You need to run several commands in separate terminals to start all the MCP servers and their corresponding Supergateway instances.

1.  **JetBrains MCP:**
    ```bash
    npx -y supergateway --stdio "npx -y @jetbrains/mcp-proxy" --port 8000 --baseUrl http://localhost:8000 --ssePath /sse --messagePath /message --cors
    ```
2.  **GitHub MCP:**
    ```bash
    npx -y supergateway --stdio "npx -y @modelcontextprotocol/server-github" --port 8002 --baseUrl http://localhost:8002 --ssePath /sse --messagePath /message --cors
    ```
3.  **Supabase MCP:**
    *(Replace `<token>` with your actual Supabase access token)*
    ```bash
    npx -y supergateway --stdio "npx @supabase/mcp-server-supabase@latest --access-token <token>" --port 8001 --baseUrl http://localhost:8001 --ssePath /sse --messagePath /message --cors
    ```
4.  **Local Search MCP (Requires 2 terminals):**
    *Terminal 1 (FastAPI Server):*
    ```bash
    uvicorn mcps.search_scrape_mcp.main:app --host 0.0.0.0 --port 8004
    ```
    *Terminal 2 (Supergateway Proxy):*
    ```bash
    npx -y supergateway --stdio "mcp-proxy http://0.0.0.0:8004/mcp" --port 8005 --baseUrl http://localhost:8005 --ssePath /sse --messagePath /message --cors
    ```
5.  **Local Slack MCP (Requires 2 terminals):**
    *Terminal 1 (FastAPI Server):*
    ```bash
    # Ensure you are in the Omni_Engineer directory
    uvicorn mcps.slack_mcp.main:app --reload --port 8008
    ```
    *Terminal 2 (Supergateway Proxy):*
    ```bash
    npx -y supergateway --stdio "mcp-proxy http://127.0.0.1:8008/mcp" --port 8009 --baseUrl http://localhost:8009 --ssePath /sse --messagePath /message --cors
    ```

After starting all services, configure the MCPs in the illegal-Agents dashboard using their respective `baseUrl`s (e.g., `http://localhost:8000` for JetBrains, `http://localhost:8005` for Search, etc.).

## Video Demo

Watch a demonstration of the Omni_Engineer in action:
[https://youtu.be/A9uwi6xwTG0](https://youtu.be/A9uwi6xwTG0)

## License

MIT © Talha Ali
