"""Tests for API schema validation."""

import pytest
from pydantic import ValidationError

from agentfactory_mcp_server.catalog import load_catalog
from agentfactory_mcp_server.schemas import AgentCreateRequest


def test_agent_create_request_valid_minimal():
    """Test a valid minimal agent create request."""
    # Get a valid model ID and tool from the catalog
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    # Create the minimal valid request
    request = AgentCreateRequest(
        model_id=model_id,
        tools=[tool],
        agent_name=None,
        prompt=None,
        context=None,
        stream=False
    )

    # Check that default values are set correctly
    assert request.ttl_seconds == 900
    assert request.stream is False
    assert request.agent_name is None
    assert request.prompt is None
    assert request.context is None


def test_agent_create_request_valid_full():
    """Test a valid complete agent create request with all fields."""
    # Get a valid model ID and tool from the catalog
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    # Create a complete request with all fields
    request = AgentCreateRequest(
        model_id=model_id,
        tools=[tool],
        agent_name="test-agent",
        prompt="Do something useful",
        context={"key": "value"},
        ttl_seconds=1800,
        stream=True
    )

    # Verify all fields are set correctly
    assert request.model_id == model_id
    assert request.tools == [tool]
    assert request.agent_name == "test-agent"
    assert request.prompt == "Do something useful"
    assert request.context == {"key": "value"}
    assert request.ttl_seconds == 1800
    assert request.stream is True


def test_agent_create_request_invalid_model_id():
    """Test validation fails with an invalid model ID."""
    catalog = load_catalog()
    tool = list(catalog.tools.keys())[0]

    with pytest.raises(ValueError, match="Model 'nonexistent-model' not found in catalog"):
        AgentCreateRequest(model_id="nonexistent-model", tools=[tool])


def test_agent_create_request_invalid_tool():
    """Test validation fails with an invalid tool."""
    catalog = load_catalog()
    model_id = catalog.models[0].id

    with pytest.raises(ValueError, match="Tool\\(s\\) not found in catalog"):
        AgentCreateRequest(model_id=model_id, tools=["nonexistent-tool"])


def test_agent_create_request_empty_tools():
    """Test validation fails with an empty tools list."""
    catalog = load_catalog()
    model_id = catalog.models[0].id

    with pytest.raises(ValidationError):
        AgentCreateRequest(model_id=model_id, tools=[])


def test_agent_create_request_invalid_ttl_too_small():
    """Test validation fails with TTL less than minimum."""
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    with pytest.raises(ValidationError):
        AgentCreateRequest(model_id=model_id, tools=[tool], ttl_seconds=59)


def test_agent_create_request_invalid_ttl_too_large():
    """Test validation fails with TTL greater than maximum."""
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    with pytest.raises(ValidationError):
        AgentCreateRequest(model_id=model_id, tools=[tool], ttl_seconds=7201)


def test_agent_create_request_invalid_agent_name_empty():
    """Test validation fails with empty agent name."""
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    with pytest.raises(ValueError, match="agent_name must not be empty if provided"):
        AgentCreateRequest(model_id=model_id, tools=[tool], agent_name="")


def test_agent_create_request_invalid_agent_name_too_long():
    """Test validation fails with agent name exceeding max length."""
    catalog = load_catalog()
    model_id = catalog.models[0].id
    tool = list(catalog.tools.keys())[0]

    # Create a name longer than 64 characters
    long_name = "a" * 65

    with pytest.raises(ValidationError):
        AgentCreateRequest(model_id=model_id, tools=[tool], agent_name=long_name)


def test_agent_create_request_multiple_invalid_tools():
    """Test validation fails with multiple invalid tools."""
    catalog = load_catalog()
    model_id = catalog.models[0].id

    with pytest.raises(ValueError, match="Tool\\(s\\) not found in catalog: bad-tool-1, bad-tool-2"):
        AgentCreateRequest(model_id=model_id, tools=["bad-tool-1", "bad-tool-2"])
