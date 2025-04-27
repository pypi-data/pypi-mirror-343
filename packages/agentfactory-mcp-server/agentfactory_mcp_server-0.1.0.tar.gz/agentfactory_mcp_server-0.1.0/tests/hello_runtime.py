#!/usr/bin/env python3
"""
Minimal "hello world" runtime for testing purposes.
This script prints a simple message and environment variables.
"""

import os
import sys
import json


def main():
    """Print environment variables and a hello message."""
    print("Hello from the test runtime!")
    
    # Print agent ID if available
    agent_id = os.environ.get("AGENT_ID")
    if agent_id:
        print(f"Agent ID: {agent_id}")
    
    # Print model ID if available
    model_id = os.environ.get("MODEL_ID")
    if model_id:
        print(f"Model ID: {model_id}")
    
    # Print tool information
    tool_count = 0
    for key in os.environ:
        if key.startswith("TOOL_") and key.endswith("_CMD"):
            tool_count += 1
            
    print(f"Found {tool_count} tools")
    
    # Print prompt if available
    prompt = os.environ.get("PROMPT")
    if prompt:
        print(f"Prompt: {prompt}")
    
    # Print context if available
    context_json = os.environ.get("CONTEXT")
    if context_json:
        try:
            context = json.loads(context_json)
            print(f"Context: {json.dumps(context, indent=2)}")
        except json.JSONDecodeError:
            print("Error: Invalid context JSON")
    
    # Return success
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)