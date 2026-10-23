import os
import unittest
import configparser

class TestDeemedApproval(unittest.TestCase):
    def test_deemed_approval_config_load(self):
        """Test that deemed_approval script loads configuration from existing app.ini."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base_dir, "app", "scripts", "deemed_approval.py")
        
        with open(script_path, "r", encoding="utf-8") as f:
            script_code = f.read()

        # Check what config file the script tries to open
        self.assertNotIn("settings.ini", script_code,
                         "deemed_approval.py is still pointing to non-existent settings.ini!")
        
        # Verify that app.ini exists and has required sections
        app_ini_path = os.path.join(base_dir, "app", "config", "app.ini")
        self.assertTrue(os.path.exists(app_ini_path), "app.ini must exist")
        
        config = configparser.ConfigParser()
        with open(app_ini_path) as fh:
            config.read_file(fh)
        
        self.assertTrue(config.has_section("pension"))
        self.assertTrue(config.has_option("pension", "sla_days"))

if __name__ == "__main__":
    unittest.main()
