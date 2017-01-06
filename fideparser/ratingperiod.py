from bs4 import BeautifulSoup
from dictunicodewriter import DictUnicodeWriter
from exceptions import InvalideFileFormat
from jsonencdec import FIDEJSONEncoder
from tournament import Tournament
import json
import pickle
import re
import urllib2


BASE_URL = 'https://ratings.fide.com/tournament_list.phtml?moder=ev_code&country=%(country)s&rating_period=%(period)s'


class RatingPeriod(object):
    def __init__(self, country, period):
        self.country = country
        self.period = period
        self.tournaments = []
        self.fieldnames = set([])

    def save(self):
        """ import the data from FIDE site """
        url = BASE_URL % {'country': self.country, 'period': self.period}
        print 'Getting period data...'
        sock = urllib2.urlopen(url)
        soup = BeautifulSoup(sock.read(), "html.parser")
        tournament_link_re = re.compile('^/tournament_details?')
        tournament_links = soup.find_all('a', href=tournament_link_re,)
        i = 1
        for link in tournament_links:
            print 'Importing tournament %s of %s' % (i, len(tournament_links))
            tournament = Tournament(link.get('href'))
            self.tournaments.append(tournament)
            self.fieldnames = self.fieldnames.union(set(tournament.data.keys()))
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
        for tournament in self.tournaments:
            self.fieldnames = self.fieldnames.union(tournament.data.keys())

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
        # If we export data to JSON and reimport without the
        # special data format for Arbiters, we can easily
        # create a big dict to export it to a CSV file
        json_data = json.dumps(self.tournaments, cls=FIDEJSONEncoder)
        data = json.loads(json_data)
        keys = list(self.fieldnames)
        # Manually add arbiter code and name headers
        # Because some lines don't have them
        # because they have just 1 or 2 arbiters and others 4
        for i in range(1, 10):
            keys.append('arbiter%d_code' % i)
            keys.append('arbiter%d_name' % i)
        keys = set(keys)
        keys.remove('arbiter_objects')
        fp = open(filename, 'w')
        writer = DictUnicodeWriter(fp, keys)
        writer.writeheader()
        writer.writerows(data)
        fp.close()
