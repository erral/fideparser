from .utils import get_path_to_store_export_files
from .utils import get_test_file_contents
from fideparser.ratingperiod import RatingPeriod

import os
import re
import responses
import unittest


class TestArbiter(unittest.TestCase):
    def setUp(self):
        ratingperiod_url = re.compile(
            "https:\/\/ratings\.fide\.com\/tournament_list\.phtml\?moder=ev_code&country=[A-Z]+&rating_period=[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-01"
        )
        contents = get_test_file_contents("ratingperiod.html")
        responses.add(responses.GET, ratingperiod_url, body=contents)

        tournament_url = re.compile(
            "https:\/\/ratings\.fide\.com\/tournament_details\.phtml\?event=[\d]+"
        )
        tournament_contents = get_test_file_contents("tournament.html")
        responses.add(responses.GET, tournament_url, body=tournament_contents)

    @responses.activate
    def test_ratingperiod_data(self):
        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()

        self.assertIsInstance(r.tournaments, list)
        self.assertEqual(len(r.tournaments), 86)

    @responses.activate
    def test_ratingperiod_export_json(self):
        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()
        filename = "myjson.json"
        export_path = get_path_to_store_export_files(filename)
        r.export(export_path, "json")

        dir_path = os.path.dirname(export_path)
        self.assertIn(filename, os.listdir(dir_path))

    @responses.activate
    def test_ratingperiod_export_csv(self):
        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()
        filename = "myjson.csv"
        export_path = get_path_to_store_export_files(filename)
        r.export(export_path, "csv")

        dir_path = os.path.dirname(export_path)
        self.assertIn(filename, os.listdir(dir_path))

    @responses.activate
    def test_ratingperiod_export_binary(self):
        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()
        filename = "myjson.binary"
        export_path = get_path_to_store_export_files(filename)
        r.export(export_path, "binary")

        dir_path = os.path.dirname(export_path)
        self.assertIn(filename, os.listdir(dir_path))

    @responses.activate
    def test_ratingperiod_import_binary(self):
        """Check that exported binary can be imported """
        r = RatingPeriod("ESP", "2018-07-01", arbiters_data=False, report_data=False)
        r.save()
        filename = "myjson.binary"
        export_path = get_path_to_store_export_files(filename)
        r.export_binary(export_path)

        dir_path = os.path.dirname(export_path)
        self.assertIn(filename, os.listdir(dir_path))

        r_imported = RatingPeriod("ESP", "2018-07-01")
        r_imported.load_from_file(export_path)

        self.assertEquals(r, r_imported)
