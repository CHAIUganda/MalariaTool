from datetime import date
import requests
from malariatool.local_settings import DHIS2_USER, DHIS2_PASS
from isoweek import Week
from malariatool.settings import BASE_DIR


def get_data_set_file_path(data_set, period):
    return "%s/dhisdash/downloads/data_set_%s_%s.json" % (BASE_DIR, data_set.identifier, period)


def dhis2_request(resource):
    url = 'http://hmis2.health.go.ug/hmis2/api/%s' % resource
    result = requests.get(url, auth=(DHIS2_USER, DHIS2_PASS))
    return result.json()


def dhis2_request_to_file(resource, file_name):
    url = 'http://hmis2.health.go.ug/hmis2/api/%s' % resource
    print 'Fetching [%s]' % url
    result = requests.get(url, auth=(DHIS2_USER, DHIS2_PASS), stream=True)

    with open(file_name, 'wb') as f:
        for chunk in result.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def month_to_weeks(year, month):
    max_weeks = date(year, 12, 28).isocalendar()[1]  # Last week in year
    matched_weeks = []

    for week in range(max_weeks):
        week += 1
        day = Week(int(year), int(week)).day(0)
        if day.month == month:
            matched_weeks.append(week)

    return matched_weeks


def create_period_list(year, weeks):
    period_list = []
    for week in weeks:
        period_list.append('%sW%s' % (year, week))
    return ",".join(period_list)