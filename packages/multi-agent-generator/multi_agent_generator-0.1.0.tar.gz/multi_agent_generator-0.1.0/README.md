# Multi-Agent Generator

A powerful tool that transforms plain English instructions into fully configured multi-agent AI teams - no scripting, no complexity. Powered by OpenAI GPT models with an intuitive Streamlit UI.

## Features

- Generate agent code for multiple frameworks:
  - **CrewAI**: Structured workflows for multi-agent collaboration
  - **CrewAI Flow**: Event-driven workflows with state management
  - **LangGraph**: LangChain's framework for stateful, multi-actor applications
  - **ReAct**: Reasoning + Acting framework for adaptive AI agents

- **User-Friendly Interface**: Streamlit-based UI for effortless code generation
- **Intelligent Analysis**: Analyzes natural language requirements to suggest appropriate agents, roles, and tasks
- **Visualizations**: View agent relationships, workflow paths, and execution flow

## Installation

```bash
pip install multi-agent-generator
```

## Prerequisites

- OpenAI API key
- Environment variables setup
  - `OPENAI_API_KEY`: Your OpenAI API key

## Usage

### Command Line

```bash
multi-agent-generator "I need a research assistant that summarizes papers and answers questions" --framework crewai
```

### Streamlit UI

```bash
streamlit run -m multi_agent_generator.streamlit_app.app
```

## Examples

### Research Assistant

```
I need a research assistant that summarizes papers and answers questions
```

### Content Creation Team

```
I need a team to create viral social media content and manage our brand presence
```

### Data Analysis

```
I need a team to analyze customer data and create visualizations
```

## Frameworks

### CrewAI

CrewAI is a framework for orchestrating role-playing autonomous AI agents. It allows you to create a crew of agents that work together to accomplish tasks, with each agent having a specific role, goal, and backstory.

### CrewAI Flow

CrewAI Flow extends CrewAI with event-driven workflows. It enables you to define multi-step processes with clear transitions between steps, maintaining state throughout the execution, and allowing for complex orchestration patterns like sequential, parallel, and conditional execution.

### LangGraph

LangGraph is LangChain's framework for building stateful, multi-actor applications with LLMs. It provides a way to create directed graphs where nodes are LLM calls, tools, or other operations, and edges represent the flow of information between them.

### ReAct

ReAct (Reasoning + Acting) is a framework that combines reasoning and action in LLM agents. It prompts the model to generate both reasoning traces and task-specific actions in an interleaved manner, creating a synergy between the two that leads to improved performance.

## License

MIT