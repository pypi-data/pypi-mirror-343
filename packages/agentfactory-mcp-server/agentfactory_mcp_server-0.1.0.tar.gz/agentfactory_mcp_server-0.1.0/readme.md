# AgentFactory-MCP-Server

TODO

## Quick Start

```bash
```

## Docker Runtime

The agent runtime is containerized to provide isolation and resource limits. You can build the Docker image locally with:

```bash
docker build -t agentfactory-runtime .
```

Then run a test agent with:

```bash
docker run --rm -e MODEL_ID=test-model -e TOOL_TEST_CMD=echo -e 'TOOL_TEST_ARGS=["Hello, World!"]' agentfactory-runtime
```

### Runtime Environment Variables

- `MODEL_ID`: The model ID to use for the agent (required)
- `PROMPT`: Optional system/task prompt
- `CONTEXT`: Optional JSON context for the agent
- `TOOL_<n>_CMD`: Command to run for tool <n> (required for at least one tool)
- `TOOL_<n>_ARGS`: JSON array of arguments for tool <n>

For example, to run an agent with the execution environment and browser tools:

```bash
docker run --rm \
  -e MODEL_ID=anthropic:claude-3-7-sonnet-latest \
  -e PROMPT="Help the user with their task" \
  -e 'CONTEXT={"user_request": "Find information about pandas in Python"}' \
  -e TOOL_EXECUTION_ENV_CMD=deno \
  -e 'TOOL_EXECUTION_ENV_ARGS=["run", "-N", "-R=node_modules", "-W=node_modules", "--node-modules-dir=auto", "jsr:@pydantic/mcp-run-python", "stdio"]' \
  -e TOOL_BROWSER_CMD=npx \
  -e 'TOOL_BROWSER_ARGS=["@playwright/mcp@latest"]' \
  agentfactory-runtime
```

## Agent Lifecycle and TTL

Agents have a Time-To-Live (TTL) which defaults to 900 seconds (15 minutes). You can customize this when creating an agent using the `ttl_seconds` parameter (between 60 and 7200 seconds).

The server includes a background task that automatically scans for expired agents and terminates their containers. Agents go through the following states:

1. `pending`: Agent created but container not yet launched
2. `running`: Container is running
3. `succeeded`: Container exited with code 0
4. `failed`: Container exited with non-zero code
5. `expired`: Agent's TTL expired and container was terminated
6. `terminating`: Agent is being manually terminated via API

You can manually terminate a running agent before its TTL expires:

```bash
curl -X DELETE http://localhost:8000/agents/agt_12345678
```

This will send a DELETE request to the server which will terminate the agent's container and update its state.

The agent status can be queried at any time:

```bash
curl http://localhost:8000/agents/agt_12345678/status
```

Which returns:
```json
{
  "state": "running",
  "exit_code": null,
  "started_at": "2025-04-24T12:00:00Z",
  "finished_at": null
}
```

────────────────────────────────────────
    Purpose & Scope
    • Deliver a "manufacturing" service that lets any Model-Context-Protocol (MCP) client spin up short-lived AI agents composed of:
        – ONE LLM back-end chosen from a server-maintained catalog.
        - ONE + tool MCP servers injected into the agent's runtime.


• The service exposes an MCP-compliant REST/streaming API.
• Each agent executes inside an isolated Docker container that runs the uv+pydantic-ai command shown in the prototype.

This spec focuses on the MVP catalog agreed in chat; the design is extensible.

────────────────────────────────────────
2. Functional Requirements
────────────────────────────────────────
2.1 Catalog Endpoints

GET /catalog

→ 200 OK

{
"models": [
"anthropic:claude-3-7-sonnet-latest",
"google-gla:gemini-2.5-flash-preview-04-17",
"gpt-4.1"
],
"tools": [
"execution_env_server",
"browser_server",
"sequential-thinking"
]
}

2.2 Create Agent

