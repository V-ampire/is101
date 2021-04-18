from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models

from companies import validators

from core.models import TimeStamptedModel, StatusModel, Statuses

import uuid


def get_company_media_path(instance, filename) -> str:
    """
    Возвращает путь к директории в которую сохраняются сканы паспортов.
    Путь опеределяется по шаблону: 
    /companies/<company_uuid>/company_media/<filename>
    """
    return f"companies/{instance.uuid}/company_media/{filename}"


class CompanyProfile(TimeStamptedModel, StatusModel):
    """
    Информация о компании.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="company_profile")
    title = models.CharField("Название компании", max_length=128, unique=True)
    logo = models.ImageField("Логотип компании", upload_to=get_company_media_path,
                                validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])
    tagline = models.CharField("Слоган компании", max_length=264)
    inn = models.CharField("ИНН", max_length=12, unique=True)
    ogrn = models.CharField("ОГРН\ОГРНИП", max_length=15, unique=True)
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    phone = models.CharField("Номер телефона", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Юридические лица'
        verbose_name_plural = 'Юридические лица'
        ordering = ('title', '-created')


class Branch(TimeStamptedModel, StatusModel):
    """
    Модель филиала компании.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company = models.ForeignKey("companies.CompanyProfile", on_delete=models.CASCADE, related_name="branches")
    city = models.CharField("Город", max_length=264, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    phone = models.CharField("Номер телефона", max_length=32) # FIXME список телефонов

    def __str__(self):
        return f"{self.city}, {self.address}"

    class Meta:
        verbose_name = 'Филиалы'
        verbose_name_plural = 'Филиалы'


class Position(TimeStamptedModel, StatusModel):
    """
    Модель должности.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField("Название должности", max_length=264, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должности'
        verbose_name_plural = 'Должности'


def get_employee_pasport_scan_path(instance, filename) -> str:
    """
    Возвращает путь к директории в которую сохраняются сканы паспортов.
    Путь опеределяется по шаблону: 
    /companies/<company_uuid>/employees/<employee_uuid>/<employee.fio>
    """
    company_uuid = instance.branch.company.uuid
    return f"companies/{company_uuid}/employees/{instance.uuid}/{instance.fio}"


class EmployeeProfile(TimeStamptedModel, StatusModel):
    """
    Модель работника.
    DEFAULT_POSTITION - значение, которое будет использовано 
    если работнику не назначана должность.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="employee_profile")
    fio = models.CharField("ФИО", max_length=264)
    branch = models.ForeignKey("companies.Branch", on_delete=models.CASCADE, null=True, 
                                    related_name='employees')
    position = models.ForeignKey("companies.Position", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField("Дата рождения")
    pasport = models.CharField("Паспортные данные", max_length=264, unique=True)
    pasport_scan = models.FileField(
        "Скан паспорта",
        max_length=264, 
        upload_to=get_employee_pasport_scan_path, 
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'pdf', 'zip'])]
    )

    @property
    def company(self):
        return self.branch.company.title

    # def __str__(self):
    #     return f"{self.position.title}: {self.fio}"

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ('branch',)