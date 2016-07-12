from dhisdash.models import DataElement, CategoryOptionCombo


def generate_dict(objects):
    result = {}
    for o in objects:
        result[o.name] = o.identifier
    return result


class IdentifierManager(object):

    def __init__(self):
        self.data_elements = {}
        self.category_option_combos = {}

        self.load_identifiers()

    def load_identifiers(self):
        self.data_elements = generate_dict(DataElement.objects.all())
        self.category_option_combos = generate_dict(CategoryOptionCombo.objects.all())

    def de(self, identifier):
        if identifier not in self.data_elements:
            raise Exception("DATA ELEMENT NOT FOUND")
        return self.data_elements[identifier]

    def coc(self, identifier):
        if identifier not in self.category_option_combos:
            raise Exception("CATEGORY OPTION COMBO NOT FOUND")
        return self.category_option_combos[identifier]