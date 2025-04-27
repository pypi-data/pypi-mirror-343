from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
from contextlib import asynccontextmanager
from typing import AsyncIterator
from dataclasses import dataclass
from agentfactory_mcp_server.catalog import load_catalog
from agentfactory_mcp_server.database import (
    AgentMeta,
    create_agent as create_agent_in_db,
    create_db_and_tables,
    get_agent_by_id,
    update_agent_state,
)
from agentfactory_mcp_server.runner import launch_agent
from agentfactory_mcp_server.database import get_session
from agentfactory_mcp_server.database import Session
from agentfactory_mcp_server.cleanup import cleanup_task

@dataclass
class AppContext:
    db: Session

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    # Validate catalog, initialize DB, start cleanup task
    load_catalog()
    create_db_and_tables()
    db = get_session()
    await cleanup_task.start()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        await cleanup_task.stop()

# Create MCP server instance
mcp = FastMCP(name="AgentFactory MCP Server", lifespan=app_lifespan)

# -- Immediate endpoints --

@mcp.resource("catalog://models")
def list_models() -> List[str]:
    """List available model IDs"""
    catalog = load_catalog()
    return [model.id for model in catalog.models]

@mcp.resource("catalog://tools")
def list_tools() -> List[str]:
    """List available tool names"""
    catalog = load_catalog()
    return list(catalog.tools.keys())

@mcp.tool()
async def create_agent(
    model_id: str,
    tools: List[str],
    prompt: Optional[str] = None,
    context: Optional[Dict] = None,
    ttl_seconds: int = 900,
    stream: bool = False,
) -> Dict:
    """Create a new agent and launch its container"""
    # Validate model and tools against catalog
    catalog = load_catalog()
    if model_id not in [m.id for m in catalog.models]:
        raise ValueError(f"Invalid model_id: {model_id}")
    invalid_tools = [t for t in tools if t not in catalog.tools]
    if invalid_tools:
        raise ValueError(f"Invalid tools: {invalid_tools}")
    agent_id = AgentMeta.create_id()
    tools_dict = {"tool_ids": tools}
    if prompt:
        tools_dict["prompt"] = prompt
    if context:
        tools_dict["context"] = context
    agent = create_agent_in_db(
        agent_id=agent_id,
        model_id=model_id,
        tools=tools_dict,
        ttl_seconds=ttl_seconds,
    )
    success, error = await launch_agent(agent)
    if not success:
        raise RuntimeError(f"Failed to launch agent container: {error}")
    result: Dict = {"agent_id": agent.id, "expires_at": agent.expires_at}
    if stream:
        # Stream URL provided by MCP transport configuration
        result["stream_url"] = f"wss://{mcp.server_url}/agents/{agent.id}/stream"
    return result

@mcp.tool()
def get_agent_status(agent_id: str) -> Dict:
    """Get the status of an existing agent"""
    agent = get_agent_by_id(agent_id)
    if not agent:
        raise RuntimeError(f"Agent with ID {agent_id} not found")
    return agent.to_status_dict()

@mcp.tool()
async def terminate_agent(agent_id: str) -> Dict:
    """Terminate an agent prematurely"""
    agent = get_agent_by_id(agent_id)
    if not agent:
        raise RuntimeError(f"Agent with ID {agent_id} not found")
    if agent.state in ["succeeded", "failed", "expired"]:
        return {"message": f"Agent {agent_id} is already in terminal state: {agent.state}"}
    await cleanup_task._kill_container(agent_id)
    update_agent_state(agent_id, "terminating")
    return {"message": f"Termination request for agent {agent_id} accepted"}

