import json
import unittest
from unittest.mock import mock_open, patch

from newsfeed.send_summaries_to_discord import (  # Replace `your_module` with the actual module name
    hash_summary,
    read_sent_log,
    truncate_string,
    write_sent_log,
)


class TestYourModule(unittest.TestCase):
    def test_truncate_string(self):
        self.assertEqual(truncate_string("1234567890", 5), "12...")

    def test_hash_summary(self):
        self.assertIsInstance(hash_summary({"key": "value"}), str)  # Just checking the type

    @patch("builtins.open", new_callable=mock_open, read_data='["hash1", "hash2"]')
    def test_read_sent_log(self, mock_file):
        sent_log = read_sent_log()
        self.assertEqual(sent_log, ["hash1", "hash2"])

    @patch("builtins.open", new_callable=mock_open)
    def test_write_sent_log(self, mock_file):
        write_sent_log(["hash1", "hash2"])
        mock_file().write.assert_called_once_with('["hash1", "hash2"]')


if __name__ == "__main__":
    unittest.main()
