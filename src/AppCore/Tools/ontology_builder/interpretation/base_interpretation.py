import json


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: dict({**super(o.__class__, o).__dict__}), sort_keys=True, indent=4)


class BaseImplementation(Object):
    def __init__(self, cls):
        self.system_name = cls.__name__
        self.words = []
