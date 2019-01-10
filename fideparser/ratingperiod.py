# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from fideparser.exceptions import InvalideFileFormat
from fideparser.jsonencdec import FIDEJSONEncoder
from fideparser.tournament import Tournament
from io import BytesIO

import unicodecsv as csv
import json
import pickle
import re
import requests


BASE_URL = "https://ratings.fide.com/tournament_list.phtml?moder=ev_code&country=%(country)s&rating_period=%(period)s"


class RatingPeriod(object):
    def __init__(self, country, period, arbiters_data=True, report_data=True):
        self.country = country
        self.period = period
        self.arbiters_data = arbiters_data
        self.report_data = report_data
        self.tournaments = []
        self.fieldnames = set([])

    def __eq__(self, other):
        fields_equal = self.fieldnames == other.fieldnames
        tournaments_equal = False

        for tournament in self.tournaments:
            tournaments_equal = tournament in other.tournaments
            if not tournaments_equal:
                return False

        for tournament in other.tournaments:
            tournaments_equal = tournament in self.tournaments
            if not tournaments_equal:
                return False

        return fields_equal and tournaments_equal

    def save(self):
        """ import the data from FIDE site """
        url = BASE_URL % {"country": self.country, "period": self.period}
        print("Getting period data...")
        sock = requests.get(url)
        soup = BeautifulSoup(sock.content, "html.parser")
        tournament_link_re = re.compile("^/tournament_details?")
        tournament_links = soup.find_all("a", href=tournament_link_re)
        for i, link in enumerate(tournament_links, 1):
            print("Importing tournament %s of %s" % (i, len(tournament_links)))
            tournament = Tournament(
                link.get("href"), self.arbiters_data, self.report_data
            )
            self.tournaments.append(tournament)
            self.fieldnames = self.fieldnames.union(set(tournament.data.keys()))
            print("Tournament done")

    def load_from_file(self, filepath):
        fp = open(filepath, "r")
        data = pickle.load(fp)
        if not isinstance(data, RatingPeriod):
            raise InvalideFileFormat

        self.country = data.country
        self.period = data.period
        self.tournaments = data.tournaments
        for tournament in self.tournaments:
            self.fieldnames = self.fieldnames.union(tournament.data.keys())

    def export(self, filename, format="binary"):
        """ return the saved data in a structured way """
        if format == "binary":
            self.export_binary(filename)
        elif format == "json":
            self.export_json(filename)
        elif format == "csv":
            self.export_csv(filename)

    def export_binary(self, filename):
        fp = open(filename, "wb")
        pickle.dump(self, fp)
        fp.close()

    def export_json(self, filename):
        fp = open(filename, "wb")
        json.dump(self.tournaments, fp, cls=FIDEJSONEncoder)
        fp.close()

    def export_csv(self, filename):
        # If we export data to JSON and reimport without the
        # special data format for Arbiters, we can easily
        # create a big dict to export it to a CSV file
        json_data = json.dumps(self.tournaments, cls=FIDEJSONEncoder)
        data = json.loads(json_data)
        keys = list(self.fieldnames)
        # Manually add arbiter code and name headers
        # Because some lines don't have them
        # because they have just 1 or 2 arbiters and others 4
        for i in range(1, 10):
            keys.append("arbiter%d_code" % i)
            keys.append("arbiter%d_name" % i)
        keys = set(keys)
        if "arbiter_objects" in keys:
            keys.remove("arbiter_objects")
        keys = list(keys)
        keys.sort()
        fp = open(filename, "wb")
        writer = csv.DictWriter(fp, keys, encoding="utf-8")
        writer.writeheader()
        writer.writerows(data)
        fp.close()
