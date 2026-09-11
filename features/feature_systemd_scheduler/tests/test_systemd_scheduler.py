"""
Unit Test Suite for Systemd Scheduler (Git Branch: feature/systemd-scheduler)
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
from features.feature_systemd_scheduler.implementation.scheduler import (
    get_timer_status,
    install_systemd_timer,
)


class TestSystemdScheduler(unittest.TestCase):
    def test_get_timer_status_structure(self):
        status = get_timer_status()
        self.assertIn("installed", status)
        self.assertIn("active", status)
        self.assertIn("enabled", status)
        self.assertIn("detail", status)

    @patch("subprocess.run")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_install_systemd_timer_success(self, mock_file, mock_mkdir, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0)
        success = install_systemd_timer()
        self.assertTrue(success)
        self.assertEqual(mock_file.call_count, 2)
        self.assertEqual(mock_subprocess.call_count, 2)

    @patch("subprocess.run")
    @patch("pathlib.Path.mkdir")
    def test_install_systemd_timer_failure(self, mock_mkdir, mock_subprocess):
        mock_subprocess.side_effect = Exception("Systemd error")
        success = install_systemd_timer()
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
