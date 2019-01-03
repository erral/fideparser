# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import requests


class InvalidReportException(Exception):
    pass


class Report(object):
    """ Extract data from the tournament report"""

    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        sock = requests.get(self.link)
        soup = BeautifulSoup(sock.content, "html.parser")
        table = soup.find("table", class_=None)

        odds = table.findAll("tr", bgcolor="#e2e2e2")
        even = table.findAll("tr", bgcolor="#ffffff")

        self.data = {"player_count_in_report": str(len(odds) + len(even))}
