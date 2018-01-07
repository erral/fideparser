from .arbiter import Arbiter
from .report import Report
from .tournament import Tournament
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
