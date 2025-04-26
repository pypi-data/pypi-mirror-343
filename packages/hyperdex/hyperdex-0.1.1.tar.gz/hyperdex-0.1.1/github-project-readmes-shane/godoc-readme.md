# GoDoc

> Technical Documentation Assistant with Dual MCP/CLI Interface

A configurable documentation assistant that allows searching and querying any technical documentation using Claude 3.5 Sonnet. GoDoc offers both an MCP server for AI integration and a CLI interface for direct use, now generalized to support any documentation source through configuration.

## Features

- **Dual Interfaces**: Use as both an MCP server and a CLI tool with the same capabilities
- **Configurable Documentation**: Support for multiple documentation sources through YAML configuration
- **Query Capabilities**: Search documentation using Claude 3.5 Sonnet
- **Vector Embeddings**: Optional embeddings-based semantic search
- **Flexible API Key Management**: Use .env file, environment variables, configuration, or command-line options
- **Multiple Access Methods**: Use via uv run, Make commands, or shell script

## Installation

```sh
# Clone the repository
git clone <repository_url>
cd godoc

# Option 1: Install using uv (recommended)
uv venv
source .venv/bin/activate
uv sync

# Option 2: Or use the setup script
./start_server.sh
```

## Configuration

1. Copy the example environment file:

   ```sh
   cp .env.example .env
   ```

2. Edit `.env` to add your Anthropic API key:

   ```ini
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. Configure documentation sources in the `configs/` directory and register them in `meta-config.yaml`

## Usage - Three Ways to Access Dual Functionality

Both the MCP server and CLI functionality can be accessed through three different methods:

### 1. Using UV Run (Recommended)

```sh
# List available configurations
uv run src/build_docs.py --list-configs

# Build documentation
uv run src/build_docs.py --config langgraph
uv run src/build_docs.py --config langgraph --create-vectors

# MCP SERVER FUNCTIONALITY
uv run src/docs_mcp.py --config langgraph  # Run MCP server

# CLI FUNCTIONALITY
uv run src/cli.py --config langgraph  # Interactive mode
uv run src/cli.py --config langgraph "What is a StateGraph?"  # Direct query
```

### 2. Using Make

```sh
# List available configurations
make list-configs

# Build documentation
make build CONFIG=langgraph
make build-vectors CONFIG=langgraph

# MCP SERVER FUNCTIONALITY
make mcp CONFIG=langgraph  # Run MCP server

# CLI FUNCTIONALITY
make cli CONFIG=langgraph  # Interactive mode
make query QUERY="What is a StateGraph?" CONFIG=langgraph  # Direct query

# Show all Make options
make help
```

### 3. Using Shell Script (Legacy)

```sh
# List configurations
./start_server.sh --list-configs

# MCP SERVER FUNCTIONALITY
./start_server.sh --config langgraph  # Run MCP server

# CLI FUNCTIONALITY
./start_server.sh --cli --config langgraph  # Interactive mode
./start_server.sh --query "What is a StateGraph?" --config langgraph  # Direct query

# Show help
./start_server.sh --help
```

## Command-Line Options

All interfaces support these common options:

```sh
Configuration Options:
  --config NAME              Use the named configuration
  --config-file PATH         Use a specific configuration file
  --list-configs             List available configurations

Query Options:
  --method METHOD            Query method: direct, embeddings, auto (default)
  --context-limit N          Character limit for context
  --api-key KEY              Use specific API key
  --create-vectors           Create vector embeddings (build only)
```

## Adding New Documentation Sources

1. Create a new configuration YAML file in the `configs/` directory:

   ```yaml
   # configs/new-docs.yaml
   project:
     name: New Documentation
     description: Documentation for New Project

   documentation:
     sources:
       - type: url
         location: https://docs.newproject.io/guide/
         max_depth: 3
     parser:
       type: html
       selectors:
         content: main.content
         title: h1.title
         code: pre.code

   storage:
     raw_file: data/new-docs/docs_full.txt
     vector_store: data/new-docs/vector_store.parquet

   models:
     llm:
       provider: anthropic
       model_name: claude-3-5-sonnet-20240620
       temperature: 0
     embeddings:
       model_name: all-MiniLM-L6-v2

   prompts:
     system_message: |
       You are a helpful assistant specializing in New Project.
       Answer the question based on this documentation context.
     query_template: |
       QUESTION: {query}

       DOCUMENTATION CONTEXT:
       {context}

       If the documentation doesn't contain enough information to give a complete answer,
       please be honest about any limitations in your response.
   ```

2. Register the configuration in `meta-config.yaml`:

   ```yaml
   configurations:
     new-docs:
       name: New Documentation
       path: configs/new-docs.yaml
       alias: nd
   ```

3. Build the documentation:

   ```sh
   uv run src/build_docs.py --config new-docs
   ```

4. Use the new configuration:

   ```sh
   uv run src/cli.py --config new-docs "How do I get started?"
   ```

## MCP Server Interface

The MCP server provides a standardized interface for AI systems to access documentation:

### Available Tools

- **docs_query_tool**: Query the documentation
  - Parameters:
    - query (str): The question about the documentation
    - use_embeddings (bool): Whether to use embeddings-based retrieval

### Available Resources

- **docs://{project}/full**: Resource for accessing the complete documentation

### MCP Protocol Integration

The server implements the Model Context Protocol, allowing AI systems to:

- Discover available documentation tools and resources
- Send structured queries through the MCP protocol
- Receive well-formatted responses with documentation information

This enables seamless integration with AI assistants and other systems that support the MCP protocol.

## Requirements

- Python 3.10 or higher
- Anthropic API key
