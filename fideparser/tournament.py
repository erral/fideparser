import urllib2
import re
from bs4 import BeautifulSoup
from arbiter import Arbiter

BASE_URL = u'http://ratings.fide.com'

class Tournament(object):
    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        sock = urllib2.urlopen(BASE_URL + self.link)
        soup = BeautifulSoup(sock.read())
        temp = []
        # Extract general data
        tdata = soup.find_all('tr', bgcolor='#efefef')
        for tr in tdata:
            for item in tr.find_all('td'):
                temp.append(item.text.strip())

        i = iter(temp)
        data = dict(zip(i, i))

        # Extract arbiter data
        arbiter_url_re = re.compile('^http://ratings.fide.com/card.phtml?')
        arbiter_links = soup.find_all('a', href=arbiter_url_re)
        data['arbiter_objects'] = []
        for arbiter_link in arbiter_links:
            arbiter = Arbiter(arbiter_link.get('href'))
            data['arbiter_objects'].append(arbiter)

        self.data = data