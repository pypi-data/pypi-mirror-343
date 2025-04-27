"""Tests for the TTL enforcement and container cleanup task."""

import asyncio
import datetime
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from agentfactory_mcp_server.cleanup import CleanupTask
from agentfactory_mcp_server.database import AgentMeta


@pytest.fixture
def mock_docker_client():
    """Create a mock Docker client for testing."""
    client = MagicMock()
    containers = MagicMock()
    client.containers = containers
    return client


@pytest.fixture
def expired_agent():
    """Create an expired agent for testing."""
    now = datetime.datetime.now(datetime.timezone.utc)
    # Set expiry to 10 minutes in the past
    expires_at = now - datetime.timedelta(minutes=10)
    
    return AgentMeta(
        id="agt_expired1",
        model_id="test-model",
        tools={"tool_ids": ["test-tool"]},
        state="running",
        created_at=now - datetime.timedelta(minutes=30),
        expires_at=expires_at,
        started_at=now - datetime.timedelta(minutes=20),
    )


@pytest.fixture
def active_agent():
    """Create an active (non-expired) agent for testing."""
    now = datetime.datetime.now(datetime.timezone.utc)
    # Set expiry to 10 minutes in the future
    expires_at = now + datetime.timedelta(minutes=10)
    
    return AgentMeta(
        id="agt_active1",
        model_id="test-model",
        tools={"tool_ids": ["test-tool"]},
        state="running",
        created_at=now - datetime.timedelta(minutes=10),
        expires_at=expires_at,
        started_at=now - datetime.timedelta(minutes=5),
    )


@pytest.mark.asyncio
@patch('agentfactory_mcp_server.cleanup.update_agent_state')
async def test_cleanup_expired_agent(mock_update_state, mock_docker_client, expired_agent):
    """Test that expired agents are properly cleaned up."""
    # Set up the mock container
    container = MagicMock()
    mock_docker_client.containers.get.return_value = container
    
    # Create the cleanup task with the mock client
    cleanup = CleanupTask(docker_client=mock_docker_client)
    
    # Mock _get_expired_agents to return our expired agent
    cleanup._get_expired_agents = AsyncMock(return_value=[expired_agent])
    
    # Run the cleanup
    count = await cleanup.cleanup_expired_agents()
    
    # Verify that the container was killed
    mock_docker_client.containers.get.assert_called_once_with(f"agent-{expired_agent.id}")
    container.kill.assert_called_once()
    
    # Verify that the agent state was updated
    mock_update_state.assert_called_once_with(expired_agent.id, "expired", exit_code=None)
    
    # Verify that the count is correct
    assert count == 1


@pytest.mark.asyncio
@patch('agentfactory_mcp_server.cleanup.update_agent_state')
async def test_cleanup_container_not_found(mock_update_state, mock_docker_client, expired_agent):
    """Test that cleanup works even if the container is not found."""
    # Set up the mock container to raise NotFound
    from docker.errors import NotFound
    mock_docker_client.containers.get.side_effect = NotFound("Container not found")
    
    # Create the cleanup task with the mock client
    cleanup = CleanupTask(docker_client=mock_docker_client)
    
    # Mock _get_expired_agents to return our expired agent
    cleanup._get_expired_agents = AsyncMock(return_value=[expired_agent])
    
    # Run the cleanup
    count = await cleanup.cleanup_expired_agents()
    
    # Verify that the container get was attempted
    mock_docker_client.containers.get.assert_called_once_with(f"agent-{expired_agent.id}")
    
    # Verify that the agent state was updated despite container not found
    mock_update_state.assert_called_once_with(expired_agent.id, "expired", exit_code=None)
    
    # Verify that the count is correct
    assert count == 1


@pytest.mark.asyncio
@patch('agentfactory_mcp_server.cleanup.select')
async def test_get_expired_agents(mock_select, mock_docker_client):
    """Test the query for finding expired agents."""
    # Create the cleanup task with the mock client
    cleanup = CleanupTask(docker_client=mock_docker_client)
    
    # Mock time to a fixed value for testing
    fixed_time = datetime.datetime(2025, 4, 30, 12, 0, 0, tzinfo=datetime.timezone.utc)
    
    # Run the get_expired_agents method
    with patch('agentfactory_mcp_server.cleanup.get_db_session'):
        await cleanup._get_expired_agents(fixed_time)
    
    # Verify that the query was constructed correctly
    mock_select.assert_called_once()
    # Note: We can't easily verify the exact query construction from outside
    # But we can verify that select was called with AgentMeta
    args, _ = mock_select.call_args
    assert args[0] == AgentMeta


@pytest.mark.asyncio
async def test_cleanup_task_loop():
    """Test the cleanup task loop starts and stops correctly."""
    # Create the cleanup task
    cleanup = CleanupTask(cleanup_interval=0.1)  # Short interval for testing
    
    # Mock the cleanup_expired_agents method
    cleanup.cleanup_expired_agents = AsyncMock(return_value=2)
    
    # Start the task
    await cleanup.start()
    
    # Let it run for a moment
    await asyncio.sleep(0.3)  # Should run at least 2-3 times
    
    # Stop the task
    await cleanup.stop()
    
    # Verify that cleanup_expired_agents was called
    assert cleanup.cleanup_expired_agents.call_count >= 2


@pytest.mark.asyncio
@patch('agentfactory_mcp_server.cleanup.datetime')
@patch('agentfactory_mcp_server.cleanup.get_db_session')
async def test_cleanup_with_mocked_time(mock_get_db_session, mock_datetime, mock_docker_client):
    """Test cleanup with a mocked clock to control time."""
    # Set up the mock time
    fixed_time = datetime.datetime(2025, 4, 30, 12, 0, 0, tzinfo=datetime.timezone.utc)
    mock_datetime.datetime.now.return_value = fixed_time
    
    # Create an agent that expires 5 minutes before the fixed time
    expired_time = fixed_time - datetime.timedelta(minutes=5)
    expired_agent = AgentMeta(
        id="agt_expired_time",
        model_id="test-model",
        tools={"tool_ids": ["test-tool"]},
        state="running",
        created_at=expired_time - datetime.timedelta(minutes=10),
        expires_at=expired_time,
        started_at=expired_time - datetime.timedelta(minutes=5),
    )
    
    # Create the cleanup task
    cleanup = CleanupTask(docker_client=mock_docker_client)
    
    # Mock the query results to return our expired agent
    mock_session = MagicMock()
    mock_get_db_session.return_value.__enter__.return_value = mock_session
    mock_session.exec.return_value.all.return_value = [expired_agent]
    
    # Run the cleanup
    with patch('agentfactory_mcp_server.cleanup.update_agent_state') as mock_update_state:
        # Set up the mock container
        container = MagicMock()
        mock_docker_client.containers.get.return_value = container
        
        count = await cleanup.cleanup_expired_agents()
    
    # Verify that cleanup ran and found our expired agent
    assert count == 1
    mock_update_state.assert_called_once_with(expired_agent.id, "expired", exit_code=None)
    container.kill.assert_called_once()