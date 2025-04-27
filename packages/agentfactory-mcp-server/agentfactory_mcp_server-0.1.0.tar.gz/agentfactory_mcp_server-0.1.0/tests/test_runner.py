"""Tests for the container runner module."""

import asyncio
import datetime
import json
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agentfactory_mcp_server.database import AgentMeta
from agentfactory_mcp_server.runner import launch_agent


@pytest.fixture
def mock_catalog():
    """Mock for the catalog module."""
    return {
        "models": [
            {"id": "anthropic:claude-3-7-sonnet-latest"},
        ],
        "tools": {
            "execution_env_server": {
                "command": "deno",
                "args": ["run", "-N", "jsr:@pydantic/mcp-run-python", "stdio"]
            },
            "browser_server": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"]
            }
        }
    }


@pytest.fixture
def agent_row():
    """Sample agent row for testing."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=900)
    
    return AgentMeta(
        id="agt_test1234",
        model_id="anthropic:claude-3-7-sonnet-latest",
        tools={"tool_ids": ["execution_env_server", "browser_server"]},
        state="pending",
        created_at=now,
        expires_at=expires_at,
    )


@pytest.mark.asyncio
@patch("agentfactory_mcp_server.runner.load_catalog")
@patch("agentfactory_mcp_server.runner.update_agent_state")
@patch("agentfactory_mcp_server.runner.docker")
@patch("agentfactory_mcp_server.runner.asyncio.create_task")
@patch("agentfactory_mcp_server.runner.asyncio.get_event_loop")
async def test_launch_agent_success(
    mock_get_event_loop, 
    mock_create_task, 
    mock_docker, 
    mock_update_state, 
    mock_load_catalog, 
    mock_catalog, 
    agent_row
):
    """Test successful agent launch."""
    # Mock the catalog load
    mock_load_catalog.return_value.tools = mock_catalog["tools"]
    
    # Mock Docker client and container
    mock_client = MagicMock()
    mock_docker.from_env.return_value = mock_client
    mock_client.ping.return_value = True
    
    # Mock container
    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container
    
    # Set up the container.wait result
    mock_container.wait.return_value = {"StatusCode": 0}
    
    # Mock event loop and run_in_executor
    mock_loop = MagicMock()
    mock_get_event_loop.return_value = mock_loop
    mock_loop.run_in_executor.return_value = {"StatusCode": 0}
    
    # Create a future for the create_task mock
    future = asyncio.Future()
    future.set_result(None)
    mock_create_task.return_value = future
    
    # Run the test
    success, error = await launch_agent(agent_row)
    
    # Verify success
    assert success is True
    assert error is None
    
    # Verify Docker client calls
    mock_docker.from_env.assert_called_once()
    mock_client.ping.assert_called_once()
    
    # Verify container creation with correct parameters
    mock_client.containers.run.assert_called_once()
    args, kwargs = mock_client.containers.run.call_args
    
    # Check image
    assert kwargs["image"] == "agentfactory-agent:latest"
    
    # Check environment variables
    env = kwargs["environment"]
    assert env["MODEL_ID"] == "anthropic:claude-3-7-sonnet-latest"
    assert env["AGENT_ID"] == "agt_test1234"
    assert "TOOL_0_CMD" in env
    assert "TOOL_0_ARGS" in env
    
    # Verify state updates
    mock_update_state.assert_called_once_with(agent_row.id, "running")


@pytest.mark.asyncio
@patch("agentfactory_mcp_server.runner.load_catalog")
@patch("agentfactory_mcp_server.runner.update_agent_state")
@patch("agentfactory_mcp_server.runner.docker")
async def test_launch_agent_with_prompt_and_context(mock_docker, mock_update_state, mock_load_catalog, mock_catalog, agent_row):
    """Test agent launch with prompt and context."""
    # Add prompt and context to the agent
    agent_row.tools = {
        "tool_ids": ["execution_env_server"],
        "prompt": "Hello, agent!",
        "context": {"key": "value"}
    }
    
    # Mock the catalog load
    mock_load_catalog.return_value.tools = mock_catalog["tools"]
    
    # Mock Docker client
    mock_client = MagicMock()
    mock_docker.from_env.return_value = mock_client
    mock_client.ping.return_value = True
    
    # Mock container
    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container
    
    # Patch asyncio.create_task to not run the monitor
    with patch("asyncio.create_task", return_value=None):
        # Run the test
        success, error = await launch_agent(agent_row)
    
    # Verify success
    assert success is True
    
    # Verify container creation with correct environment variables
    args, kwargs = mock_client.containers.run.call_args
    env = kwargs["environment"]
    
    # Check for prompt and context
    assert env["PROMPT"] == "Hello, agent!"
    assert json.loads(env["CONTEXT"]) == {"key": "value"}