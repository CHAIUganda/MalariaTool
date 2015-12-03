from django.views.generic import TemplateView
from rolepermissions.mixins import HasRoleMixin


class AdminDashboardView(HasRoleMixin, TemplateView):
    allowed_roles = 'admin'
    template_name = "admin_index.html"
