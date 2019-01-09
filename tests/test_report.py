from .utils import get_test_file_contents
from fideparser.report import Report

import responses
import unittest


class TestReport(unittest.TestCase):
    @responses.activate
    def test_report_creation(self):
        tournament_url = (
            "https://ratings.fide.com/tournament_report.phtml?event16=179955"
        )
        contents = get_test_file_contents("tournament.html")
        responses.add(responses.GET, tournament_url, body=contents)

        r = Report(tournament_url)
        self.assertIn("player_count_in_report", r.data)
