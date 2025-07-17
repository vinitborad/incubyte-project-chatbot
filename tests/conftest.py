"""
Simple test fixtures for the sweet shop chatbot project.
"""

import pytest
from unittest.mock import Mock
from langchain_core.messages import AIMessage, HumanMessage


@pytest.fixture
def sample_sweets_data():
    """Sample sweets data for testing."""
    return [
        {"name": "Gulab Jamun", "price": 25.50, "quantity": 10},
        {"name": "Rasgulla", "price": 20.00, "quantity": 15},
    ]


@pytest.fixture
def mock_ai_response():
    """Mock AI response for testing."""
    return AIMessage(content="Here are our available sweets!")


@pytest.fixture
def mock_tool_response():
    """Mock AI response with tool call."""
    return AIMessage(
        content="",
        tool_calls=[{"name": "get_available_sweets", "args": {}, "id": "call_123"}],
    )
