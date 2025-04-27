"""Background task for TTL enforcement and container cleanup."""

import asyncio
import datetime
import logging
import time
from typing import List, Optional

import docker
from docker.errors import DockerException, NotFound

from agentfactory_mcp_server.database import AgentMeta, get_db_session, update_agent_state
from sqlmodel import select

# Configure logging
logger = logging.getLogger(__name__)

# Default cleanup interval in seconds
DEFAULT_CLEANUP_INTERVAL = 60


class CleanupTask:
    """Background task for cleaning up expired agents and their containers."""

    def __init__(
        self, 
        cleanup_interval: int = DEFAULT_CLEANUP_INTERVAL,
        docker_client: Optional[docker.DockerClient] = None
    ):
        """
        Initialize the cleanup task.
        
        Args:
            cleanup_interval: Interval in seconds between cleanup runs
            docker_client: Optional Docker client for testing with mocks
        """
        self.cleanup_interval = cleanup_interval
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
        self._docker_client = docker_client
    
    async def start(self) -> None:
        """Start the background cleanup task."""
        if self.is_running:
            logger.warning("Cleanup task is already running")
            return
            
        self.is_running = True
        self.task = asyncio.create_task(self._run_cleanup_loop())
        logger.info("Started agent cleanup task")
    
    async def stop(self) -> None:
        """Stop the background cleanup task."""
        if not self.is_running or not self.task:
            logger.warning("Cleanup task is not running")
            return
            
        self.is_running = False
        if not self.task.done():
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                logger.info("Cleanup task cancelled")
        logger.info("Stopped agent cleanup task")
    
    async def _run_cleanup_loop(self) -> None:
        """Main cleanup loop that runs at regular intervals."""
        while self.is_running:
            try:
                expired_count = await self.cleanup_expired_agents()
                if expired_count > 0:
                    logger.info(f"Cleaned up {expired_count} expired agents")
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
            
            # Wait for the next cleanup interval
            await asyncio.sleep(self.cleanup_interval)
    
    async def cleanup_expired_agents(self) -> int:
        """
        Find and clean up expired agents.
        
        Returns:
            int: Number of agents cleaned up
        """
        # Get current time in UTC
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Get expired agents from the database
        expired_agents = await self._get_expired_agents(now)
        
        # Clean up each expired agent
        cleanup_count = 0
        for agent in expired_agents:
            if await self._cleanup_agent(agent):
                cleanup_count += 1
        
        return cleanup_count
    
    async def _get_expired_agents(self, now: datetime.datetime) -> List[AgentMeta]:
        """
        Get a list of expired agents from the database.
        
        Args:
            now: Current time for comparison
            
        Returns:
            List of expired agent metadata
        """
        with get_db_session() as session:
            # Find agents that have expired but aren't marked as expired yet
            query = select(AgentMeta).where(
                (AgentMeta.expires_at < now) & 
                (AgentMeta.state.notin_(["expired", "succeeded", "failed"]))
            )
            return session.exec(query).all()
    
    async def _cleanup_agent(self, agent: AgentMeta) -> bool:
        """
        Clean up a single expired agent.
        
        Args:
            agent: The agent metadata to clean up
            
        Returns:
            bool: True if the agent was successfully cleaned up
        """
        try:
            # Try to kill the agent's container if it's still running
            await self._kill_container(agent.id)
            
            # Mark the agent as expired in the database
            update_agent_state(agent.id, "expired", exit_code=None)
            
            logger.info(f"Cleaned up expired agent {agent.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clean up agent {agent.id}: {e}")
            return False
    
    async def _kill_container(self, agent_id: str) -> bool:
        """
        Kill the container for an agent.
        
        Args:
            agent_id: The ID of the agent
            
        Returns:
            bool: True if the container was killed or not found
        """
        try:
            # Get or create Docker client
            client = self._docker_client or docker.from_env()
            
            # Try to get and kill the container
            container_name = f"agent-{agent_id}"
            try:
                # Run these operations in a thread since they're blocking calls
                loop = asyncio.get_event_loop()
                
                # Get container
                container = await loop.run_in_executor(
                    None, lambda: client.containers.get(container_name)
                )
                
                # Kill container
                await loop.run_in_executor(
                    None, container.kill
                )
                
                logger.info(f"Killed container for agent {agent_id}")
                return True
            except NotFound:
                # Container doesn't exist, which is fine
                logger.debug(f"No container found for agent {agent_id}")
                return True
                
        except DockerException as e:
            logger.error(f"Docker error killing container for agent {agent_id}: {e}")
            return False


# Singleton instance for the application
cleanup_task = CleanupTask()