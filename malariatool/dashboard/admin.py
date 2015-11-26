from django.contrib import admin

# Register your models here.
from dashboard.models import District, IP, Meeting, Task, User
from dashboard.models.document import Document

admin.site.register(Document)
admin.site.register(District)
admin.site.register(IP)
admin.site.register(Meeting)
admin.site.register(Task)
admin.site.register(User)
