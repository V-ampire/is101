from rest_framework.routers import SimpleRouter

from api.v1.accounts import views

router = SimpleRouter()
router.register(
    r'companies', 
    views.CompanyAccountsViewSet, 
    basename='account-companies'
)