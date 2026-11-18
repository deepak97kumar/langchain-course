# LangChain Course Agent

[![PyPI version](https://badge.fury.io/py/langchain-course.svg)](https://pypi.org/project/langchain-course/)
[![Python version](https://badge.fury.io/python/langchain-course.svg)](https://pepy.sha/package/langchain-course)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A powerful, multi-tool LangChain agent designed for cost-aware, comprehensive web search and problem-solving. This course project demonstrates advanced LLM orchestration, integrating local LLMs, structured search APIs, and OpenTelemetry tracing for observability.

## 🚀 Overview

The LangChain Course Agent is an advanced example of an autonomous reasoning system. It leverages a central language model (LLM) orchestrated by LangChain to perform sophisticated search queries. Critically, it intelligently delegates web search tasks to the best available tool—either a paid, high-accuracy service (Tavily) or a cost-effective, open-source alternative (DuckDuckGo)—while providing end-to-end visibility into its operations via Arize Phoenix OpenTelemetry tracing.

## ⚙️ Tech Stack

This project is built on a modern, modular stack designed for robust, observable AI applications:

*   **LLM:** `langchain-ollama`
    *   Uses locally hosted language models via Ollama for private, cost-effective inference.
*   **Search Tools:**
    *   `langchain-tavily`: Integrates the Tavily API for high-fidelity web search.
    *   `ddgs`: Utilizes the DuckDuckGo API Wrapper (configured with the Yahoo backend) for reliable, open-source search results.
*   **LLM Orchestration:** `langchain`
*   **Observability:** `arize-phoenix-otel`
    *   Provides OpenTelemetry tracing to capture the agent's execution flow, allowing developers to track and debug model decisions and tool usage cost-effectively.
*   **Core Dependencies:** `python-dotenv`, `tavily-python`, `ddgs`, etc.

## ✨ Prerequisites

To run this project, ensure you have the following services and tools running:

1.  **Python Version:** Python 3.12 or higher (`>=3.12`).
2.  **Dependency Manager:** The `uv` package manager must be installed (`pip install uv`).
3.  **LLM Backend:** A running Ollama server instance accessible via `OLLAMA_BASE_URL`.
4.  **OpenTelemetry/Tracing:** A local instance of the Arize Phoenix Collector running and reachable.

## <0xF0><0x9F><0x97><0x82>️ Installation & Setup

### 1. Dependency Installation

Use `uv` to install all required dependencies listed in `pyproject.toml`:

```bash
uv sync

2. Environment Configuration
Create a .env file in the project root to securely manage API keys and connection details. The agent requires configuration for the LLM, search providers, and the tracing backend.

.env Template:

# ==============================
# 🔑 API Keys & Credentials
# ==============================
# API key for the paid Tavily search service
TAVILY_API_KEY="YOUR_TAVILY_API_KEY"

# ==============================
# 🤖 Ollama LLM Configuration
# ==============================
# Base URL for the Ollama server (default is http://localhost:11434)
OLLAMA_BASE_URL="http://localhost:11434"
# The name of the model to use (e.g., llama2, mistral)
OLLAMA_MODEL="llama2"

# ==============================
# 🔬 Arize Phoenix Observability
# ==============================
# The project name for tracing in Arize Phoenix
PHOENIX_PROJECT_NAME="langchain-course"
# Endpoint URL for the Phoenix Collector
PHOENIX_COLLECTOR_ENDPOINT="http://localhost:4242/v1/collector/otlp"
# API Key for authentication with the Phoenix service
PHOENIX_API_KEY="YOUR_PHOENIX_API_KEY"

🚀 Usage
The agent is executed via the main.py script. The script initializes the tracing provider, loads the LLM, and passes the combined set of search tools to the agent executor.

To run the agent:

uv run main.py

Execution Flow:
Upon execution, the agent reads the initial prompt (e.g., "What is the current weather of gurugram?"). It determines the best tool, executes the tool (which prints its activity to stdout and sends tracing data to Phoenix), and then uses the LLM to synthesize the final, conclusive answer for the user.

🏛️ Code Architecture Details
Multi-Tool Agent Coordination
The main.py file encapsulates the agent creation using langchain.agents.create_agent. This agent is given a list of available tools:

search_tavily: A wrapper around TavilyClient. This is the high-accuracy, but potentially costly, option.
search_duckduckgo: A wrapper around DuckDuckGoSearchRun. This provides a cost-effective, robust search alternative.
The agent logic handles cost-aware routing: it intelligently decides which tool to invoke based on the query's context and the configured prompt, simulating a routing decision based on tool availability and associated costs.

OpenTelemetry Tracing
All critical components—the LLM call, the execution of search_tavily, and the execution of search_duckduckgo—are wrapped by phoenix.otel.register(). This ensures that every step of the agent's thought process is instrumented and sent to the Arize Phoenix Collector, providing a complete trace of the entire interaction for monitoring and cost analysis.