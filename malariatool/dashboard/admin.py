from django.contrib import admin

# Register your models here.
from dashboard.models import District, IP, Meeting, Task, User
from dashboard.models.document import Document
from dashboard.models.excel_documents import ExcelDocument
from dashboard.models.tasks import Item

admin.site.register(Document)
admin.site.register(District)
admin.site.register(IP)
admin.site.register(Meeting)
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Item)
admin.site.register(ExcelDocument)

