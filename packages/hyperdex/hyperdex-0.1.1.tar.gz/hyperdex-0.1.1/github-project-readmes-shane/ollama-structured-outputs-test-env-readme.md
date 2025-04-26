# Ollama Structured Outputs

A demonstration project showing different approaches to getting structured outputs from Ollama using both JavaScript and Python implementations. The project focuses on type safety, proper error handling, and multiple implementation strategies.

[[toc]]

## Prerequisites

- Ollama installed and running
- Node.js 20 (managed via Volta)
- Python 3.12
- UV package manager for Python dependencies

## Installation

1. Clone the repository
2. Pull the required Ollama model:

```bash
ollama pull llama3.2:latest
```

### Python Setup

Install dependencies using UV:

```bash
uv pip install .
```

### JavaScript Setup

Install dependencies using npm:

```bash
npm install
```

## Implementations

### JavaScript Version

Uses Zod for runtime type validation and provides structured JSON outputs. Key features:

- Type safety with Zod
- Structured data output
- Schema validation
- ESM support

Run the JavaScript implementation:

```bash
node ollama_only.js
```

### Python Versions

Three different Python implementations are provided:

1. **Ollama Package (Async)**
   - Uses official Ollama Python package
   - Async/await for stream handling
   - Pydantic for type validation

   ```bash
   python ollama_only.py
   ```

2. **Instructor Implementation**
   - OpenAI-compatible interface
   - Built-in Pydantic integration

   ```bash
   python instructor_ollama.py
   ```

3. **Direct API Calls**
   - Raw HTTP requests to Ollama API
   - Comprehensive error handling

   ```bash
   python ollama_json.py
   ```

## Project Structure

- `ollama_only.js` - JavaScript implementation
- `ollama_only.py` - Python implementation using Ollama package
- `instructor_ollama.py` - Python implementation using Instructor
- `ollama_json.py` - Python implementation using direct API calls
- `pyproject.toml` - Python project configuration
- `package.json` - Node.js project configuration
- `uv.lock` - Python dependency lock file

## Features

- Multiple implementation approaches in both Python and JavaScript
- Type safety and validation
- Proper error handling
- Request timeouts
- Comprehensive documentation
- Linter compliance
- Async support (Python)

## Dependencies

### Python

- ollama: 0.4.4
- instructor: 1.7.0
- pydantic: 2.10.3
- openai: 1.57.0
- requests

### JavaScript

- ollama: ^0.5.11
- zod: ^3.23.8
- zod-to-json-schema: ^3.23.5

## Example Output

```javascript
{
  cities: [
    { name: 'Paris', country: 'France' },
    { name: 'Tokyo', country: 'Japan' },
    { name: 'Rio de Janeiro', country: 'Brazil' },
    { name: 'Beijing', country: 'China' },
    { name: 'Cape Town', country: 'South Africa' }
  ]
}
```

## Version Requirements

- Python: >=3.12
- Node.js: 20.x
