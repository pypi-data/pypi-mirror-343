# Comprehensive Blueprint & Incremental Implementation Plan
(for “agentfactory-mcp-server” MVP)

This document is divided into four sections:

1. High-level blueprint (phases & rationale).
2. Three-level work-breakdown (phase → iteration → atomic step).
3. Review & right-sizing check.
4. A sequence of ready-to-copy prompts (each in its own code-block) for a code-generation LLM to implement every atomic step in a fully test-driven, incremental way.

Where useful, prompt–engineering-style insights from agent-building guidelines such as the “Agentic Building Blocks” gist [gist.github.com](https://gist.github.com/disler/409d9685c8b251ed723a7aca43cc4b9b) are cited to reinforce best practices around modularity and fallbacks.

---

## 1. High-Level Blueprint

PHASE A — Foundation
• Repository, tooling, CI skeleton, catalog loader, health endpoint.

PHASE B — Core API
• GET /catalog
• POST /agents (validation only)
• Persistent metadata store

PHASE C — Agent Runtime
• Docker image build
• Container launcher + TTL cleanup
• stdout capture

PHASE D — UX Endpoints & Streaming
• GET /agents/{id}/status
• logs & stream (SSE/WS)

PHASE E — Hardening
• Auth, quotas, metrics, error codes, security tests.

PHASE F — Stretch
• browser_server network ns, load test harness, deployment scripts.

---

## 2. Three-Level Work-Breakdown

Level 1 = Phase → Level 2 = Iteration (≈½-day) → Level 3 = Atomic Step (≈30-60 min)

### Phase A — Foundation
| Iter | Atomic Steps |
|------|--------------|
|A1 Repo & Tooling|A1-1 Init git repo, add README + LICENSE.<br>A1-2 Add pyproject (Poetry) + requirements lock.<br>A1-3 Add pre-commit (black, isort, flake8, mypy).<br>A1-4 Add GitHub Action “lint & unit”.|
|A2 Catalog Loader|A2-1 Define catalog.json (models & tools).<br>A2-2 Implement `agentfactory.catalog` loader w/ pydantic model.<br>A2-3 Unit tests for happy & sad paths.|
|A3 Health Endpoint|A3-1 Scaffold FastAPI app.<br>A3-2 Implement GET /health return 200 OK JSON.<br>A3-3 Integration test via httpx.|

### Phase B — Core API
| Iter | Atomic Steps |
|------|--------------|
|B1 GET /catalog|B1-1 Wire endpoint returning loader output.<br>B1-2 Add schema examples to OpenAPI.<br>B1-3 Integration tests.|
|B2 POST /agents (validation)|B2-1 Define AgentCreateRequest pydantic model.<br>B2-2 Validate against catalog; persist stub row in SQLite (state=pending).<br>B2-3 Return 201 + agent_id.<br>B2-4 Unit + integration tests.|
|B3 Metadata Access|B3-1 Implement GET /agents/{id}/status (reads DB).<br>B3-2 404 & E_SCHEMA error handling middleware.<br>B3-3 Tests.|

### Phase C — Agent Runtime <- *Currently Here*
| Iter | Atomic Steps |
|------|--------------|
|C1 Docker Base Image|C1-1 Create Dockerfile per spec.<br>C1-2 GitHub Action builds & pushes image.<br>C1-3 Image smoke test in CI.|
|C2 Container Launcher|C2-1 Implement `runner.launch_agent(agent_row)` using python-docker sdk.<br>C2-2 Write minimal “hello” runtime_entry.py injected as CMD.<br>C2-3 Update status to running/finished; capture exit code.<br>C2-4 Tests with testcontainers-python.|
|C3 TTL & Cleanup|C3-1 Background task scans DB for expired agents and kills containers.<br>C3-2 Unit tests with mocked clock.|

### Phase D — UX & Streaming
| Iter | Atomic Steps |
|------|--------------|
|D1 Logs Endpoint|D1-1 Persist stdout/err chunks to tmp dir / DB.<br>D1-2 GET /agents/{id}/logs returns paged JSON.<br>D1-3 Tests.|
|D2 SSE / WS Stream|D2-1 Implement `/agents/{id}/stream` (fastapi-sse).<br>D2-2 Propagate container output in real time.<br>D2-3 Add integration test with websocket client.|
|D3 Delete Endpoint|D3-1 DELETE /agents/{id} → kill & mark “cancelled”.<br>D3-2 Tests.|

### Phase E — Hardening
| Iter | Atomic Steps |
|------|--------------|
|E1 Auth & Quota|E1-1 API-key header middleware.<br>E1-2 Per-key concurrent agent limit.<br>E1-3 Tests.|
|E2 Metrics & Logging|E2-1 Expose /metrics Prometheus.<br>E2-2 structlog JSON conf.<br>E2-3 Alert rules sample.|
|E3 Security Tests|E3-1 Add seccomp profile; unit test container args.<br>E3-2 Snyk / Trivy scan in CI.|

### Phase F — Stretch
| Iter | Atomic Steps |
|------|--------------|
|F1 Network Namespaces|F1-1 Conditional `--network` none|bridge for browser tool.<br>F1-2 E2E test hitting example.com via browser_server.|
|F2 Load Testing|F2-1 Locust file; CI smoke perf.<br>F2-2 Report template.|

---

## 3. Right-Sizing Review

• Each atomic step is ≤ ~150 lines diff; introduces one concept.
• Every iteration ends in green CI; nothing is half-wired.
• First external dependency (Docker) appears only at Phase C after core API is solid.
• Failure modes & tests added the same iteration where feature lands (mirrors practices recommended in agentic “fallback chains” [gist.github.com](https://gist.github.com/disler/409d9685c8b251ed723a7aca43cc4b9b)).

Result: safe, incremental, yet forward-moving.

---

## 4. Code-Generation LLM Prompts (one per atomic step)

Each prompt is self-contained, references only prior-merged code, and demands TDD (pytest first). Copy-paste directly into your favorite coding-LLM.
Prompts are fenced with ```text so they’re treated as plain text.

> NOTE: Replace `YOUR_GH_ORG/agentfactory` with actual repo.
> All prompts assume Python 3.11, Poetry, FastAPI, and pytest.

---
