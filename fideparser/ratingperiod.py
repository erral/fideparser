from bs4 import BeautifulSoup
import re
import urllib2
import pickle
import json
import csv
from dictunicodewriter import DictUnicodeWriter
from tournament import Tournament
from exceptions import InvalideFileFormat
from jsonencdec import FIDEJSONEncoder

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
        print 'Getting period data...'
        sock = urllib2.urlopen(url)
        soup = BeautifulSoup(sock.read())
        tournament_link_re = re.compile('^/tournament_details?')
        tournament_links = soup.find_all('a',
                                         href=tournament_link_re,
                                        )
        i = 1
        for link in tournament_links:
            print 'Importing tournament %s of %s' % (i, len(tournament_links))
            tournament = Tournament(link.get('href'))
            self.tournaments.append(tournament)
            print 'Tournament done'
            i = i + 1

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
            self.export_binary(filename)
        elif format == 'json':
            self.export_json(filename)
        elif format == 'csv':
            self.export_csv(filename)

    def export_binary(self, filename):
        fp = open(filename, 'w')
        pickle.dump(self, fp)
        fp.close()

    def export_json(self, filename):
        fp = open(filename, 'w')
        json.dump(self.tournaments,
                  fp,
                  cls=FIDEJSONEncoder)
        fp.close()

    def export_csv(self, filename):
        json_data = json.dumps(self.tournaments, cls=FIDEJSONEncoder)
        data = json.loads(json_data)
        fp = open(filename, 'w')
        writer = DictUnicodeWriter(fp,
                                   data[0].keys(),
                )
        writer.writeheader()
        writer.writerows(data)
        fp.close()
