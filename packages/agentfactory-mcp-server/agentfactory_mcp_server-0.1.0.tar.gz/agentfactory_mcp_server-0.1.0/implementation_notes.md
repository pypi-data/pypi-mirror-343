# Implementation Notes

## Phase C3 — TTL & Cleanup

### Overview
Implemented TTL (Time-To-Live) enforcement and container cleanup for agents. This includes automatic expiration of agents based on their TTL as well as manual termination via the API.

### Key Components

1. **Background Cleanup Task**
   - Created a background task that scans the database for expired agents
   - Automatically terminates containers for expired agents
   - Updates agent state in the database

2. **Agent Termination API**
   - Added DELETE /agents/{id} endpoint for manual termination
   - Returns 202 Accepted status code for successful termination requests
   - Provides appropriate error handling and status messages

3. **Agent Lifecycle States**
   - Enhanced agent state management with new states:
     - `pending`: Initial state when agent is created
     - `running`: Container is running
     - `succeeded`: Container exited with code 0
     - `failed`: Container exited with non-zero code
     - `expired`: TTL expired and container was terminated
     - `terminating`: Being manually terminated via API

4. **Testing**
   - Unit tests with mocked clock for TTL enforcement
   - Tests for agent termination API
   - Integration tests using testcontainers-python

5. **Documentation**
   - Updated README with TTL and agent lifecycle information
   - Added API documentation for the termination endpoint

### Implementation Details

1. **CleanupTask Class**
   - Asynchronous background task that runs at configurable intervals
   - Uses Docker SDK to kill containers for expired agents
   - Updates agent state to "expired" when TTL is reached
   - Proper error handling for Docker connections and container operations

2. **Agent Termination Logic**
   - Asynchronous container termination to avoid blocking the API
   - State transitions: running -> terminating -> expired
   - Proper cleanup of container resources

3. **Integration with FastAPI**
   - Task started during application startup
   - Task gracefully stopped during application shutdown
   - Efficient database queries to find expired agents

### Benefits
- Ensures resources are properly cleaned up and not leaked
- Provides control over agent lifecycle for users
- Maintains system stability under load by enforcing resource limits
- Prevents runaway containers from consuming excessive resources