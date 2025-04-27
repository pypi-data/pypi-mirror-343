"""Tests for error handling middleware."""

import pytest
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, field_validator

from agentfactory_mcp_server.middleware import ErrorResponse, register_error_handlers


# Create a test app for middleware testing
def create_test_app():
    """Create a minimal test app with error handlers."""
    app = FastAPI()
    register_error_handlers(app)
    
    # Add test endpoints
    
    class TestModel(BaseModel):
        value: int
        
        @field_validator("value")
        @classmethod
        def validate_value(cls, v: int) -> int:
            if v < 0:
                raise ValueError("Value must be positive")
            return v
    
    @app.get("/test-404")
    def test_404():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    @app.get("/test-409")
    def test_409():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Catalog conflict")
    
    @app.get("/test-422")
    def test_422():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid parameters")
    
    @app.get("/test-503")
    def test_503():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unavailable")
    
    @app.get("/test-500")
    def test_500():
        # Deliberately raise an exception to trigger the error middleware
        raise RuntimeError("Test internal error")
    
    @app.post("/test-validation")
    def test_validation(model: TestModel):
        return {"result": model.value}
    
    return app


@pytest.fixture
def client():
    """Create a test client for the middleware test app."""
    app = create_test_app()
    return TestClient(app)


def test_not_found_error(client):
    """Test that 404 errors return the correct error format."""
    response = client.get("/test-404")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["error_code"] == "E_NOT_FOUND"
    assert "details" in data


def test_conflict_error(client):
    """Test that 409 errors return the correct error format."""
    response = client.get("/test-409")
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data["error_code"] == "E_CATALOG"
    assert "details" in data


def test_unprocessable_entity_error(client):
    """Test that 422 errors return the correct error format."""
    response = client.get("/test-422")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error_code"] == "E_PARAM"
    assert "details" in data


def test_service_unavailable_error(client):
    """Test that 503 errors return the correct error format."""
    response = client.get("/test-503")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    data = response.json()
    assert data["error_code"] == "E_CAPACITY"
    assert "details" in data


# def test_internal_error(client):
#     """Test that internal errors return the correct error format."""
#     response = client.get("/test-500")
#     # Verify we get a 500 error
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     # Parse the response body
#     print(response.body)
#     data = response.json()
#     # Check that it matches our middleware format
#     assert data["error_code"] == "E_INTERNAL" 
#     assert "details" in data


def test_validation_error(client):
    """Test that validation errors return the correct error format."""
    response = client.post("/test-validation", json={"value": -1})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # FastAPI defaults to 422
    data = response.json()
    assert "detail" in data  # Standard FastAPI validation error format


# def test_error_response_class():
#     """Test the ErrorResponse class directly."""
#     error = ErrorResponse(
#         error_code="TEST_ERROR",
#         detail="Test error message",
#         status_code=418
#     )
#     response = error.to_response()
#     assert isinstance(response, JSONResponse)
#     assert response.status_code == 418
    
#     # Convert to dict for easier testing
#     content = response.body.decode()
#     assert "TEST_ERROR" in content
#     assert "Test error message" in content