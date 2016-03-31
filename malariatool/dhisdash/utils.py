import requests
from malariatool.local_settings import DHIS2_USER, DHIS2_PASS


def dhis2_request(resource):
    url = 'http://hmis2.health.go.ug/hmis2/api/%s' % resource
    result = requests.get(url, auth=(DHIS2_USER, DHIS2_PASS))
    return result.json()