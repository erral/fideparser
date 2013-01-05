from bs4 import BeautifulSoup
import re
import urllib2
import pickle
from tournament import Tournament
from exceptions import InvalideFileFormat

BASE_URL = 'http://ratings.fide.com/tournament_list.phtml?moder=ev_code&country=%(country)s&rating_period=%(period)s'

class RatingPeriod(object):
    def __init__(self, country, period):
        self.country = country
        self.period = period
        self.tournaments = []

    def save(self):
        """ import the data from FIDE site """
        url = BASE_URL % {'country': self.country,
                          'period': self.period,
        }
        sock = urllib2.urlopen(url)
        soup = BeautifulSoup(sock.read())
        tournament_link_re = re.compile('^/tournament_details?')
        tournament_links = soup.find_all('a',
                                         href=tournament_link_re,
                                        )
        for link in tournament_links:
            tournament = Tournament(link.get('href'))
            self.tournaments.append(tournament)

    def load_from_file(self, filepath):
        fp = open(filepath, 'r')
        data = pickle.load(fp)
        if not isinstance(data, RatingPeriod):
            raise InvalideFileFormat

        self.country = data.country
        self.period = data.period
        self.tournaments = data.tournaments


    def export(self, filename, format='binary'):
        """ return the saved data in a structured way """
        if format == 'binary':
            self.export_binary()
        elif format == 'json':
            self.export_json()
        elif format == 'csv':
            self.export_csv()

    def export_binary(self):
        pass

    def export_json(self):
        pass

    def export_csv(self):
        pass
