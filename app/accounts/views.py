from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from django.utils import timezone

from accounts import forms
from accounts import utils
from accounts.models import IPAddress

import datetime


class BruteForceLoginView(LoginView):
    """
    LoginView с ограничение попыток входа
    """
    template_name = 'accounts/login.html'
    template_block = 'accounts/block.html'

    def render_block_template(self, unblock_time):
        return render(self.request, self.template_block, {'unblock_time': unblock_time})

    def post(self, request, *args, **kwargs):
        ip = utils.get_client_ip(request)
        form = self.get_form()
        ip_address = utils.process_ip(ip)
        if ip_address.is_blocked:
            return self.render_block_template(ip_address.unblock_time)
        if form.is_valid():
            return self.form_valid(form)
        else:
            ip_address = utils.process_attempt(ip)
            if ip_address.is_blocked:
                return self.render_block_template(ip_address.unblock_time)
            return self.form_invalid(form)


class LoginView(BruteForceLoginView):
    """
    LoginView для пользователей CRM.
    """
    form = forms.LoginForm
    redirect_authenticated_user = True

    def get_redirect_url_for_admin(self):
        """
        Возвращает URL для админов.
        """
        return reverse_lazy('admins_dashboard:main')

    def get_redirect_url(self):
        if self.request.user.is_staff:
            return self.get_redirect_url_for_admin()    


class BlockView(TemplateView):
    template_name = 'accounts/block.html'

    def get_context_data(self, **kwargs):
        context = super(BlockView, self).get_context_data(**kwargs)
        unblock_time = timezone.now() + datetime.timedelta(minutes=15)
        context['unblock_time'] = unblock_time
        return context
    