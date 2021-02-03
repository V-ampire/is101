from django.urls import path, include

from api.v1.accounts.router import urls as accounts_urls
from api.v1.companies.router import urls as companies_urls
from api.v1.positions.router import urls as positions_urls

app_name = 'api_v1'

urlpatterns = [
    path('accounts/', include(accounts_urls)),
    path('companies/', include(companies_urls)),
    path('positions/', include(positions_urls)),
]