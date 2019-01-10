from .utils import get_test_file_contents
from fideparser.arbiter import Arbiter

import responses
import unittest
import re


class TestArbiter(unittest.TestCase):
    def setUp(self):
        arbiter_url = re.compile(
            "https:\/\/ratings\.fide\.com\/card\.phtml\?event=[\d]+"
        )
        arbiter_contents = get_test_file_contents("arbiter.html")
        responses.add(responses.GET, arbiter_url, body=arbiter_contents)

    @responses.activate
    def test_arbiter_data(self):
        arbiter_url = "https://ratings.fide.com/card.phtml?event=22232540"
        contents = get_test_file_contents("arbiter.html")
        responses.add(responses.GET, arbiter_url, body=contents)

        r = Arbiter(arbiter_url)
        self.assertIn("FIDE title", r.data)
