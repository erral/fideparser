from .utils import get_path_to_store_export_files
from .utils import get_test_file_contents
from fideparser.main import main
from fideparser.main import parse_args

import os
import re
import responses
import sys
import unittest


try:
    # python 3.4+ should use builtin unittest.mock not mock package
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestMain(unittest.TestCase):
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

    def tearDown(self):
        filenames = ["myjson.csv", "myjson.json", "myjson.binary"]
        for filename in filenames:
            file_path = get_path_to_store_export_files(filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_arguments_csv(self):
        arguments = parse_args(["ESP", "2018-01-01", "2018-01-01.csv", "csv"])
        self.assertEqual(arguments.country, "ESP")
        self.assertEqual(arguments.period, "2018-01-01")
        self.assertEqual(arguments.output_file, "2018-01-01.csv")
        self.assertEqual(arguments.export_format, "csv")

    def test_arguments_importfile(self):
        arguments = parse_args(
            [
                "ESP",
                "2018-01-01",
                "2018-01-01.csv",
                "csv",
                "--datafile=2018-01-01.binary",
            ]
        )
        self.assertEqual(arguments.datafile, "2018-01-01.binary")

    def test_arguments_arbiter_data(self):
        arguments = parse_args(
            ["ESP", "2018-01-01", "2018-01-01.csv", "csv", "--arbiter-data"]
        )
        self.assertTrue(arguments.arbiter_data)

    def test_arguments_report_data(self):
        arguments = parse_args(
            ["ESP", "2018-01-01", "2018-01-01.csv", "csv", "--report-data"]
        )
        self.assertTrue(arguments.report_data)

    @responses.activate
    def test_main_csv_export(self):
        filename = "myjson.csv"
        export_path = get_path_to_store_export_files(filename)
        testargs = ["export_fide_tournaments", "ESP", "2018-01-01", export_path, "csv"]
        with patch.object(sys, "argv", testargs):
            main()
            self.assertTrue(os.path.exists(export_path))

    @responses.activate
    def test_main_json_export(self):
        filename = "myjson.json"
        export_path = get_path_to_store_export_files(filename)
        testargs = ["export_fide_tournaments", "ESP", "2018-01-01", export_path, "json"]
        with patch.object(sys, "argv", testargs):
            main()
            self.assertTrue(os.path.exists(export_path))

    @responses.activate
    def test_main_binary_export(self):
        filename = "myjson.binary"
        export_path = get_path_to_store_export_files(filename)
        testargs = [
            "export_fide_tournaments",
            "ESP",
            "2018-01-01",
            export_path,
            "binary",
        ]
        with patch.object(sys, "argv", testargs):
            main()
            self.assertTrue(os.path.exists(export_path))

    @responses.activate
    def test_main_binary_import(self):
        filename = "myjson.binary"
        export_path = get_path_to_store_export_files(filename)
        testargs = [
            "export_fide_tournaments",
            "ESP",
            "2018-01-01",
            export_path,
            "binary",
        ]
        with patch.object(sys, "argv", testargs):
            main()
            self.assertTrue(os.path.exists(export_path))

        filename_json = "myjson.json"
        export_path_json = get_path_to_store_export_files(filename_json)
        testargs = [
            "export_fide_tournaments",
            "--datafile={}".format(export_path),
            "ESP",
            "2018-01-01",
            export_path_json,
            "json",
        ]
        with patch.object(sys, "argv", testargs):
            main()
            self.assertTrue(os.path.exists(export_path_json))
