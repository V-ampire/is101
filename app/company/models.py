from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from core.models import TimeStamptedModel

from company.utils import get_employee_pasport_scan_path


class BusinessEntity(TimeStamptedModel):
    """
    Модель юридического лица.
    """
    title = models.CharField("Наименование юр. лица", max_length=128, unique=True)
    inn = models.CharField("ИНН", max_length=12, unique=True)
    ogrn = models.CharField("ОГРН\ОГРНИП", max_length=15, unique=True)
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    email = models.EmailField("Имеил")
    phone = models.CharField("Номер телефона", max_length=12)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация об организациях'
        verbose_name_plural = 'Информация о организациях
        ordering = ('is_active', 'title', '-created')


class Company(TimeStamptedModel):
    """
    Информация о компании.
    """
    entity = models.ForeignKey("company.BusinessEntity", on_delete=models.CASCADE, related_name="companies")
    title = models.CharField("Название компании", max_length=128, unique=True)
    logo = models.ImageField("Логотип компании", upload_to="logo/%Y/%m/%d/")
    tagline = models.CharField("Слоган компании", max_length=264)
    is_current = models.BooleanField("Текущая настройка", default=True)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация о компаниях'
        verbose_name_plural = 'Информация о компаниях'


class Branch(TimeStamptedModel):
    """
    Модель филиала компании.
    """
    city = models.CharField("Город", max_length=64, default="Комсомольск-на-Амуре") # FIXME батарейка для городов
    address = models.CharField("Адрес, без города", max_length=264)
    phone = models.CharField("Номер телефона", max_length=12) # FIXME список телефонов

    def __str__(self):
        return f"{self.city}, {self.address}"

    class Meta:
        verbose_name = 'Филиалы'
        verbose_name_plural = 'Филиалы'


class Position(TimeStamptedModel):
    """
    Модель должности.
    """
    title = models.CharField("Название должности", max_length=64, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должности'
        verbose_name_plural = 'Должности'


class Employee(TimeStamptedModel):
    """
    Модель работника.
    """
    ACTIVE = "1"
    ARCHIVED = "0"
    STATUS_CHOISES = (
        (ACTIVE, "Работает"),
        (ARCHIVED, "В архиве")
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    branch = models.ForeignKey("company.Branch", on_delete=models.SET_NULL, null=True, 
                                    related_name='employees')
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField("Дата рождения")
    pasport = models.CharField("Паспортные данные", max_length=264)
    pasport_scan = models.FileField("Скан паспорта", upload_to=get_employee_pasport_scan_path, 
                                    validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'pdf', 'zip'])])
    status = models.CharField("Статус", max_length=16, choices=STATUS_CHOISES, default=ACTIVE)

    def disable_user(self):
        """
        Отключить учетку работника.
        """
        self.user.is_active = False
        self.user.save()

    def save(self, *args, **kwargs):
        if self.status == self.ARCHIVED:
            self.disable_user()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.position.title}: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ('status', 'branch', 'position')