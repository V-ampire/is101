from django.views import View
from django.views.generic import  TemplateView
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.shortcuts import render

from .utils import get_next_url, get_client_ip, check_temp_url_token, get_random_password
from .models import TemporaryBanIP
from .forms import CustomConfirmedUserCreationForm, ResendConfirmForm

import datetime


class MyLoginView(LoginView):
    """LoginView с ограничение попыток входа"""

    template_block = 'my_auth/block.html'

    @property
    def attempts_15_minutes_block(self):
        """Кортеж с количеством попыток для бана на 15 мин"""
        return settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']
    
    @property
    def attempts_24_hours_block(self):
        """Кортеж с количеством попыток для бана на 24 часа"""
        return settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']

    def render_block_template(self, ip_adress):
        return render(self.request, self.template_block, {'unblock_time': ip_adress.unblock_time})

    def post(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        form = self.get_form()
        try:
            ip_adress = TemporaryBanIP.objects.get(ip=ip)
            if ip_adress.is_blocked:
                if ip_adress.time_unblock < timezone.now():
                    ip_adress.is_blocked = False
                    ip_adress.save()
                else:
                    return self.render_block_template(ip_adress)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form, ip_adress)

        except TemporaryBanIP.DoesNotExist:
            if form.is_valid():
                return self.form_valid(form)
            else:
                ip_adress = TemporaryBanIP.objects.create(ip=ip)
                return self.form_invalid(form, ip_adress)
    
    def form_invalid(self, form, ip_adress, **kwargs):
        """Если форма не валидна проверить количество запросов с IP"""
        ip_adress.attempts += 1
        ip_adress.save()
        if ip_adress.attempts in self.attempts_15_minutes_block:
            ip_adress.block(minutes=15)
            return self.render_block_template(ip_adress)
        elif ip_adress.attempts in self.attempts_24_hours_block:
            ip_adress.block(minutes=24*60)
            return self.render_block_template(ip_adress)
        else:
            return super(MyLoginView, self).form_invalid(form)


class BlockView(TemplateView):
    template_name = 'my_auth/block.html'

    def get_context_data(self, **kwargs):
        context = super(BlockView, self).get_context_data(**kwargs)
        unblock_time = timezone.now() + datetime.timedelta(minutes=15)
        print(type(unblock_time))
        context['unblock_time'] = unblock_time
        return context
    