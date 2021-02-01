from django.db import models


class TimeStamptedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class Statuses(models.IntegerChoices):
    WORKS = 1, 'Работает'
    ARCHIVED = 0, 'В архиве'


class StatusModel(models.Model):
    """
    Модель позволяющая не удалять, а перемещать записи в архив.
    """
    status = models.IntegerField("Статус", choices=Statuses.choices, default=Statuses.WORKS)

    class Meta:
        abstract = True
        ordering = ('status', )

    def to_archive(self):
        """
        Перевести запись в статус В архиве
        """
        self.status = Statuses.ARCHIVED
        self.save()

    def to_work(self):
        """
        Перевести запись в статус Работает
        """
        self.status = Statuses.WORKS
        self.save()