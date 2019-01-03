# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from fideparser.arbiter import Arbiter
from fideparser.arbiter import InvalidArbiterException
from fideparser.report import InvalidReportException
from fideparser.report import Report

import re

from six.moves import urllib


BASE_URL = u"https://ratings.fide.com"


class Tournament(object):
    def __init__(self, link, extract_arbiter_data=True, extract_report_data=False):
        self.link = link
        self.extract_arbiter_data = extract_arbiter_data
        self.extract_report_data = extract_report_data
        self._extract_data()

    def _extract_data(self):
        sock = urllib.request.urlopen(BASE_URL + self.link)
        soup = BeautifulSoup(sock.read(), "html.parser")
        temp = []
        # Extract general data
        tdata = soup.find_all("tr", bgcolor="#efefef")
        arb = False
        reports = False
        arbiter_objects = []
        report_objects = []
        for tr in tdata:
            for item in tr.find_all("td"):
                text = item.text.strip()
                if self.extract_arbiter_data and arb:
                    arbiter_url_re = re.compile("^https://ratings.fide.com/card.phtml?")
                    arbiter_links = item.find_all("a", href=arbiter_url_re)
                    for arbiter_link in arbiter_links:
                        print("Importing arbiter data...")
                        try:
                            arbiter = Arbiter(arbiter_link.get("href"))
                        except InvalidArbiterException:
                            print(
                                "Information not available for %s" % arbiter_link.text,
                                arbiter_link.get("href"),
                            )
                            continue

                        arbiter_objects.append(arbiter)

                    arb = False

                if self.extract_report_data and reports:
                    report_url_re = re.compile("^tournament_report.phtml?")
                    report_links = item.find_all("a", href=report_url_re)
                    for report_link in report_links[:1]:
                        print("Importing report data...")
                        try:
                            full_link = "https://ratings.fide.com/" + report_link.get(
                                "href"
                            )
                            report = Report(full_link)
                        except InvalidReportException:
                            print(
                                "Information not available for %s"
                                % report_link.get("href")
                            )
                            continue

                        report_objects.append(report)

                    reports = False

                if "arbiter" in text.lower():
                    arb = True

                if "view report" in text.lower():
                    reports = True
                temp.append(text)

        i = iter(temp)
        data = dict(zip(i, i))
        data["arbiter_objects"] = arbiter_objects
        for report in report_objects:
            for k, v in report.data.items():
                data[k] = v

        for num, arbiter in enumerate(data["arbiter_objects"], 1):
            for key in arbiter.data.keys():
                if key.isdigit():
                    arb_code = key
                    arb_name = arbiter.data[key]
                    data["arbiter%d_code" % num] = arb_code
                    data["arbiter%d_name" % num] = arb_name

        self.data = data
