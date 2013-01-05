from bs4 import BeautifulSoup
import re
import urllib2
from tournament import Tournament

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


    def export(self, format='binary'):
        """ return the saved data in a structured way """
        pass