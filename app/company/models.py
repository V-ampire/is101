from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import TimeStamptedModel

from company.utils import get_employee_pasport_scan_path


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
        ('-status', )


class Company(TimeStamptedModel, StatusModel):
    """
    Информация о компании.
    """
    title = models.CharField("Название компании", max_length=128, unique=True)
    logo = models.ImageField("Логотип компании", upload_to="logo/%Y/%m/%d/")
    tagline = models.CharField("Слоган компании", max_length=264)
    inn = models.CharField("ИНН", max_length=12, unique=True)
    ogrn = models.CharField("ОГРН\ОГРНИП", max_length=15, unique=True)
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    email = models.EmailField("Имеил")
    phone = models.CharField("Номер телефона", max_length=12)

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
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="branches")
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    phone = models.CharField("Номер телефона", max_length=12) # FIXME список телефонов

    def __str__(self):
        return f"{self.city}, {self.address}"

    class Meta:
        verbose_name = 'Филиалы'
        verbose_name_plural = 'Филиалы'


class Position(TimeStamptedModel, StatusModel):
    """
    Модель должности.
    """
    title = models.CharField("Название должности", max_length=64, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должности'
        verbose_name_plural = 'Должности'


class Employee(TimeStamptedModel, StatusModel):
    """
    Модель работника.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    fio = models.CharField("ФИО", max_length=264)
    branch = models.ForeignKey("company.Branch", on_delete=models.SET_NULL, null=True, 
                                    related_name='employees')
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField("Дата рождения")
    pasport = models.CharField("Паспортные данные", max_length=264)
    pasport_scan = models.FileField("Скан паспорта", upload_to=get_employee_pasport_scan_path, 
                                    validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'pdf', 'zip'])])

    def __str__(self):
        return f"{self.position.title}: {self.fio}"

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ('branch', 'position')