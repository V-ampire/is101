from django.urls import path, include

from api.v1.accounts.router import router as accounts_router
from api.v1.companies.router import urls as companies_urls

app_name = 'api_v1'

urlpatterns = [
    path('accounts/', include(accounts_router.urls)),
    path('companies/', include(companies_urls)),
]