from dhisdash.models import DataValue, Facility, Region, District, SubCounty, DataElement, DataSet, \
    CategoryOptionCombo, AgeGroups


class MyTestHelper(object):
    @staticmethod
    def create_region(identifier='xx', name='central'):
        r = Region()
        r.identifier = identifier
        r.name = name
        r.save()
        return r

    @staticmethod
    def create_district(region, identifier='yy', name='kampala', population=0):
        d = District()
        d.identifier = identifier
        d.name = name
        d.region = region
        d.population = population
        d.save()
        return d

    @staticmethod
    def create_sub_county(district, identifier='zz', name='nansana'):
        s = SubCounty()
        s.identifier = identifier
        s.name = name
        s.district = district
        s.save()
        return s

    def create_facility(self, sub_county, identifier='aa', name='Sample Facility'):
        f = Facility()
        f.identifier = identifier
        f.name = name
        f.sub_county = sub_county
        f.save()
        return f

    def create_test_data(self):
        r = self.create_region()
        d = self.create_district(r)
        s = self.create_sub_county(d)
        f = self.create_facility(s)

        return {'facility': f, 'sub_county': s, 'district': d, 'region': r}

    @staticmethod
    def create_sample_data_element(identifier='xx', name='sample element', data_set_identifier='yy'):
        de = DataElement()
        de.identifier = identifier
        de.data_set_identifier = data_set_identifier
        de.name = name
        de.save()
        return de

    def create_sample_data_set(self):
        ds = DataSet()
        ds.identifier = 'xx'
        ds.period_type = 'monthly'
        ds.name = 'sample data set'
        ds.save()
        return ds

    def create_sample_category_option(self, de, identifier='xx', name='sample combo'):
        co = CategoryOptionCombo()
        co.name = name
        co.identifier = identifier
        co.data_element = de
        co.save()
        return co

    def create_data_value(self, data, de, co, ds, period, value, age_group=0):
        dv = DataValue()
        dv.region = data['region']
        dv.district = data['district']
        dv.facility = data['facility']
        dv.data_element = de
        dv.category_option_combo = co
        dv.data_set = ds
        dv.period = period
        dv.age_group = age_group
        dv.value = value
        dv.original_period = period
        dv.save()
