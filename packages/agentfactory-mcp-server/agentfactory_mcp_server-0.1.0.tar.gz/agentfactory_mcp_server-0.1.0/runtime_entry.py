#!/usr/bin/env python3
"""
Runtime entry point for agent containers.

This script is executed within the container and:
1. Sets up MCP servers based on environment variables
2. Creates an agent with the spcified model
3. Runs the agent with the provided context
"""

import json
import os
import sys
from typing import Dict, List, Optional

try:
    from pydantic_ai import Agent
except ImportError:
    print("ERROR: pydantic-ai package not found. Please install it with: pip install pydantic-ai", file=sys.stderr)
    sys.exit(1)


def get_env_var(name: str, required: bool = True) -> Optional[str]:
    """
    Get environment variable with error handling.
    
    Args:
        name: The name of the environment variable
        required: Whether the variable is required
        
    Returns:
        The value of the environment variable or None if not set and not required
        
    Raises:
        SystemExit: If the variable is required but not set
    """
    value = os.environ.get(name)
    if required and not value:
        print(f"ERROR: Required environment variable {name} not set", file=sys.stderr)
        sys.exit(1)
    return value


def build_tool_list_from_env() -> List[Dict]:
    """
    Build a list of MCP server configurations from environment variables.
    
    Environment variables should be in the format:
    - TOOL_<name>_CMD: The command to run
    - TOOL_<name>_ARGS: JSON string of arguments to pass
    
    Returns:
        List of tool configurations for the agent
    """
    tools = []
    
    # Find all TOOL_*_CMD environment variables
    for key in os.environ:
        if not key.startswith("TOOL_") or not key.endswith("_CMD"):
            continue
            
        # Extract the tool name from the environment variable
        tool_name = key[5:-4]  # Remove TOOL_ prefix and _CMD suffix
        cmd = os.environ[key]
        
        # Get the arguments JSON string
        args_key = f"TOOL_{tool_name}_ARGS"
        args_json = os.environ.get(args_key, "[]")
        
        try:
            args = json.loads(args_json)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON for {args_key}: {args_json}", file=sys.stderr)
            sys.exit(1)
            
        tools.append({
            "name": tool_name,
            "command": cmd,
            "args": args
        })
    
    if not tools:
        print("ERROR: No tools configured. Set TOOL_*_CMD environment variables.", file=sys.stderr)
        sys.exit(1)
        
    return tools


async def main():
    """Main entry point for the agent runtime."""
    # Get required environment variables
    model_id = get_env_var("MODEL_ID")
    
    # Get optional environment variables
    context_json = get_env_var("CONTEXT", required=False)
    prompt = get_env_var("PROMPT", required=False)
    
    # Build the list of tools
    tool_configs = build_tool_list_from_env()
    
    # Log configuration
    print(f"Starting agent with model: {model_id}")
    print(f"Using {len(tool_configs)} tools")
    
    # Create the agent
    agent = Agent(model_id, mcp_servers=tool_configs)
    
    # Parse context if provided
    context = {}
    if context_json:
        try:
            context = json.loads(context_json)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON for CONTEXT: {context_json}", file=sys.stderr)
            sys.exit(1)
    
    # Add prompt to context if provided
    if prompt:
        context["prompt"] = prompt
    
    # Run the agent with the mcp server given by envvar
    async with agent.run_mcp_servers():
        result = agent.run(user_prompt=prompt)
        
    # Output the result
    print(result.output)
    
    # Return success
    return 0


if __name__ == "__main__":
    import asyncio
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"ERROR: Unhandled exception: {e}", file=sys.stderr)
        sys.exit(1)