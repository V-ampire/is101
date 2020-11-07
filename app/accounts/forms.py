from django.contrib.auth.forms import UserChangeForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import UserAccount

class UserAccountChangeForm(UserChangeForm):

    class Meta:
        model = UserAccount
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data['role']
        is_superuser = cleaned_data['is_superuser']
        if is_superuser and role != UserAccount.ADMIN:
            raise ValidationError(
                _('User with role %(role)s can not be a superuser'), 
                params={'role': role}
            )
        

class LoginForm(AuthenticationForm):
    """
    Форма для входа в систему
    """
    pass