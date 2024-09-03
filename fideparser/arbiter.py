# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import requests


class InvalidArbiterException(Exception):
    """When the given arbiter data is not valid
    this exception is raised
    """


class Arbiter(object):
    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        arbiter_data = {}
        sock = requests.get(self.link)
        soup = BeautifulSoup(sock.content, "html.parser")
        table = soup.find("div", class_="profile-top-info")
        if table is not None:

            headers = table.find_all(
                "div", class_="profile-top-info__block__row__header"
            )
            values = table.find_all("div", class_="profile-top-info__block__row__data")

            for header, value in zip(headers, values):
                arbiter_data[self._clean(header.text)] = self._clean(value.text)

        self.data = arbiter_data

    def _clean(self, text):
        text = text.replace("\xa0", " ")
        text = text.strip()
        return text
