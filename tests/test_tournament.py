from .utils import get_test_file_contents
from fideparser.tournament import Tournament

import responses
import unittest
import re


class TestTournament(unittest.TestCase):
    def setUp(self):
        contents = get_test_file_contents("tournament.html")
        tournament_url = re.compile(
            "https:\/\/ratings\.fide\.com\/tournament_details\.phtml\?event=[\d]+"
        )
        responses.add(responses.GET, tournament_url, body=contents)

        arbiter_url = re.compile(
            "https:\/\/ratings\.fide\.com\/card\.phtml\?event=[\d]+"
        )
        arbiter_contents = get_test_file_contents("arbiter.html")
        responses.add(responses.GET, arbiter_url, body=arbiter_contents)

        report_url = re.compile(
            "https:\/\/ratings\.fide\.com\/tournament_report\.phtml\?event16=[\d]+"
        )
        report_contents = get_test_file_contents("report.html")
        responses.add(responses.GET, report_url, body=report_contents)

    @responses.activate
    def test_tournament(self):
        tournament_url_value = "/tournament_details.phtml?event=186590"

        r = Tournament(
            tournament_url_value, extract_arbiter_data=False, extract_report_data=False
        )
        self.assertIn("Tournament Name", r.data)
        self.assertTrue("arbiter1_name" not in r.data)
        self.assertTrue("player_count_in_report" not in r.data)

    @responses.activate
    def test_tournament_with_arbiter_data(self):
        tournament_url_value = "/tournament_details.phtml?event=186590"
        r = Tournament(tournament_url_value, extract_arbiter_data=True)
        self.assertIn("arbiter1_name", r.data)

    @responses.activate
    def test_tournament_with_report_data(self):
        tournament_url_value = "/tournament_details.phtml?event=186590"

        r = Tournament(tournament_url_value, extract_report_data=True)
        self.assertIn("player_count_in_report", r.data)
        self.assertGreater(r.data["player_count_in_report"], 0)
