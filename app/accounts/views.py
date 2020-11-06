from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from accounts import utils
from accounts.models import IPAddress

import datetime


class MyLoginView(LoginView):
    """LoginView с ограничение попыток входа"""

    template_block = 'accounts/block.html'

    def render_block_template(self, unblock_time):
        return render(self.request, self.template_block, {'unblock_time': unblock_time})

    def post(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        form = self.get_form()
        ip_adress = utils.process_ip(ip)
        if ip_adress.is_blocked:
            return self.render_block_template(ip_adress.unblock_time)
        if form.is_valid():
            return self.form_valid(form)
        else:
            ip_adress = utils.process_attempt(ip)
            if ip_adress.is_blocked:
                return self.render_block_template(ip_adress.unblock_time)
            return self.form_invalid(form)


# class BlockView(TemplateView):
#     template_name = 'my_auth/block.html'

#     def get_context_data(self, **kwargs):
#         context = super(BlockView, self).get_context_data(**kwargs)
#         unblock_time = timezone.now() + datetime.timedelta(minutes=15)
#         print(type(unblock_time))
#         context['unblock_time'] = unblock_time
#         return context
    