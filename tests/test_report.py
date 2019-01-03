from fideparser.report import Report

import unittest


class TestReport(unittest.TestCase):
    def test_report_creation(self):
        r = Report("https://ratings.fide.com/tournament_report.phtml?event16=179955")
        self.assertIn("player_count_in_report", r.data)
