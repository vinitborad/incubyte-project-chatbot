"""
Simple unit tests for main.py FastAPI application.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage
import os


class TestMainApp:
    """Basic tests for FastAPI application."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with patch.dict(os.environ, {"REDIS_URL": "redis://localhost:6379"}):
            with patch("main.get_agent_with_history"):
                from main import app

                return TestClient(app)

    @patch("main.get_agent_with_history")
    def test_chat_endpoint_success(self, mock_get_agent, client):
        """Test successful chat endpoint call."""
        # Arrange
        mock_agent = Mock()
        mock_agent.return_value = AIMessage(content="Here are our available sweets!")
        mock_get_agent.return_value = mock_agent

        request_data = {
            "message": "What sweets do you have?",
            "session_id": "test_session_123",
        }

        # Act
        response = client.post("/chat", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "Here are our available sweets!"

    def test_chat_endpoint_missing_session_id(self, client):
        """Test chat endpoint with missing session_id."""
        # Arrange
        request_data = {"message": "Hello", "session_id": ""}

        # Act
        response = client.post("/chat", json=request_data)

        # Assert
        assert response.status_code == 400

    def test_chat_endpoint_missing_message(self, client):
        """Test chat endpoint with missing message field."""
        # Arrange
        request_data = {"session_id": "test_session"}

        # Act
        response = client.post("/chat", json=request_data)

        # Assert
        assert response.status_code == 422  # Validation error

    def test_api_documentation_accessible(self, client):
        """Test that API documentation endpoints are accessible."""
        # Act
        docs_response = client.get("/docs")
        openapi_response = client.get("/openapi.json")

        # Assert
        assert docs_response.status_code == 200
        assert openapi_response.status_code == 200
