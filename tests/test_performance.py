"""
Simple performance tests for the chatbot system.
"""

import pytest
from unittest.mock import patch, Mock
import time


class TestBasicPerformance:
    """Basic performance tests for critical components."""

    @patch("tools.get_all_sweets")
    def test_get_sweets_response_time(self, mock_get_sweets):
        """Test that getting sweets responds within reasonable time."""
        # Arrange
        mock_get_sweets.return_value = [
            {"name": "Gulab Jamun", "price": 50, "quantity": 10}
        ]

        from tools import get_available_sweets

        # Act
        start_time = time.time()
        result = get_available_sweets.invoke("")
        end_time = time.time()

        # Assert
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
        assert "Gulab Jamun" in result

    @patch("chatbot.get_agent_with_history")
    def test_agent_creation_time(self, mock_get_agent):
        """Test that agent creation is reasonably fast."""
        # Arrange
        mock_agent = Mock()
        mock_get_agent.return_value = mock_agent

        # Act
        start_time = time.time()
        agent = mock_get_agent(session_id="test", redis_url="redis://localhost")
        end_time = time.time()

        # Assert
        creation_time = end_time - start_time
        assert creation_time < 2.0  # Should create within 2 seconds
        assert agent is not None
