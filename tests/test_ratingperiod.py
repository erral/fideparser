from .utils import get_test_file_contents
from fideparser.ratingperiod import RatingPeriod

import responses
import unittest


class TestArbiter(unittest.TestCase):
    @responses.activate
    def test_ratingperiod_data(self):
        ratingperiod_url = "https://ratings.fide.com/tournament_list.phtml?country=ESP&moder=ev_code&rating_period=2018-07-01"
        contents = get_test_file_contents("ratingperiod.html")
        responses.add(responses.GET, ratingperiod_url, body=contents)

        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()

        self.assertIsInstance(r.tournaments, list)
        self.assertEqual(len(r.tournaments), 86)