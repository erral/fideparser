from bs4 import BeautifulSoup
import urllib2


class InvalidArbiterException(Exception):
    """ When the given arbiter data is not valid
        this exception is raised
    """


class Arbiter(object):
    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        sock = urllib2.urlopen(self.link)
        soup = BeautifulSoup(sock.read(), "html.parser")
        table = soup.find("table", class_="contentpaneopen")
        inner_table = table.find("table")
        if not inner_table:
            raise InvalidArbiterException

        data_table = inner_table.find("table")
        arbiter_data = {}
        for tr in data_table.find_all("tr"):
            items = []
            for td in tr.find_all("td"):
                items.append(td.text)
            if len(items) > 2:
                # The first row contains a td for the photo
                # so we have to ignore it
                items = items[1:]
            elif len(items) < 2:
                # Rows with just one celd are not interesting
                continue

            arbiter_data[self._clean(items[0])] = self._clean(items[1])

        self.data = arbiter_data

    def _clean(self, text):
        text = text.replace(u"\xa0", " ")
        text = text.strip()
        return text
