from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.validators import is_user_company, is_user_employee

from core.models import TimeStamptedModel

import uuid


class StatusModel(models.Model):
    """
    Модель позволяющая не удалять, а перемещать записи в архив.
    """
    ACTIVE = 1
    ARCHIVED = 0
    STATUS_CHOISES = (
        (ACTIVE, "Работает"),
        (ARCHIVED, "В архиве")
    )
    status = models.PositiveSmallIntegerField("Статус", choices=STATUS_CHOISES, default=ACTIVE)
    class Meta:
        abstract = True
        ('status', )

    def archive(self):
        """
        Архивировать запись.
        """
        self.status = self.ARCHIVED
        self.save()


class Company(TimeStamptedModel, StatusModel):
    """
    Информация о компании.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="company")
    title = models.CharField("Название компании", max_length=128, unique=True)
    logo = models.ImageField("Логотип компании", upload_to="logo/%Y/%m/%d/",
                                validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])
    tagline = models.CharField("Слоган компании", max_length=264)
    inn = models.CharField("ИНН", max_length=12, unique=True)
    ogrn = models.CharField("ОГРН\ОГРНИП", max_length=15, unique=True)
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    email = models.EmailField("Имеил")
    phone = models.CharField("Номер телефона", max_length=32)

    def clean(self):
        is_user_company(self.user.pk)

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
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="branches")
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
    """
    return f"employees_pasports/{instance.fio}"


class Employee(TimeStamptedModel, StatusModel):
    """
    Модель работника.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="employee")
    fio = models.CharField("ФИО", max_length=264)
    branch = models.ForeignKey("company.Branch", on_delete=models.SET_NULL, null=True, 
                                    related_name='employees')
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField("Дата рождения")
    pasport = models.CharField("Паспортные данные", max_length=264)
    pasport_scan = models.FileField("Скан паспорта", upload_to=get_employee_pasport_scan_path, 
                                    validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'pdf', 'zip'])])

    def clean(self):
        is_user_employee(self.user.pk)

    # def __str__(self):
    #     return f"{self.position.title}: {self.fio}"

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ('branch', 'position')