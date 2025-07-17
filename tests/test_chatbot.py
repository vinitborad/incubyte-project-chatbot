"""
Simple unit tests for chatbot.py module.
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from chatbot import AgentState, call_model, should_continue, graph


class TestAgentGraph:
    """Basic tests for the agent graph."""

    def test_graph_compiles_successfully(self):
        """Test that the graph compiles without errors."""
        # Act & Assert
        assert graph is not None
        assert hasattr(graph, "invoke")

    @patch("chatbot.llm_with_tools")
    def test_call_model_adds_system_prompt(self, mock_llm):
        """Test that call_model adds system prompt when not present."""
        # Arrange
        mock_response = AIMessage(content="Hello! How can I help?")
        mock_llm.invoke.return_value = mock_response

        state = AgentState(messages=[HumanMessage(content="Hello")])

        # Act
        result = call_model(state)

        # Assert
        assert len(result["messages"]) == 1
        assert result["messages"][0] == mock_response

        # Verify system prompt was added to the call
        called_messages = mock_llm.invoke.call_args[0][0]
        assert len(called_messages) == 2
        assert isinstance(called_messages[0], SystemMessage)

    def test_should_continue_with_tool_calls(self):
        """Test should_continue returns 'call_tool' when AI has tool calls."""
        # Arrange
        ai_message = AIMessage(
            content="Let me check our sweets.",
            tool_calls=[{"name": "get_available_sweets", "args": {}, "id": "call_123"}],
        )
        state = AgentState(messages=[ai_message])

        # Act
        result = should_continue(state)

        # Assert
        assert result == "call_tool"

    def test_should_continue_without_tool_calls(self):
        """Test should_continue returns 'end' when no tool calls."""
        # Arrange
        ai_message = AIMessage(content="Here are our sweets!")
        state = AgentState(messages=[ai_message])

        # Act
        result = should_continue(state)

        # Assert
        assert result == "end"


class TestAgentWithHistory:
    """Basic tests for agent with chat history."""

    @patch("chatbot.RedisChatMessageHistory")
    @patch("chatbot.graph")
    def test_agent_with_history_basic_flow(self, mock_graph, mock_redis):
        """Test basic agent with history functionality."""
        # Arrange
        from chatbot import get_agent_with_history

        mock_history = Mock()
        mock_history.messages = []
        mock_redis.return_value = mock_history

        mock_graph.invoke.return_value = {"messages": [AIMessage(content="Response")]}

        # Act
        agent = get_agent_with_history("test_session")
        result = agent("Hello")

        # Assert
        assert isinstance(result, AIMessage)
        assert result.content == "Response"
        assert mock_history.add_message.call_count == 2  # User + AI message
