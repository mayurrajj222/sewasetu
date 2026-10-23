import unittest
import time
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app"))

from app import send_sms

class TestPerformanceSMSNonblocking(unittest.TestCase):
    def test_send_sms_does_not_block_submission_worker(self):
        """SMS delivery to the gateway should not block the main request execution thread."""
        def slow_post(*args, **kwargs):
            time.sleep(1.5)  # Simulate carrier / gateway latency
            return None

        with patch("requests.post", side_effect=slow_post):
            start = time.time()
            send_sms("9876543210", "Test OTP")
            duration = time.time() - start
            
            # If asynchronous / background thread, duration will be < 0.3s
            # If synchronous, duration will be >= 1.5s and fail
            self.assertLess(duration, 0.5,
                            f"send_sms blocked the worker thread for {duration:.2f}s! This causes 504 timeouts under load.")

if __name__ == "__main__":
    unittest.main()
