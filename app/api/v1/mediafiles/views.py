from api.v1.permissions import IsCompanyOwnerOrAdmin

from private_storage.views import PrivateStorageView


class CompanyMediaView(PrivateStorageView):
    """
    Определяет давать ли доступ к статическому файлу юрлица.
    """
    company_uuid_kwarg = 'company_uuid'

    def can_access_file(self, private_file):
        permission = IsCompanyOwnerOrAdmin()
        return permission.has_permission(self.request, self)

    def get_path(self):
        company_uuid = self.kwargs[self.company_uuid_kwarg]
        media_name = self.kwargs['media_name']
        return f'companies/{company_uuid}/company_media/{media_name}'


class EmployeeMediaView(PrivateStorageView):
    """
    Определяет давать ли доступ к статическому файлу работниа.
    """
    company_uuid_kwarg = 'company_uuid'

    def can_access_file(self, private_file):
        permission = IsCompanyOwnerOrAdmin()
        return permission.has_permission(self.request, self)

    def get_path(self):
        company_uuid = self.kwargs[self.company_uuid_kwarg]
        employee_uuid = self.kwargs['employee_uuid']
        media_name = self.kwargs['media_name']
        return f'companies/{company_uuid}/employees/{employee_uuid}/{media_name}'