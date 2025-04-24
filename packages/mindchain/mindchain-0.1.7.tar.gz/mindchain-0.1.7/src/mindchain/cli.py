"""
Command Line Interface for the MindChain framework.

This module provides a simple CLI to interact with the MindChain framework.
"""
import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, Optional, Callable, Coroutine

from .mcp.mcp import MCP
from .core.agent import Agent, AgentConfig
from .core.errors import AgentError, MCPError


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


async def run_agent(config_path: Optional[str] = None, query: Optional[str] = None) -> None:
    """Run an agent with the given configuration and query."""
    # Default configuration
    default_config = {
        "name": "DefaultAgent",
        "description": "A default agent created by the MindChain CLI",
        "model_name": "gpt-3.5-turbo",
        "system_prompt": "You are a helpful AI assistant.",
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    # Load configuration if provided
    if config_path:
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
            # Create the configuration properly with named parameters
            agent_config = AgentConfig(
                name=str(config_data.get("name", "DefaultAgent")),
                description=str(config_data.get("description", "")),
                model_name=str(config_data.get("model_name", "gpt-3.5-turbo")),
                temperature=float(config_data.get("temperature", 0.7)),
                max_tokens=int(config_data.get("max_tokens", 1000)),
                tools=config_data.get("tools", []),
                system_prompt=str(config_data.get("system_prompt", "You are a helpful AI assistant.")),
                metadata=config_data.get("metadata", {})
            )
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            sys.exit(1)
    else:
        # Create with default configuration
        agent_config = AgentConfig(
            name=default_config["name"],
            description=default_config["description"],
            model_name=default_config["model_name"],
            system_prompt=default_config["system_prompt"],
            temperature=default_config["temperature"],
            max_tokens=default_config["max_tokens"]
        )

    # Initialize MCP and agent
    mcp = MCP()
    agent = Agent(agent_config)
    agent_id = mcp.register_agent(agent)
    
    logging.info(f"Agent '{agent_config.name}' initialized with ID: {agent_id}")

    try:
        # Process query if provided, otherwise enter interactive mode
        if query:
            # Create a lambda that returns the coroutine to be executed
            async_task = lambda: agent.run(query)
            response = await mcp.supervise_execution(
                agent_id=agent_id,
                task=async_task
            )
            print(f"\nAgent: {response}")
            
            while True:
                try:
                    continue_input = input("\nContinue to iterate? (y/n): ")
                    if continue_input.lower() not in ('y', 'yes'):
                        break
                    
                    # Ask for additional input for the continuation
                    iteration_input = input("\nProvide additional input (or press Enter to continue with the same context): ")
                    continuation_prompt = iteration_input if iteration_input else "Please continue from where you left off."
                    
                    # Create a new task for the continuation
                    async_task = lambda: agent.run(continuation_prompt)
                    response = await mcp.supervise_execution(
                        agent_id=agent_id,
                        task=async_task
                    )
                    print(f"\nAgent: {response}")
                except KeyboardInterrupt:
                    print("\nOperation interrupted by user")
                    break
                except Exception as e:
                    logging.error(f"Error during iteration: {e}")
                    print(f"\nError: {e}")
                    break
        else:
            print(f"MindChain CLI - Agent: {agent_config.name}")
            print("Type 'exit' to quit")
            
            while True:
                try:
                    user_input = input("\nYou: ")
                    if user_input.lower() in ("exit", "quit", "q"):
                        break
                        
                    # Create a lambda that returns the coroutine to be executed
                    async_task = lambda: agent.run(user_input)
                    response = await mcp.supervise_execution(
                        agent_id=agent_id,
                        task=async_task
                    )
                    print(f"\nAgent: {response}")
                    
                    # Ask if the user wants to continue iterating
                    while True:
                        continue_input = input("\nContinue to iterate? (y/n): ")
                        if continue_input.lower() not in ('y', 'yes'):
                            break
                        
                        # Ask for additional input for the continuation
                        iteration_input = input("\nProvide additional input (or press Enter to continue with the same context): ")
                        continuation_prompt = iteration_input if iteration_input else "Please continue from where you left off."
                        
                        # Create a new task for the continuation
                        async_task = lambda: agent.run(continuation_prompt)
                        response = await mcp.supervise_execution(
                            agent_id=agent_id,
                            task=async_task
                        )
                        print(f"\nAgent: {response}")
                except KeyboardInterrupt:
                    print("\nOperation interrupted by user")
                    break
                except (AgentError, MCPError) as e:
                    logging.error(f"Agent or MCP error: {e}")
                    print(f"\nError: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Always cleanup, even if there's an exception
        try:
            mcp.unregister_agent(agent_id)
            logging.info("Agent unregistered. Exiting.")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="MindChain Agentic AI Framework")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run agent command
    run_parser = subparsers.add_parser("run", help="Run an agent")
    run_parser.add_argument(
        "--config", "-c", 
        help="Path to agent configuration JSON file"
    )
    run_parser.add_argument(
        "--query", "-q", 
        help="Query to send to the agent"
    )
    run_parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if args.command == "run":
        setup_logging(args.verbose)
        asyncio.run(run_agent(args.config, args.query))
    elif args.command == "version":
        from . import version
        print(f"MindChain version {version.__version__}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
