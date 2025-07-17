"""
Simple unit tests for tools.py module.
"""

import pytest
import responses
from unittest.mock import patch
from tools import buy_sweet, get_available_sweets


class TestBuySweet:
    """Basic tests for buy_sweet tool."""

    @responses.activate
    def test_buy_sweet_success(self):
        """Test successful sweet purchase."""
        # Arrange
        responses.add(
            responses.GET,
            "http://localhost:5000/search",
            json=[{"_id": "sweet1", "name": "Gulab Jamun"}],
            status=200,
        )
        responses.add(
            responses.POST,
            "http://localhost:5000/purchase/sweet1",
            json={"message": "Purchase successful"},
            status=200,
        )

        # Act
        result = buy_sweet.invoke({"sweet_name": "Gulab Jamun", "quantity": 2})

        # Assert
        assert result == "Successfully purchased 2 of Gulab Jamun."

    @responses.activate
    def test_buy_sweet_not_found(self):
        """Test purchase when sweet is not found."""
        # Arrange
        responses.add(
            responses.GET, "http://localhost:5000/search", json=[], status=200
        )

        # Act
        result = buy_sweet.invoke({"sweet_name": "Nonexistent Sweet", "quantity": 1})

        # Assert
        assert "Could not find a sweet named 'Nonexistent Sweet'" in result


class TestGetAvailableSweets:
    """Basic tests for get_available_sweets tool."""

    @patch("tools.get_all_sweets")
    def test_get_available_sweets_success(
        self, mock_get_all_sweets, sample_sweets_data
    ):
        """Test successful retrieval of available sweets."""
        # Arrange
        mock_get_all_sweets.return_value = sample_sweets_data

        # Act
        result = get_available_sweets.invoke({})

        # Assert
        assert "Here are the sweets currently available:" in result
        assert "Gulab Jamun: ₹25.50" in result
        assert "Rasgulla: ₹20.00" in result

    @patch("tools.get_all_sweets")
    def test_get_available_sweets_empty_inventory(self, mock_get_all_sweets):
        """Test retrieval when inventory is empty."""
        # Arrange
        mock_get_all_sweets.return_value = []

        # Act
        result = get_available_sweets.invoke({})

        # Assert
        assert result == "No sweets are currently available in our inventory."
