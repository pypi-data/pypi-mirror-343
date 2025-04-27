"""Database models and utilities for AgentFactory."""

import datetime
import json
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import Field
from sqlalchemy import Column, JSON, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, create_engine, select


class AgentMeta(SQLModel, table=True):
    """Metadata for an agent instance."""

    id: str = Field(primary_key=True)
    model_id: str
    tools: Dict[str, Any] = Field(sa_column=Column(JSON))
    state: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None
    exit_code: Optional[int] = None

    @classmethod
    def create_id(cls) -> str:
        """Generate a unique agent ID prefixed with 'agt_'."""
        return f"agt_{uuid.uuid4().hex[:8]}"
    
    @property
    def is_expired(self) -> bool:
        """Check if the agent has expired."""
        return datetime.datetime.now(datetime.timezone.utc) > self.expires_at
    
    def to_status_dict(self) -> Dict[str, Any]:
        """Convert to a status dictionary."""
        return {
            "state": self.state,
            "exit_code": self.exit_code,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


# Create engine and session factory
DATABASE_URL = "sqlite:///data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Create a new database session."""
    return Session(engine)


@contextmanager
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_agent_by_id(agent_id: str) -> Optional[AgentMeta]:
    """
    Get an agent by its ID.
    
    Args:
        agent_id: The ID of the agent to retrieve.
        
    Returns:
        The agent metadata or None if not found.
    """
    with get_db_session() as session:
        return session.exec(select(AgentMeta).where(AgentMeta.id == agent_id)).first()


def list_agents() -> List[AgentMeta]:
    """
    Get a list of all agents.
    
    Returns:
        A list of all agent metadata.
    """
    with get_db_session() as session:
        return session.exec(select(AgentMeta)).all()


def create_agent(agent_id: str, model_id: str, tools: Dict[str, Any], ttl_seconds: int) -> AgentMeta:
    """
    Create a new agent in the database.
    
    Args:
        agent_id: The ID of the agent.
        model_id: The model ID to use for the agent.
        tools: Dictionary containing tool_ids and optional prompt and context.
        ttl_seconds: The time-to-live in seconds.
        
    Returns:
        The created agent metadata.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=ttl_seconds)
    
    agent = AgentMeta(
        id=agent_id,
        model_id=model_id,
        tools=tools,
        state="pending",
        created_at=now,
        expires_at=expires_at,
    )
    
    with get_db_session() as session:
        session.add(agent)
        session.commit()
        session.refresh(agent)
        return agent


def update_agent_state(agent_id: str, state: str, exit_code: Optional[int] = None) -> bool:
    """
    Update the state of an agent.
    
    Args:
        agent_id: The ID of the agent to update.
        state: The new state value.
        exit_code: Optional exit code if the agent has finished.
        
    Returns:
        True if the agent was found and updated, False otherwise.
    """
    with get_db_session() as session:
        agent = session.exec(select(AgentMeta).where(AgentMeta.id == agent_id)).first()
        if agent:
            now = datetime.datetime.now(datetime.timezone.utc)
            
            # Set started_at if transitioning to running
            if state == "running" and agent.state != "running" and not agent.started_at:
                agent.started_at = now
            
            # Set finished_at and exit_code if transitioning to a terminal state
            if state in ("succeeded", "failed", "expired") and not agent.finished_at:
                agent.finished_at = now
                if exit_code is not None:
                    agent.exit_code = exit_code
            
            agent.state = state
            session.add(agent)
            session.commit()
            return True
        return False