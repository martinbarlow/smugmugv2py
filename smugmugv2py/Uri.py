class Uri(object):
    def __init__(self, uri):
        for key in uri:
            setattr(self, key.lower(), uri[key])
