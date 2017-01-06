import urllib2
import re
from bs4 import BeautifulSoup
from arbiter import Arbiter
from arbiter import InvalidArbiterException


BASE_URL = u'https://ratings.fide.com'


class Tournament(object):
    def __init__(self, link):
        self.link = link
        self._extract_data()

    def _extract_data(self):
        sock = urllib2.urlopen(BASE_URL + self.link)
        soup = BeautifulSoup(sock.read(), "html.parser")
        temp = []
        # Extract general data
        tdata = soup.find_all('tr', bgcolor='#efefef')
        arb = False
        arbiter_objects = []
        for tr in tdata:
            for item in tr.find_all('td'):
                text = item.text.strip()
                if arb:
                    arbiter_url_re = re.compile('^https://ratings.fide.com/card.phtml?')
                    arbiter_links = item.find_all('a', href=arbiter_url_re)
                    for arbiter_link in arbiter_links:
                        print('Importing arbiter data...')
                        try:
                            arbiter = Arbiter(arbiter_link.get('href'))
                        except InvalidArbiterException:
                            print('Information not available for %s' % arbiter_link.text, arbiter_link.get('href'))
                            continue

                        arbiter_objects.append(arbiter)

                    arb = False

                if 'arbiter'in text.lower():
                    arb = True
                temp.append(text)

        i = iter(temp)
        data = dict(zip(i, i))
        data['arbiter_objects'] = arbiter_objects

        for num, arbiter in enumerate(data['arbiter_objects'], 1):
            for key in arbiter.data.keys():
                if key.isdigit():
                    arb_code = key
                    arb_name = arbiter.data[key]
                    data['arbiter%d_code' % num] = arb_code
                    data['arbiter%d_name' % num] = arb_name

        self.data = data
