# LangGraph Anthropic Agency

This repository contains a series of agents powered by Anthropic Claude that demonstrate the capabilities of generative UIs using LangGraph.js. The project includes a local Agent Chat UI for a complete self-hosted development environment.

![Generative UI Example](./static/gen_ui.gif)

## Key Features

- **Anthropic Claude Integration**: Uses Anthropic Claude models instead of OpenAI
- **Local Agent Chat UI**: Integrated [Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui) for local development
- **Generative UI Components**: Rich UI components that enhance the agent experience
- **Multiple Agent Types**: Various specialized agents to demonstrate different capabilities

## Quick Start

> [!TIP]
> For detailed setup instructions, see the [installation-guide.md](./docs/guidelines/installation-guide.md)

### 1. Clone the repository

```sh
git clone https://github.com/langchain-ai/langgraph-anthropic-agency.git
cd langgraph-anthropic-agency
```

### 2. Install dependencies

```sh
# Main project dependencies
pnpm install

# Agent Chat UI dependencies
cd agent-chat-ui
pnpm install
cd ..
```

### 3. Set up environment variables

```sh
cp .env.example .env
```

Edit the `.env` file to add your API keys:

```env
# Required
# OPENAI_API_KEY=""  # Not needed anymore
GOOGLE_API_KEY="your_google_api_key"
ANTHROPIC_API_KEY="your_anthropic_api_key"
```

### The API and Chat servers in one go

```sh
pnpm Start
```

This will start the LangGraph server on port 2024 and the Agent Chat UI on port 5173.

### 6. Access the application

Open your browser and go to [http://localhost:5173](http://localhost:5173). Connect to your local LangGraph server using:

- **Deployment URL**: <http://localhost:2024>
- **Assistant/Graph ID**: agent (or email_agent, chat)
- **LangSmith API Key**: (leave empty for local use)

## Available Agents and Tools

### Supervisor Agent (graph ID: `agent`)

This is the default agent that routes to specialized subgraphs based on user requests:

- **Stockbroker**: Get stock prices, manage portfolio
- **TripPlanner**: Plan trips with accommodation and restaurant suggestions
- **OpenCode**: Generate a React TODO app
- **OrderPizza**: Order pizza with delivery options

### Chat Agent (graph ID: `chat`)

A simple chat agent with no specialized tools.

### Email Agent (graph ID: `email_agent`)

An email assistant that can help draft and send emails with human-in-the-loop capabilities.

## Example Prompts

Try these prompts with the supervisor agent (graph ID: `agent`):

- `What can you do?` - Lists all available tools
- `Show me places to stay in San Francisco` - Triggers the TripPlanner UI
- `Recommend some restaurants for me in New York` - Shows restaurant recommendations
- `What's the current price of AAPL?` - Displays Apple stock price
- `I want to buy 10 shares of MSFT` - Triggers the stock purchase UI
- `Show me my portfolio` - Displays your investment portfolio
- `Write a React TODO app for me` - Demonstrates the OpenCode agent
- `Order me a pizza in Boston` - Demonstrates the OrderPizza agent

## Project Architecture

The project is organized around LangGraph-based agents that use the Agent Chat UI for interaction:

```tree
├── src/
│   ├── agent/              # Agent definitions and logic
│   │   ├── chat-agent/     # Simple chat agent
│   │   ├── email-agent/    # Email assistant
│   │   ├── open-code/      # Code generation agent
│   │   ├── pizza-orderer/  # Pizza ordering agent
│   │   ├── stockbroker/    # Stock market agent
│   │   ├── supervisor/     # Main routing agent
│   │   └── trip-planner/   # Travel planning agent
│   ├── agent-uis/          # UI components for agents
│   └── components/         # Shared UI components
└── agent-chat-ui/          # Local Agent Chat UI
```

## Technical Details

- **Backend**: Node.js with LangGraph.js
- **Models**: Anthropic Claude (various sizes)
- **Frontend**: React with Vite
- **UI Framework**: Tailwind CSS with shadcn/ui components
- **State Persistence**: Conversation history and agent states are persisted to disk in `.langgraph_api/.langgraphjs_ops.json`, ensuring continuity across server restarts

## Customization

You can modify the agent behaviors by:

1. Editing the model configurations in the respective agent files
2. Creating new agent types by duplicating and modifying existing ones
3. Developing custom UI components in the `src/agent-uis` directory

## Related Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraphjs/)
- [Agent Chat UI Repository](https://github.com/langchain-ai/agent-chat-ui)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
