from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse


class AdminAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Миксин с для ограничения доступа в раздел для админов.
    """
    def test_func(self):
        return self.request.user.is_staff


class AdminDashboardView(AdminAccessMixin, TemplateView):
    template_name = 'dashboards/admin.html'


class CompanyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/company.html'


class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/employee.html'