POST /agents

Body (JSON, max 32 kB):
{
"model_id": "gpt-4.1",                      // required
"tools": ["execution_env_server"],          // required (≥1)
"agent_name": "opt-label",                  // optional ≤64 chars
"prompt": "optional system/task prompt",    // optional ≤32 kB
"context": {...},                           // optional arbitrary JSON
"ttl_seconds": 1800,                        // optional (default 900, max 7200)
"stream": true                              // optional, default false
}

Success → 201 Created

{
"agent_id": "agt_3f9ba4a0",
"expires_at": "2025-04-24T00:23:11Z",
"stream_url": "wss://…/agents/agt_3f9ba4a0/stream" // only if stream=true
}

2.3 Agent Lifecycle

• GET /agents/{id}/status
{ state: "pending|running|succeeded|failed|expired", exit_code: 0, started_at, finished_at }
• GET /agents/{id}/logs  (non-stream use-case)
• DELETE /agents/{id}    (premature kill; 202 Accepted)

2.4 Streaming

– Server supports Server-Sent-Events or WebSocket; messages are newline-delimited JSON:
{ "stdout": "…" } | { "stderr": "…" } | { "state": "succeeded" }.

2.5 Auth & Quotas

– REST protected by Bearer <api-key> header (issued by operator).
– Provider keys (Anthropic, OpenAI, Google, …) are supplied by caller via env-vars; server does zero storage.
– Optional per-user quota: max concurrent agents, cpu/mem seconds.

────────────────────────────────────────
3. Non-Functional Requirements
────────────────────────────────────────
• Availability ≥99 %.
• Single agent must spin-up ≤3 s P95.
• Hard agent CPU limit: 1 vCPU; RAM 1 GiB.
• Only outbound HTTPS traffic; deny all else.
• Logs and stdout may be transient; retained 24 h then purged.

────────────────────────────────────────
4. High-Level Architecture
────────────────────────────────────────
┌───────────┐          ┌─────────────────────┐
Client ─►  REST API ├────────►│AgentController (Py) │
└───────────┘          │ • validates payload │
│ • launches Docker   │
└─────────▲───────────┘
│
docker run --rm -e … agent-runtime
│
┌───────────┴──────────┐
│  uv + pydantic-ai    │
│  (inside container)  │
└───────────▲──────────┘
│std{out,err}
streamed back / stored

4.1 Tech Choices

– REST layer: FastAPI (async) + Pydantic v2.
– Container engine: Docker with Python 3.11-slim image.
– Deno runtime fetched at container build.
– Async process orchestration: aio-docker or subprocess w/ timeouts.
– DB (ephemeral metadata): SQLite (MVP) behind async-SQLModel.
– Observability: structlog JSON → stdout, Prometheus metrics.

────────────────────────────────────────
5. Container-Runtime Details
────────────────────────────────────────
Dockerfile (sketch):

FROM python:3.11-slim

# system deps
RUN apt-get update && apt-get install -y curl git

# deno
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV DENO_INSTALL=/root/.deno
ENV PATH=$DENO_INSTALL/bin:$PATH

# node + npx
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y nodejs

# python libs
RUN pip install --no-cache-dir uv pydantic-ai fastapi aiohttp uvicorn

WORKDIR /app
COPY runtime_entry.py .

ENTRYPOINT ["python", "runtime_entry.py"]


runtime_entry.py (abbrev):

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
...
agent = Agent(MODEL_ID, mcp_servers=BUILD_TOOL_LIST_FROM_ENV())
async with agent.run_mcp_servers():
    result = await agent.run(PROMPT_OR_CONTEXT)
print(result.output)


The AgentController injects ENV vars:
MODEL_ID, PROMPT_OR_CONTEXT, TOOL_x_CMD, TOOL_x_ARGSjson.

────────────────────────────────────────
6. Data Validation & Error Handling
────────────────────────────────────────
• 400  – Schema / field errors → {error_code:"E_SCHEMA",details:…}

