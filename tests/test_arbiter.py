from fideparser.arbiter import Arbiter

import unittest


class TestArbiter(unittest.TestCase):
    def test_arbiter_data(self):
        r = Arbiter("https://ratings.fide.com/card.phtml?event=22232540")
        self.assertIn("FIDE title", r.data)
