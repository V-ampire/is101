from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from accounts.models import UserAccount

class UserAccountChangeForm(UserChangeForm):

    def clean_is_superuser(self):
        role = self.cleaned_data['role']
        is_superuser = self.cleaned_data['is_superuser']
        if is_superuser and role != UserAccount.ADMIN:
            raise ValidationError(f'User with role {role} can not be a superuser')
        return is_superuser
        