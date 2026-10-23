import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))

from app import sanitize

class TestIndicNamesAndSanitization(unittest.TestCase):
    def test_sanitize_preserves_indic_name(self):
        """Test that Indian language names (Assamese, Hindi, Bengali) are preserved and not sliced by bytes."""
        # A typical Assamese name
        assamese_name = "ৰঞ্জিত শৰ্মা"
        sanitized = sanitize(assamese_name)
        self.assertEqual(sanitized, assamese_name,
                         f"Sanitize corrupted the Assamese name: expected '{assamese_name}', got '{sanitized}'")

    def test_sanitize_long_indic_name(self):
        """Test that names longer than 20 bytes (common for Indic scripts) are not chopped in half."""
        # "কমলেশ কুমাৰ শৰ্মা" is ~50 bytes in UTF-8
        long_indic_name = "কমলেশ কুমাৰ শৰ্মা"
        sanitized = sanitize(long_indic_name)
        self.assertEqual(sanitized, long_indic_name,
                         f"Sanitize cut the Indic name in half: expected '{long_indic_name}', got '{sanitized}'")

if __name__ == "__main__":
    unittest.main()
