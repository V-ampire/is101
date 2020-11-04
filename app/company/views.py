from django.views.generic import TemplateView

from company import models


# class IndexView(TemplateView):
#     template_name = 'company/index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['company'] = models.Company.objects.filter(is_current=True)[0]
#         context['branches'] = models.Branch.objects.all()

