import pytest
from agentfactory_mcp_server.database import create_db_and_tables
from server import mcp 
from mcp.server.fastmcp import FastMCP

@pytest.fixture(autouse=True)
def init_db():
    # Ensure DB tables exist for each test
    create_db_and_tables()

@pytest.fixture
def client() -> FastMCP:
    return mcp


# def test_list_models(client: FastMCP):
#     catalog = load_catalog()
#     result = client.
#     assert result == [m.id for m in catalog.models]


# def test_list_tools(client):
#     catalog = load_catalog()
#     result = rpc_call(client, "list_tools", {})
#     assert result == list(catalog.tools.keys())


# def test_create_status_and_terminate(client):
#     catalog = load_catalog()
#     model_id = catalog.models[0].id
#     tool = list(catalog.tools.keys())[0]

#     # create agent
#     create_res = rpc_call(client, "create_agent", {"model_id": model_id, "tools": [tool]})
#     assert "agent_id" in create_res and "expires_at" in create_res
#     agent_id = create_res["agent_id"]

#     # get status
#     status_res = rpc_call(client, "get_agent_status", {"agent_id": agent_id})
#     assert status_res["state"] == "pending"

#     # terminate
#     term_res = rpc_call(client, "terminate_agent", {"agent_id": agent_id})
#     assert "message" in term_res and "Termination request" in term_res["message"]
