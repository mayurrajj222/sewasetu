import unittest
from datetime import datetime, date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))

from app import app

class TestFormValidation(unittest.TestCase):
    def test_indian_date_parsing_priority(self):
        """Test that DD/MM/YYYY is parsed correctly and not swapped to MM/DD/YYYY."""
        # Date: 05/08/1950 (5th August 1950)
        # Under US parsing %m/%d/%Y, it erroneously becomes May 8th, 1950
        dob_raw = "05/08/1950"
        
        # Test how the app parses this date
        from app import parse_dob  # We will define parse_dob helper in app.py
        parsed = parse_dob(dob_raw)
        self.assertEqual(parsed, date(1950, 8, 5),
                         f"05/08/1950 was parsed as month {parsed.month} instead of August (8)!")

    def test_iso_date_parsing(self):
        """Standard HTML5 date input format (YYYY-MM-DD) must be parsed successfully."""
        from app import parse_dob
        parsed = parse_dob("1950-08-05")
        self.assertEqual(parsed, date(1950, 8, 5))

    def test_widow_husband_employer_not_required(self):
        """A widowed citizen must not be blocked for leaving husband employer empty."""
        from app import validate_submission_data
        data = {
            "applicant_name": "Runu Dutta",
            "village": "Milanpur",
            "block": "Borgaon",
            "gender": "Female",
            "marital_status": "Widowed",
            "husband_name": "Late Biren Dutta",
            "husband_employer": "",  # Deceased spouse has no employer
            "bank_account": "3921227103603",
            "ifsc": "CNRB0004417",
            "dob": "20/05/1961"
        }
        is_valid, err_msg = validate_submission_data(data)
        self.assertTrue(is_valid, f"Widow without husband employer was rejected: {err_msg}")

if __name__ == "__main__":
    unittest.main()
