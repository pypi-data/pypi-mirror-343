"""Test the catalog module."""

import json
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from agentfactory_mcp_server.catalog import Catalog, ModelInfo, ToolInfo, load_catalog


def test_load_catalog_happy_path():
    """Test loading the catalog with a valid file."""
    catalog = load_catalog()

    # Verify there are models and tools
    assert len(catalog.models) > 0
    assert len(catalog.tools) > 0

    # Verify specific model and tool exists
    assert any(model.id == "gpt-4.1" for model in catalog.models)
    assert "execution_env_server" in catalog.tools


def test_load_catalog_with_path():
    """Test loading the catalog with a custom path."""
    # Create a temporary catalog file
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({
            "models": [{"id": "test-model", "provider": "test"}],
            "tools": {
                "test-tool": {
                    "command": "test",
                    "args": ["--test"]
                }
            }
        }, f)
        temp_path = f.name

    try:
        catalog = load_catalog(temp_path)
        assert len(catalog.models) == 1
        assert catalog.models[0].id == "test-model"
        assert "test-tool" in catalog.tools
    finally:
        # Clean up
        Path(temp_path).unlink()


def test_load_catalog_file_not_found():
    """Test that FileNotFoundError is raised when the catalog file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_catalog("nonexistent_catalog.json")


def test_catalog_duplicate_model_ids():
    """Test that ValidationError is raised when duplicate model IDs are found."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({
            "models": [
                {"id": "duplicate", "provider": "test1"},
                {"id": "duplicate", "provider": "test2"}
            ],
            "tools": {
                "test-tool": {
                    "command": "test",
                    "args": ["--test"]
                }
            }
        }, f)
        temp_path = f.name

    try:
        with pytest.raises(ValidationError):
            load_catalog(temp_path)
    finally:
        # Clean up
        Path(temp_path).unlink()


def test_catalog_empty_models():
    """Test that ValidationError is raised when no models are specified."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({
            "models": [],
            "tools": {
                "test-tool": {
                    "command": "test",
                    "args": ["--test"]
                }
            }
        }, f)
        temp_path = f.name

    try:
        with pytest.raises(ValidationError):
            load_catalog(temp_path)
    finally:
        # Clean up
        Path(temp_path).unlink()


def test_catalog_empty_tools():
    """Test that ValidationError is raised when no tools are specified."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump({
            "models": [{"id": "test-model", "provider": "test"}],
            "tools": {}
        }, f)
        temp_path = f.name

    try:
        with pytest.raises(ValidationError):
            load_catalog(temp_path)
    finally:
        # Clean up
        Path(temp_path).unlink()


def test_model_info():
    """Test the ModelInfo schema."""
    model = ModelInfo(id="test-model", provider="test")
    assert model.id == "test-model"
    assert model.provider == "test"

    # Test optional provider
    model = ModelInfo(id="test-model")
    assert model.id == "test-model"
    assert model.provider is None


def test_tool_info():
    """Test the ToolInfo schema."""
    tool = ToolInfo(command="test", args=["--test"])
    assert tool.command == "test"
    assert tool.args == ["--test"]
