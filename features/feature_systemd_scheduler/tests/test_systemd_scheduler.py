"""
Unit Test Suite for Systemd Scheduler (Git Branch: feature/systemd-scheduler)
"""

import unittest
from features.feature_systemd_scheduler.implementation.scheduler import get_timer_status


class TestSystemdScheduler(unittest.TestCase):
    def test_get_timer_status_structure(self):
        status = get_timer_status()
        self.assertIn("installed", status)
        self.assertIn("active", status)
        self.assertIn("enabled", status)
        self.assertIn("detail", status)


if __name__ == "__main__":
    unittest.main()
