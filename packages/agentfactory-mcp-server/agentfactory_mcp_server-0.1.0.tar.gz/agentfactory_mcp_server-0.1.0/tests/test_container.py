"""Integration tests for container functionality using testcontainers."""

import pytest
import os
import shutil
import tempfile
from pathlib import Path
import json
import time

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from agentfactory_mcp_server.database import AgentMeta
import datetime


@pytest.fixture(scope="module")
def docker_image():
    """Build a test Docker image for the tests."""
    # Create a temporary directory for the Dockerfile
    temp_dir = tempfile.mkdtemp()
    try:
        # Copy the hello_runtime.py to the temp directory
        shutil.copy(
            os.path.join(os.path.dirname(__file__), "hello_runtime.py"),
            os.path.join(temp_dir, "hello_runtime.py")
        )
        
        # Create a simple Dockerfile
        dockerfile_path = os.path.join(temp_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write("""FROM python:3.12-slim
WORKDIR /app
COPY hello_runtime.py .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "hello_runtime.py"]
""")
        
        # Build the image
        image_name = "agentfactory-test:latest"
        os.system(f"docker build -t {image_name} {temp_dir}")
        
        yield image_name
        
        # Cleanup - remove the image
        os.system(f"docker rmi {image_name}")
    finally:
        # Remove the temporary directory
        shutil.rmtree(temp_dir)


@pytest.mark.integration
def test_container_runs_with_environment(docker_image):
    """Test that the container runs with the provided environment variables."""
    # Create test environment variables
    env = {
        "AGENT_ID": "agt_test1234",
        "MODEL_ID": "test-model",
        "TOOL_0_CMD": "deno",
        "TOOL_0_ARGS": json.dumps(["run", "stdio"]),
        "PROMPT": "Hello, world!",
        "CONTEXT": json.dumps({"test": "value"})
    }
    
    # Start container with environment variables
    container = DockerContainer(docker_image)
    for key, value in env.items():
        container.with_env(key, value)
    
    # Run the container
    with container:
        # Wait for the container to finish
        exit_code = container.get_wrapped_container().wait()["StatusCode"]
        logs = container.get_logs()
        # siily solution for the output looking like this: (b'Hello from the test runtime!\nAgent ID: agt_test1...)
        logs = list(map(lambda log: log.decode('utf-8').split('\n'), logs))
        logs = [line for log in logs for line in log if line.strip()]
        
        # Verify exit code
        assert exit_code == 0
        
        # Verify logs contain expected output
        assert "Hello from the test runtime!" in logs
        assert f"Agent ID: {env['AGENT_ID']}" in logs
        assert f"Model ID: {env['MODEL_ID']}" in logs
        assert "Found 1 tools" in logs
        assert f"Prompt: {env['PROMPT']}" in logs


@pytest.fixture
def agent_meta():
    """Create a sample agent metadata object."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=900)
    
    return AgentMeta(
        id="agt_test1234",
        model_id="test-model",
        tools={
            "tool_ids": ["execution_env_server"],
            "prompt": "Test prompt",
            "context": {"key": "value"}
        },
        state="pending",
        created_at=now,
        expires_at=expires_at,
    )


@pytest.mark.integration
def test_container_with_agent_meta(docker_image, agent_meta):
    """Test running a container with agent metadata."""
    # Format environment variables from agent metadata
    env = {
        "AGENT_ID": agent_meta.id,
        "MODEL_ID": agent_meta.model_id,
        "TOOL_0_CMD": "deno",
        "TOOL_0_ARGS": json.dumps(["run", "stdio"]),
        "PROMPT": agent_meta.tools.get("prompt"),
        "CONTEXT": json.dumps(agent_meta.tools.get("context"))
    }
    
    # Start container with environment variables
    container = DockerContainer(docker_image)
    for key, value in env.items():
        container.with_env(key, value)
    
    # Run the container
    with container:
        # Wait for the container to finish
        exit_code = container.get_wrapped_container().wait()["StatusCode"]
        logs = container.get_logs()
        logs = list(map(lambda log: log.decode('utf-8').split('\n'), logs))
        logs = [line for log in logs for line in log if line.strip()]

        
        # Verify exit code
        assert exit_code == 0
        
        # Verify logs contain expected output
        assert f"Agent ID: {agent_meta.id}" in logs
        assert f"Model ID: {agent_meta.model_id}" in logs