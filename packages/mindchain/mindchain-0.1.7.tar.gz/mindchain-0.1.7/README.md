# MindChain: Agentic AI Framework

[![PyPI version](https://img.shields.io/pypi/v/mindchain.svg)](https://pypi.org/project/mindchain/)
[![Build Status](https://github.com/Ali-Beg/mindchain/actions/workflows/ci.yml/badge.svg)](https://github.com/Ali-Beg/mindchain/actions)
[![Documentation Status](https://github.com/Ali-Beg/mindchain/actions/workflows/docs.yml/badge.svg)](https://ali-beg.github.io/mindchain/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MindChain is a comprehensive framework for building, deploying, and managing AI agents with a unique Master Control Program (MCP) supervision layer. The architecture enables both simple single-agent workflows and complex multi-agent systems with advanced coordination capabilities.

## Installation

Install from PyPI:

```bash
pip install mindchain
```

## Core Features

- **Master Control Program (MCP)**: Central supervision system for agent management, monitoring, and orchestration
- **Flexible Agent Architecture**: Build single agents or complex multi-agent systems
- **Memory Management**: Contextual memory for improved agent responses
- **Policy Enforcement**: Control what agents can and cannot do
- **Resource Monitoring**: Track and limit resource usage
- **Agent Orchestration**: Coordinate multi-agent workflows with dependency management

## Quick Start

```python
import asyncio
from mindchain import MCP, Agent, AgentConfig

async def main():
    # Initialize the MCP
    mcp = MCP(config={
        'log_level': 'INFO',
        'policies': {
            'allow_external_tools': True,
        }
    })
    
    # Create agent configuration
    config = AgentConfig(
        name="ResearchAssistant",
        description="Helps with research tasks",
        system_prompt="You are a helpful research assistant that provides concise and accurate information."
    )
    
    # Create and register an agent
    agent = Agent(config)
    agent_id = mcp.register_agent(agent)
    
    # Run the agent with MCP supervision
    response = await mcp.supervise_execution(
        agent_id=agent_id,
        task=lambda: agent.run("What are the key benefits of transformer models?")
    )
    print(response)
    
    # Clean up
    mcp.unregister_agent(agent_id)

# Run in an async environment
if __name__ == "__main__":
    asyncio.run(main())
```

## Multi-Agent Orchestration

MindChain provides a powerful `AgentOrchestrator` for coordinating complex multi-agent workflows:

```python
import asyncio
from mindchain import MCP, Agent, AgentConfig, AgentOrchestrator

async def main():
    mcp = MCP()
    orchestrator = AgentOrchestrator(mcp)
    
    # Create and register multiple agents
    agents = []
    agent_ids = []
    
    for role in ["Researcher", "Analyst", "Writer"]:
        agent = Agent(AgentConfig(
            name=role,
            description=f"{role} agent",
            system_prompt=f"You are a {role.lower()} specialized in your domain."
        ))
        agent_id = mcp.register_agent(agent)
        agents.append(agent)
        agent_ids.append(agent_id)
    
    # Create a sequential workflow
    topic = "Artificial Intelligence in Healthcare"
    workflow_id = orchestrator.create_sequential_workflow(
        name="Research and Article Creation",
        description=f"Research and create an article about: {topic}",
        agent_ids=agent_ids,
        prompts=[
            f"Research the topic: {topic}",
            "Analyze this research: {previous_result}",
            "Write an article based on: {previous_result}"
        ]
    )
    
    # Execute the workflow
    results = await orchestrator.execute_workflow(workflow_id)
    
    # Get the final article from the last step
    workflow = orchestrator.get_workflow(workflow_id)
    final_step_id = workflow['steps'][-1]['id']
    article = results[final_step_id]
    
    print(article)
    
    # Clean up
    for agent_id in agent_ids:
        mcp.unregister_agent(agent_id)

if __name__ == "__main__":
    asyncio.run(main())
```

## Framework Structure

- **MCP**: Centralized supervision layer
- **Agent**: Core agent implementation
- **Memory**: Remembers interactions for context
- **Policies**: Controls agent behaviors and permissions
- **Resources**: Manages and limits resource usage
- **Orchestrator**: Coordinates multi-agent workflows

## Running Examples

Explore the included examples to see the framework in action:

```bash
# Run the simple agent example
python -m examples.basic_agent.simple_agent

# Run the multi-agent collaboration example
python -m examples.multi_agent.team_collaboration
```

## Command Line Interface

MindChain comes with a built-in CLI:

```bash
# Show available commands
python -m mindchain --help

# Run an agent interactively
python -m mindchain run

# Run an agent with a specific query
python -m mindchain run --query "Explain what agentic AI is"

# Use a custom configuration file
python -m mindchain run --config my_agent_config.json
```

## Testing

Run the tests:

```bash
pytest
```

## Documentation

For detailed documentation, visit [https://ali-beg.github.io/mindchain](https://ali-beg.github.io/mindchain)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/Ali-Beg/mindchain/blob/main/CONTRIBUTING.md) for details.

## Roadmap

Check out our [ROADMAP.md](https://github.com/Ali-Beg/mindchain/blob/main/ROADMAP.md) for upcoming features and development plans.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Ali-Beg/mindchain/blob/main/LICENSE) file for details.
