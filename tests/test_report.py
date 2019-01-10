from .utils import get_test_file_contents
from fideparser.report import Report

import re
import responses
import unittest


class TestReport(unittest.TestCase):
    def setUp(self):
        report_url = re.compile(
            "https:\/\/ratings\.fide\.com\/tournament_report\.phtml\?event16=[\d]+"
        )

        contents = get_test_file_contents("report.html")
        responses.add(responses.GET, report_url, body=contents)

    @responses.activate
    def test_report_creation(self):
        tournament_url = (
            "https://ratings.fide.com/tournament_report.phtml?event16=179955"
        )

        r = Report(tournament_url)
        self.assertIn("player_count_in_report", r.data)
