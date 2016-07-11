class Table(object):
    def __init__(self, toggle, identifier, ng_repeat, labels, sources):
        self.toggle = toggle
        self.identifier = identifier
        self.ng_repeat = ng_repeat
        self.labels = labels
        self.sources = sources


class ContentAreaManager(object):

    def __init__(self):
        self.tables = {}

    def add(self, toggle, identifier, ng_repeat, labels, sources):
        self.tables[identifier] = Table(toggle, identifier, ng_repeat, labels, sources)

    def all(self):
        return self.tables.values()
