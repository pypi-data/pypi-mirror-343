"""
Tests for the GibGram client module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from tgrab.client import GibGramClient

class TestGibGramClient(unittest.TestCase):
    """Tests for the GibGramClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = GibGramClient(
            api_id=123456,
            api_hash="test_hash",
            phone="+1234567890",
            session_name="test_session",
            download_folder="test_downloads"
        )

    def test_init(self):
        """Test client initialization."""
        self.assertEqual(self.client.api_id, 123456)
        self.assertEqual(self.client.api_hash, "test_hash")
        self.assertEqual(self.client.phone, "+1234567890")
        self.assertEqual(self.client.session_name, "test_session")
        self.assertEqual(self.client.download_folder, "test_downloads")
        self.assertTrue(os.path.exists("test_downloads"))

    @patch("telethon.TelegramClient")
    async def test_connect(self, mock_client):
        """Test connecting to Telegram."""
        # Mock the client
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        # Test connection
        result = await self.client.connect()

        # Verify
        self.assertTrue(result)
        mock_instance.start.assert_called_once_with(phone="+1234567890")

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("test_downloads"):
            os.rmdir("test_downloads")

if __name__ == "__main__":
    unittest.main()
