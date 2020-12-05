from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class AdminAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Миксин с для ограничения доступа в раздел для админов.
    """
    def test_func(self):
            return self.request.user.is_staff


class AdminDashboardView(AdminAccessMixin, TemplateView):
    template_name = 'dashboards/admin/main.html'
