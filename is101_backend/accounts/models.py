from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import datetime


class UserAccountManager(BaseUserManager):
    """
    Менеджер для модели учетной записи пользователя.
    """
    def create_user(self, username, role, password, **extra_fields):
        """
        Создать и сохранить новую учетную запись.
        """
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Создать и сохранить учетку суперпользоватля.
        """
        role = UserAccount.ADMIN
        user = self.create_user(username, role, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CompanyManager(UserAccountManager):
    """
    Менеджер возвращающий только учетки юр. лиц.
    """
    def get_queryset(self):
        return super().get_queryset().filter(role=UserAccount.COMPANY)

    def create_account(self, username, password, **extra_fields):
        """
        Создать учетную запись для компании.
        """
        role = UserAccount.COMPANY
        return self.create_user(username, role, password, **extra_fields)


class EmployeeManager(UserAccountManager):
    """
    Менеджер возвращающий только учетки работников.
    """
    def get_queryset(self):
        return super().get_queryset().filter(role=UserAccount.EMPLOYEE)

    def create_account(self, username, password, **extra_fields):
        """
        Создать учетную запись для работника.
        """
        role = UserAccount.EMPLOYEE
        return self.create_user(username, role, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Модель учетной записи для входа в систему.
    Содержит только поля username и password.
    """
    username_validator = UnicodeUsernameValidator()

    ADMIN = 'admin'
    COMPANY = 'company'
    EMPLOYEE = 'employee'

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (COMPANY, 'Юр. лицо'),
        (EMPLOYEE, 'Работник')
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    role = models.CharField("Тип учетки", max_length=16, choices=ROLE_CHOICES, default=EMPLOYEE)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()
    company_objects = CompanyManager()
    employee_objects = EmployeeManager()

    @property
    def is_staff(self):
        return self.role == self.ADMIN

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = 'Учетные записи'
        verbose_name_plural = 'Учетные записи'


class IPAddress(models.Model):
    """
    IP адрес с возможностью блокировки по числу неудачных попыток входа.
    """ 
    ip = models.GenericIPAddressField("IP адрес", unique=True)
    attempts = models.IntegerField("Неудачных попыток", default=0)
    unblock_time = models.DateTimeField("Время разблокировки", blank=True, null=True)
    is_blocked = models.BooleanField("Статус блокировки", default=False)

    def block(self, minutes: int):
        """Заблокировать IP на указанное количество минут"""
        self.is_blocked = True
        self.unblock_time = timezone.now() + datetime.timedelta(minutes=minutes)
        self.save()

    def unblock(self):
        """
        Разблокировать IP.
        """
        self.is_blocked = False
        self.unblock_time = None
        self.save()

    def clean(self):
        if self.is_blocked and not self.unblock_time:
            raise ValidationError(_("You must set unblock time when blocking IP"))

    def __str__(self):
        return self.ip