• 403  – Bad API key → "E_AUTH"

• 404  – Unknown agent id → "E_NOT_FOUND"

• 409  – Invalid model/tool choice → "E_CATALOG"

• 422  – Unsupported TTL or payload size → "E_PARAM"

• 500  – Internal (logged w/ request_id)

• 503  – Capacity / docker spawn failure → "E_CAPACITY", Retry-After hdr.

────────────────────────────────────────
7. Security
────────────────────────────────────────
• Docker run flags:

–‐cpus 1 –‐memory 1g –‐pids-limit 256 –‐network none (except if browser_server needs net: we create a separate net namespace with egress only 443).

• seccomp & no-new-privs.
• TMPFS for /tmp; no host mounts.
• Validate tool/model names against allow-list (static JSON).

────────────────────────────────────────
8. Catalog Implementation
────────────────────────────────────────
catalog.json:

{
  "models": [
    {"id":"anthropic:claude-3-7-sonnet-latest","provider":"anthropic"},
    {"id":"google-gla:gemini-2.5-flash-preview-04-17","provider":"google-gla"},
    {"id":"gpt-4.1","provider":"openai"}
  ],
  "tools": {
    "execution_env_server": {
      "command":"deno",
      "args":[
        "run","-N","-R=node_modules","-W=node_modules",
        "--node-modules-dir=auto",
        "jsr:@pydantic/mcp-run-python","stdio"
      ]
    },
    "browser_server": {
      "command":"npx",
      "args":["@playwright/mcp@latest"]
    },
    "sequential-thinking": {
      "command":"npx",
      "args":["-y","@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}


────────────────────────────────────────
9. Configuration
────────────────────────────────────────
env file or helm values:
SERVER_PORT=8000

API_KEYS=csv_of_valid_keys

MAX_CONCURRENT_AGENTS=20

DEFAULT_TTL=900

LOG_LEVEL=info

────────────────────────────────────────
10. Logging & Observability
────────────────────────────────────────
• Each HTTP request: request_id, path, status, duration.

• Agent events: create, start, stdout bytes, exit, ttl_expire.

• Metrics: active_agents gauge, agent_duration histogram, agent_fail_total counter.

• Export Prometheus at /metrics.

────────────────────────────────────────
11. Testing Plan
────────────────────────────────────────
11.1 Unit Tests (pytest)

– Payload pydantic validation: success & failure cases.
– Catalog loading / unknown IDs.
– TTL enforcement logic.

11.2 Integration Tests

– Spin docker-in-docker (testcontainers-python).
– POST /agents → wait → GET /status == succeeded.
– Validate that stdout matches expected on deterministic prompt.

11.3 Failure Injection

– Force tool command not found ⇒ expect agent.state == failed.
– Kill container mid-run ⇒ server surfaces "E_RUNTIME_CRASH".

11.4 Load / Concurrency

– Locust script: ramp to MAX_CONCURRENT_AGENTS*2, P95 create ≤3 s.

11.5 Security Tests

– Attempt to mount host dir ⇒ expect denied.
– Network egress test when network none.

11.6 CI Pipeline

– GitHub Actions: lint → unit → integ (in docker-in-docker) → build image → push registry.

────────────────────────────────────────
12. Milestones
────────────────────────────────────────


    REST skeleton & catalog loader … 1 week
    Docker runtime & happy-path agent execution … 1 week
    Streaming layer & TTL cleanup … 1 week
    Metrics, quotas, docs, CI … 1 week
    Hardening, load test, first deployment … 1 week


────────────────────────────────────────
13. References
────────────────────────────────────────
• MCP spec docs (internal).
• Pydantic-AI project README.
• Good practice on writing comprehensive specs mayvenstudios.com
• JSON context schema inspiration github.com

────────────────────────────────────────
END OF SPEC