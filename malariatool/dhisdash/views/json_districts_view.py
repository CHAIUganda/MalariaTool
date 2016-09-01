import json

from django.http import HttpResponse
from django.views.generic import View

from dhisdash.models import District


class JsonDistrictsView(View):
    def get(self, request):
        districts = District.objects.all()
        result = [(d.id, d.name) for d in districts]
        return HttpResponse(json.dumps(dict(result)))
