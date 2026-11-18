import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from phoenix.otel import register
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from tavily import TavilyClient
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

load_dotenv()

class Source(BaseModel):
    """Schema for a source used by the agent"""
    url:str = Field(description="url of the sources used to generate the response")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer:str = Field(description="the agent's answer to the query")
    sources:List[Source] = Field(default_factory=list, description="list of sources used to generate the answer to the query")

tracer_provider = register(
    project_name= os.environ.get("PHOENIX_PROJECT_NAME"),
    auto_instrument=True
)

tavily_client = TavilyClient()
api_wrapper = DuckDuckGoSearchAPIWrapper(backend="bing")
ddg_client = DuckDuckGoSearchRun(api_wrapper=api_wrapper)

@tool
def search_tavily(query: str) -> str:
    """
    Tool that search over internet, it uses tavily api key so it is costly
    Args:
        query: The query to search for

    Returns:
        the search result
    """
    print(f"Searching for {query}")
    return tavily_client.search(query=query)

@tool
def search_duckduckgo(query: str) -> str:
    """
    Tool that search over internet using open source duckduckgo tool. it's cost effective
    Args:
        query: The query to search for

    Returns:
        the search result
    """
    print(f"Searching for {query}")
    return ddg_client.invoke(input=query)



llm = ChatOllama(temperature=0, model=os.environ.get("OLLAMA_MODEL", "llama2"), base_url= os.environ.get("OLLAMA_BASE_URL", ))
tools = [search_tavily, search_duckduckgo]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages": HumanMessage(content="search for 3 job posting for an ai engineer in langchain in bangalore and gurgaon on linkedin and list their details.")})
    print(result)

if __name__ == "__main__":
    main()
