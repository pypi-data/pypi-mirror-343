"""Catalog loader module for AgentFactory MCP Server."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator


class ModelInfo(BaseModel):
    """Model information schema."""

    id: str
    provider: Optional[str] = None


class ToolInfo(BaseModel):
    """Tool information schema."""

    command: str
    args: List[str]


class Catalog(BaseModel):
    """Catalog schema containing models and tools."""

    models: List[ModelInfo]
    tools: Dict[str, ToolInfo]

    @model_validator(mode="after")
    def validate_unique_model_ids(self) -> "Catalog":
        """Validate that model IDs are unique."""
        model_ids = [model.id for model in self.models]
        if len(model_ids) != len(set(model_ids)):
            raise ValueError("Model IDs must be unique")
        if not model_ids:
            raise ValueError("At least one model must be specified")
        if not self.tools:
            raise ValueError("At least one tool must be specified")
        return self


@lru_cache(maxsize=1)
def load_catalog(path: Optional[Union[str, Path]] = None) -> Catalog:
    """
    Load and parse the catalog file.

    Args:
        path: Optional path to the catalog file. If not provided, it will look for
            catalog.json in the current directory.

    Returns:
        Catalog: A validated catalog object.

    Raises:
        FileNotFoundError: If the catalog file doesn't exist.
        ValidationError: If the catalog file is invalid.
    """
    if path is None:
        path = Path("catalog.json")
    else:
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Catalog file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Catalog.model_validate(data)