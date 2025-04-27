"""Container launcher for agent execution."""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any, Tuple

# Using docker package for docker SDK
import docker
from docker.errors import DockerException, APIError
from docker.models.containers import Container

from agentfactory_mcp_server.catalog import load_catalog
from agentfactory_mcp_server.database import AgentMeta, update_agent_state

# Configure logging
logger = logging.getLogger(__name__)

# Default container image
DEFAULT_IMAGE = os.environ.get("DEFAULT_AGENT_IMAGE", "agentfactory-agent:latest")


def _format_tool_env_vars(agent_row: AgentMeta, catalog_tools: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """
    Format environment variables for tools from agent metadata.
    
    Args:
        agent_row: Agent metadata from database
        catalog_tools: Tools from the catalog
        
    Returns:
        Dictionary of environment variables for the container
    """
    env_vars = {}
    
    # Get the tool IDs from agent metadata
    tool_ids = agent_row.tools.get("tool_ids", [])
    
    # For each requested tool, add environment variables
    for i, tool_id in enumerate(tool_ids):
        if tool_id in catalog_tools:
            tool_config = catalog_tools[tool_id]
            env_vars[f"TOOL_{i}_CMD"] = tool_config["command"]
            env_vars[f"TOOL_{i}_ARGS"] = json.dumps(tool_config.get("args", []))
    
    return env_vars


async def launch_agent(agent_row: AgentMeta) -> Tuple[bool, Optional[str]]:
    """
    Launch an agent container.
    
    Args:
        agent_row: Agent metadata from database
        
    Returns:
        Tuple containing:
          - bool: Success status
          - Optional[str]: Error message if any
    """
    # Get the catalog
    try:
        catalog = load_catalog()
    except Exception as e:
        error_msg = f"Failed to load catalog: {str(e)}"
        logger.error(error_msg)
        update_agent_state(agent_row.id, "failed", exit_code=1)
        return False, error_msg
    
    # Initialize Docker client
    try:
        client = docker.from_env()
        # Simple ping to check connection
        client.ping()
    except DockerException as e:
        error_msg = f"Failed to connect to Docker: {str(e)}"
        logger.error(error_msg)
        update_agent_state(agent_row.id, "failed", exit_code=1)
        return False, error_msg
    
    # Set up environment variables
    env_vars = {
        "MODEL_ID": agent_row.model_id,
        "AGENT_ID": agent_row.id,
    }
    
    # Add tool environment variables
    tool_env_vars = _format_tool_env_vars(agent_row, catalog.tools)
    env_vars.update(tool_env_vars)
    
    # Add optional context if available in tools
    context = agent_row.tools.get("context")
    if context:
        env_vars["CONTEXT"] = json.dumps(context)
    
    # Add optional prompt if available in tools
    prompt = agent_row.tools.get("prompt")
    if prompt:
        env_vars["PROMPT"] = prompt
    
    # Launch container
    container = None
    try:
        logger.info(f"Launching agent container for agent {agent_row.id}")
        
        # Create and start the container
        container = client.containers.run(
            image=DEFAULT_IMAGE,
            detach=True,
            environment=env_vars,
            name=f"agent-{agent_row.id}",
            auto_remove=True,  # Auto-remove container when it exits
        )
        
        # Update agent state to running
        update_agent_state(agent_row.id, "running")
        
        # Start monitoring task to capture exit code
        # Use fire-and-forget pattern, but handle any errors
        monitoring_task = asyncio.create_task(_monitor_container(container, agent_row.id))
        # monitoring_task.add_done_callback(
        #     lambda f: logger.error(f"Container monitoring error: {f.exception()}") if f.exception() else None
        # )
        
        logger.info(f"Successfully launched container for agent {agent_row.id}")
        return True, None
        
    except (DockerException, APIError) as e:
        error_msg = f"Failed to launch container: {str(e)}"
        logger.error(error_msg)
        
        # Update agent state to failed
        update_agent_state(agent_row.id, "failed", exit_code=1)
        
        # Clean up container if it was created
        if container:
            try:
                container.remove(force=True)
            except Exception as cleanup_error:
                logger.error(f"Failed to clean up container: {cleanup_error}")
        
        return False, error_msg


async def _monitor_container(container: Container, agent_id: str) -> None:
    """
    Monitor a container until it exits and update the agent state.
    
    Args:
        container: The Docker container object
        agent_id: The agent ID
    """
    try:
        # Wait for container to finish or time out
        # Use a thread for container.wait() since it's a blocking call
        loop = asyncio.get_event_loop()
        status = await loop.run_in_executor(None, container.wait)
        exit_code = status.get("StatusCode", 1)
        
        # Update agent state based on exit code
        state = "succeeded" if exit_code == 0 else "failed"
        update_agent_state(agent_id, state, exit_code=exit_code)
        
        logger.info(f"Agent {agent_id} finished with exit code {exit_code}")
        
    except DockerException as e:
        # If monitoring fails, mark the agent as failed
        logger.error(f"Error monitoring container for agent {agent_id}: {e}")
        update_agent_state(agent_id, "failed", exit_code=1)