# AI Experiments

A repository for experimenting with various AI models and capabilities from Anthropic and OpenAI.

## Overview

This repository contains various experiments and implementations using modern AI models, primarily focusing on Anthropic's Claude and OpenAI's GPT models. It serves as a sandbox for testing different AI capabilities, prompt engineering techniques, and integration approaches.

## Features

- Experiments with Anthropic's Claude models
- Implementations using OpenAI's GPT models
- Environment variable management for API keys
- Various AI use cases and applications
- Documentation of findings and best practices

## Technologies Used

- **Python** - Primary programming language
- **Anthropic API** - For accessing Claude and other Anthropic models
- **OpenAI API** - For accessing GPT and other OpenAI models
- **python-dotenv** - For managing environment variables and API keys

## Getting Started

### Prerequisites

- Python 3.8+
- Anthropic API key
- OpenAI API key

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/shaneholloman/ai-experiments.git
   cd ai-experiments
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:

   ```sh
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running Experiments

Navigate to the `src` directory and run the desired experiment:

```sh
python src/experiment_name.py
```

## Project Structure

```sh
ai-experiments/
├── docs/                # Documentation and findings
├── images/              # Images and diagrams
├── src/                 # Source code for experiments
│   ├── anthropic/       # Claude-specific experiments
│   ├── openai/          # GPT-specific experiments
│   └── utils/           # Shared utilities
├── .env                 # Environment variables (not tracked in git)
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## Experiments

The repository includes various experiments such as:

- Prompt engineering techniques
- Fine-tuning approaches
- Comparison between different models
- Domain-specific applications
- Multimodal capabilities
- Retrieval-augmented generation
- Agent-based implementations

## Contributing

Contributions are welcome! Feel free to add your own experiments or improve existing ones.

1. Fork the repository
2. Create a feature branch
3. Add your experiment
4. Submit a pull request

## License

This project is proprietary and confidential. All rights reserved.

## Acknowledgements

- [Anthropic](https://www.anthropic.com/) for Claude AI models
- [OpenAI](https://openai.com/) for GPT models
