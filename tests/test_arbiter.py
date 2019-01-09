from .utils import get_test_file_contents
from fideparser.arbiter import Arbiter

import responses
import unittest


class TestArbiter(unittest.TestCase):
    @responses.activate
    def test_arbiter_data(self):
        arbiter_url = "https://ratings.fide.com/card.phtml?event=22232540"
        contents = get_test_file_contents("arbiter.html")
        responses.add(responses.GET, arbiter_url, body=contents)

        r = Arbiter(arbiter_url)
        self.assertIn("FIDE title", r.data)
