"""
Simple unit tests for database.py module.
"""

import pytest
from unittest.mock import patch
from database import get_all_sweets


class TestDatabase:
    """Basic tests for database operations."""

    @patch("database.sweets_collection")
    def test_get_all_sweets_success(self, mock_collection, sample_sweets_data):
        """Test successful retrieval of sweets from database."""
        # Arrange
        mock_collection.find.return_value = sample_sweets_data

        # Act
        result = get_all_sweets()

        # Assert
        assert len(result) == 2
        assert result[0]["name"] == "Gulab Jamun"
        assert result[1]["name"] == "Rasgulla"
        mock_collection.find.assert_called_once_with({}, {"_id": 0})

    @patch("database.sweets_collection")
    def test_get_all_sweets_empty_database(self, mock_collection):
        """Test retrieval when database is empty."""
        # Arrange
        mock_collection.find.return_value = []

        # Act
        result = get_all_sweets()

        # Assert
        assert result == []
