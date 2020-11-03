from django.contrib.auth import get_user_model
from django.db import models

from core.models import TimeStamptedModel


class Company(TimeStamptedModel):
    """
    Информация о компании.
    """
    title = models.CharField("Название компании", max_length=128, unique=True)
    logo = models.ImageField("Логотип компании", upload_to="logo/%Y/%m/%d/")
    tagline = models.CharField("Слоган компании", max_length=264)
    is_current = models.BooleanField("Текущая настройка", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'


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
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    branch = models.ForeignKey("company.Branch", on_delete=models.SET_NULL, null=True, 
                                    related_name='employees')
    position = models.ForeignKey("company.Position", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.position.title}: {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'