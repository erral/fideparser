from tournament import Tournament
from arbiter import Arbiter
from json import JSONEncoder

class FIDEJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, Tournament):
            return o.data
        elif isinstance(o, Arbiter):
            return o.data
        else:
            return super(FIDEJSONEncoder, self).default(o)
