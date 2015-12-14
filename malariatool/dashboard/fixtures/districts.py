import csv

from django.contrib.contenttypes.models import ContentType
from django.core import serializers

from dashboard.models import District

content_type = ContentType.objects.get_for_model(District)

f = open('districts.csv', 'rb')
reader = csv.reader(f)
for row in reader:
    District.objects.create(name=row[0])
f.close()

data = serializers.serialize("json", District.objects.all())
print data
