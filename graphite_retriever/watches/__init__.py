from .parser import build_trigger



class Watch(object):
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.sources = kwargs.get('sources', [])
        self.triggers = kwargs.get('triggers', [])
