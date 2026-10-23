import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))

from app import app

class TestSecurityAccessControl(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_unauthenticated_ack_pdf_blocked(self):
        """Unauthenticated requests to /ack/<app_id>.pdf must require authentication."""
        # When unauthenticated, /ack/1.pdf must NOT attempt to serve or leak data
        response = self.client.get("/ack/1.pdf")
        # Must redirect to login (302) or return 401/403
        self.assertIn(response.status_code, [302, 401, 403],
                      f"Unauthenticated request to /ack/1.pdf was not blocked! Status: {response.status_code}")

    def test_citizen_cannot_approve_application(self):
        """A regular citizen (logged_in=True but admin=False) must receive 403 Forbidden on admin actions."""
        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["portal_mobile"] = "9876543210"
            # Explicitly not an admin

        # If security check is fixed, it must abort(403) BEFORE database access
        response = self.client.post("/admin/approve/1")
        self.assertEqual(response.status_code, 403,
                         f"Citizen without admin rights was permitted to approve applications! Status: {response.status_code}")

if __name__ == "__main__":
    unittest.main()
