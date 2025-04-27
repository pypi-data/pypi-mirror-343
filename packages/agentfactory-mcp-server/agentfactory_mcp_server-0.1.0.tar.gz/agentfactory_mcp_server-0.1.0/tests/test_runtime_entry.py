"""Unit tests for the runtime_entry.py script."""

import json
import os
import sys
from unittest import mock

import pytest

# Import the runtime_entry script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import runtime_entry


@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables for testing."""
    env_vars = {
        "MODEL_ID": "test-model",
        "TOOL_TEST_CMD": "echo",
        "TOOL_TEST_ARGS": json.dumps(["Hello, World!"]),
        "CONTEXT": json.dumps({"foo": "bar"}),
        "PROMPT": "Test prompt"
    }
    
    with mock.patch.dict(os.environ, env_vars):
        yield env_vars


def test_get_env_var():
    """Test that get_env_var works as expected."""
    # Test with existing environment variable
    with mock.patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        assert runtime_entry.get_env_var("TEST_VAR") == "test_value"
    
    # Test with non-existing required environment variable
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit):
            runtime_entry.get_env_var("TEST_VAR")
    
    # Test with non-existing optional environment variable
    with mock.patch.dict(os.environ, {}, clear=True):
        assert runtime_entry.get_env_var("TEST_VAR", required=False) is None


def test_build_tool_list_from_env(mock_env_vars):
    """Test building tool list from environment variables."""
    tools = runtime_entry.build_tool_list_from_env()
    
    # We expect 1 tool from mock_env_vars fixture
    assert len(tools) == 1
    assert tools[0]["name"] == "TEST"
    assert tools[0]["command"] == "echo"
    assert tools[0]["args"] == ["Hello, World!"]
    
    # Test with 3 tools (the original 1 + 2 new ones)
    with mock.patch.dict(os.environ, {
        "TOOL_TOOL1_CMD": "cmd1",
        "TOOL_TOOL1_ARGS": json.dumps(["arg1"]),
        "TOOL_TOOL2_CMD": "cmd2",
        "TOOL_TOOL2_ARGS": json.dumps(["arg2", "arg3"]),
    }, clear=False):  # Do not clear existing env vars
        tools = runtime_entry.build_tool_list_from_env()
        # Should find 3 tools (TEST from fixture + TOOL1 and TOOL2)
        assert len(tools) == 3
        
        # Sort tools by name for deterministic testing
        tools.sort(key=lambda t: t["name"])
        
        # Find the tools by name
        tool1 = next((t for t in tools if t["name"] == "TOOL1"), None)
        tool2 = next((t for t in tools if t["name"] == "TOOL2"), None)
        
        # Verify TOOL1
        assert tool1 is not None
        assert tool1["command"] == "cmd1"
        assert tool1["args"] == ["arg1"]
        
        # Verify TOOL2
        assert tool2 is not None
        assert tool2["command"] == "cmd2"
        assert tool2["args"] == ["arg2", "arg3"]
    
    # Test with invalid JSON
    with mock.patch.dict(os.environ, {
        "TOOL_INVALID_CMD": "cmd",
        "TOOL_INVALID_ARGS": "not json",
    }):
        with pytest.raises(SystemExit):
            runtime_entry.build_tool_list_from_env()
    
    # Test with no tools
    with mock.patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit):
            runtime_entry.build_tool_list_from_env()


@pytest.mark.asyncio
@mock.patch("runtime_entry.Agent")
async def test_main(mock_agent, mock_env_vars):
    """Test the main function with mocked Agent class."""
    # Create mock agent instance
    mock_agent_instance = mock.AsyncMock()
    mock_agent.return_value = mock_agent_instance
    
    # Configure mock run method to return a result with output
    mock_result = mock.MagicMock()
    mock_result.output = "Test output"
    mock_agent_instance.run.return_value = mock_result
    
    # Configure run_mcp_servers context manager
    mock_context_manager = mock.MagicMock()
    mock_context_manager.__aenter__ = mock.AsyncMock(return_value=None)
    mock_context_manager.__aexit__ = mock.AsyncMock(return_value=None)
    mock_agent_instance.run_mcp_servers.return_value = mock_context_manager
    
    # Run the main function
    exit_code = await runtime_entry.main()
    
    # Verify the agent was created with correct parameters
    mock_agent.assert_called_once()
    assert mock_agent.call_args[0][0] == "test-model"
    
    # Verify run_mcp_servers was called
    mock_agent_instance.run_mcp_servers.assert_called_once()
    
    # Verify run was called with correct context
    mock_agent_instance.run.assert_called_once()
    context = mock_agent_instance.run.call_args[0][0]
    assert context["foo"] == "bar"
    assert context["prompt"] == "Test prompt"
    
    # Verify exit code
    assert exit_code == 0