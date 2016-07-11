class Tab(object):
    def __init__(self, identifier, name, title, ng_bind):
        self.identifier = identifier
        self.name = name
        self.title = title
        self.ng_bind = ng_bind


class TabManager(object):
    def __init__(self):
        self.tabs = {}
        self.default = None

    def add(self, identifier, name, title, ng_bind):
        self.tabs[identifier] = Tab(identifier, name, title, ng_bind)

    def all(self):
        return self.tabs.values()

    def set_default_tab(self, identifier):
        self.default = identifier
