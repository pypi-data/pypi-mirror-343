# YouTube Snippets

A Python tool that extracts logical clips from YouTube videos using Claude 3.7 AI.

> Just to get instructor tool to use anthropic. Nothing special here ...

## Description

YouTube Snippets analyzes video transcripts and automatically identifies logical segments that could stand alone as shorter clips. For each segment, it generates:

- A specific, informative title
- A detailed description summarizing the content
- Precise start and end timestamps

This tool is perfect for content creators, researchers, or anyone who needs to extract key segments from longer YouTube videos without manual scrubbing.

## Requirements

- Python 3.10 or higher
- Anthropic API key (for Claude 3.7 access)

## Setup

This is a simple utility script that uses `uv` to manage dependencies defined in `pyproject.toml`.

## API Key

Set your Anthropic API key as an environment variable:

```sh
export ANTHROPIC_API_KEY=your-api-key
```

## Usage

```sh
# Run the script directly
uv run run.py
```

When prompted, enter a YouTube URL. The tool will:

1. Fetch the video transcript
2. Process it using Claude 3.7 to identify logical segments
3. Display a table of clips with titles, descriptions, and timestamps

## Features

- AI-powered identification of logical video segments
- Clean, formatted output using Rich for terminal display
- Spelling correction of transcript text
- Proportional clip length based on video duration

## License

MIT License - Copyright 2025 Shane Holloman
