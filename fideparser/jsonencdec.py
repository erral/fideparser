# -*- coding: utf-8 -*-
from fideparser.arbiter import Arbiter
from fideparser.report import Report
from fideparser.tournament import Tournament
from json import JSONEncoder


class FIDEJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Tournament):
            return o.data
        elif isinstance(o, Arbiter):
            return o.data
        elif isinstance(o, Report):
            return o.data
        else:
            return super(FIDEJSONEncoder, self).default(o)
