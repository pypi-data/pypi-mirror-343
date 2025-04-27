"""Pydantic schemas for API request and response payloads."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from agentfactory_mcp_server.catalog import load_catalog


class AgentCreateRequest(BaseModel):
    """Request model for creating a new agent."""

    model_id: str = Field(description="The model ID to use for the agent")
    tools: List[str] = Field(min_length=1, description="List of tool IDs to use (at least one required)")
    agent_name: Optional[str] = Field(
        None, max_length=64, description="Optional label for the agent (max 64 chars)"
    )
    prompt: Optional[str] = Field(
        None, max_length=32768, description="Optional system/task prompt (max 32 KB)"
    )
    context: Optional[Dict[str, Any]] = Field(
        None, description="Optional arbitrary JSON context for the agent"
    )
    ttl_seconds: Optional[int] = Field(
        default=900,
        ge=60,
        le=7200,
        description="Time-to-live in seconds (60-7200, default 900)",
    )
    stream: bool = Field(False, description="Whether to stream agent output")

    @field_validator("agent_name")
    @classmethod
    def validate_agent_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate agent_name is not empty if provided."""
        if v is not None and v.strip() == "":
            raise ValueError("agent_name must not be empty if provided")
        return v

    @model_validator(mode="after")
    def validate_model_and_tools(self) -> "AgentCreateRequest":
        """Validate that the model_id and tools exist in the catalog."""
        catalog = load_catalog()
        
        # Validate model_id
        model_ids = [model.id for model in catalog.models]
        if self.model_id not in model_ids:
            raise ValueError(f"Model '{self.model_id}' not found in catalog")
            
        # Validate tools
        available_tools = set(catalog.tools.keys())
        invalid_tools = [tool for tool in self.tools if tool not in available_tools]
        if invalid_tools:
            raise ValueError(f"Tool(s) not found in catalog: {', '.join(invalid_tools)}")
            
        return self


class AgentStatusResponse(BaseModel):
    """Response model for agent status endpoint."""

    state: str = Field(
        description="Current state of the agent", 
        example="pending"
    )
    exit_code: Optional[int] = Field(
        None, 
        description="Exit code of the agent process (null if not finished)",
        example=0
    )
    started_at: Optional[datetime] = Field(
        None, 
        description="When the agent was started (null if not started)"
    )
    finished_at: Optional[datetime] = Field(
        None, 
        description="When the agent finished (null if not finished)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "state": "succeeded",
                "exit_code": 0,
                "started_at": "2025-04-24T00:00:00Z",
                "finished_at": "2025-04-24T00:01:30Z"
            }
        }