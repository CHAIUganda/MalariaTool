class Table(object):
    def __init__(self, toggle, identifier, unit, labels, sources):
        self.toggle = toggle
        self.identifier = identifier
        self.ng_repeat = self.get_ng_repeat()
        self.labels = labels
        self.sources = sources
        self.unit = unit

    def get_ng_repeat(self):
        # return "%s_data_table_results" % self.identifier.replace("-", "_")
        return "%s" % self.identifier.replace("-", "_")


class ContentAreaManager(object):

    def __init__(self):
        self.tables = {}

    def add(self, toggle, identifier, unit, labels, sources=None):
        if sources is None:
            sources = ['denominator', 'numerator', 'result']
        self.tables[identifier] = Table(toggle, identifier, unit, labels, sources)

    def all(self):
        return self.tables.values()
