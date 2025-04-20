import os
from fastapi import FastAPI
from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from fastapi_mcp import FastApiMCP

# Load API keys from environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API keys are set
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY environment variable not set.")
if not GOOGLE_API_KEY:
    pass


# Initialize clients and tools
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
tavily_search = TavilySearchResults(max_results=5, include_answer=True)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize FastAPI app
app = FastAPI()

# Define request body model
class SearchRequest(BaseModel):
    query: str

# Define response model
class SearchResponse(BaseModel):
    summary: str

@app.post("/search", response_model=SearchResponse)
async def search_and_summarize(request: SearchRequest):
    """
    Accepts a search query, performs a Tavily search,
    summarizes the results using an LLM, and returns the summary.
    """
    try:
        # Perform Tavily search
        results = tavily_search.invoke(request.query)

        # Combine search result content
        combined_content = "\n\n".join([result['content'] for result in results])

        # Summarize using LLM
        prompt = f"Summarize and enhance these search results for the query '{request.query}':\n {combined_content}"
        final_output = llm.invoke(prompt)

        return SearchResponse(summary=final_output.content)
    except Exception as e:
        # Basic error handling
        return {"error": str(e)}
    
mcp = FastApiMCP(
    app,

    name="My API MCP",
    description="My API description",
    base_url="http://localhost:8008",
)

mcp.mount()
