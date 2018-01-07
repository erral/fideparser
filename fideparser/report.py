from bs4 import BeautifulSoup

import urllib2


class InvalidReportException(Exception):
    pass


class Report(object):
    """ Extract data from the tournament report"""
    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        sock = urllib2.urlopen(self.link)
        soup = BeautifulSoup(sock.read(), "html.parser")
        table = soup.find('table', class_=None)

        odds = table.find('tr', bgcolor='#e2e2e2')
        even = table.find('tr', bgcolor='#ffffff')

        self.data = {'player_count_in_report': str(len(odds) + len(even))}
        