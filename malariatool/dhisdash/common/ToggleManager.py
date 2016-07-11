class Toggle(object):

    def __init__(self, identifier, default, options):
        self.identifier = identifier
        self.default = default
        self.options = options


class ToggleManager(object):
    def __init__(self):
        self.toggles = {}

    def add(self, identifier, default, options):
        self.toggles[identifier] = {
            'main_toggle': default,
            'options': options
        }

    def find(self, identifier):
        if identifier in self.toggles:
            return self.toggles[identifier]['options']

    def exists(self, identifier):
        return identifier in self.toggles and len(self.find(identifier)) > 0

    def get_default(self, identifier):
        if identifier in self.toggles:
            return self.toggles[identifier]['main_toggle']

    def get_dict(self):
        return self.toggles
