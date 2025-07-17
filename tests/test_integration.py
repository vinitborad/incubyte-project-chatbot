"""
Simple integration tests for the chatbot system.
"""

import pytest
from unittest.mock import patch, Mock
import json


class TestBasicIntegration:
    """Basic integration tests to verify components work together."""

    @patch("tools.get_all_sweets")
    def test_get_sweets_flow(self, mock_get_sweets):
        """Test basic flow of getting available sweets."""
        # Arrange
        mock_get_sweets.return_value = [
            {"name": "Gulab Jamun", "price": 50, "quantity": 10}
        ]

        from tools import get_available_sweets

        # Act
        result = get_available_sweets.invoke("")

        # Assert
        assert "Gulab Jamun" in result
        assert "50" in result
        mock_get_sweets.assert_called_once()

    @patch("tools.get_all_sweets")
    @patch("tools.requests.get")
    @patch("tools.requests.post")
    def test_buy_sweet_flow(self, mock_post, mock_get, mock_get_sweets):
        """Test basic flow of buying a sweet."""
        # Arrange
        mock_get_sweets.return_value = [
            {"name": "Gulab Jamun", "price": 50, "quantity": 10}
        ]

        # Mock the search response
        mock_search_response = Mock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = [
            {"_id": "sweet123", "name": "Gulab Jamun"}
        ]
        mock_get.return_value = mock_search_response

        # Mock the purchase response
        mock_purchase_response = Mock()
        mock_purchase_response.status_code = 200
        mock_purchase_response.json.return_value = {"success": True}
        mock_post.return_value = mock_purchase_response

        from tools import buy_sweet

        # Act - Use proper input format for LangChain tool
        result = buy_sweet.invoke({"sweet_name": "Gulab Jamun", "quantity": 2})

        # Assert
        assert "success" in result.lower()
        mock_get.assert_called_once()
        mock_post.assert_called_once()

    @patch("chatbot.get_agent_with_history")
    def test_agent_creation(self, mock_get_agent):
        """Test that agent can be created successfully."""
        # Arrange
        mock_agent = Mock()
        mock_get_agent.return_value = mock_agent

        # Act
        agent = mock_get_agent(session_id="test", redis_url="redis://localhost")

        # Assert
        assert agent is not None
        mock_get_agent.assert_called_once_with(
            session_id="test", redis_url="redis://localhost"
        )
