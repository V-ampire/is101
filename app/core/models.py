from django.db import models


class TimeStamptedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class StatusModel(models.Model):
    """
    Модель позволяющая не удалять, а перемещать записи в архив.
    """
    WORKS = 'works'
    ARCHIVED = 'archived'
    STATUS_CHOISES = (
        (WORKS, "Работает"),
        (ARCHIVED, "В архиве")
    )
    status = models.CharField("Статус", choices=STATUS_CHOISES, default=WORKS, max_length=10)
    class Meta:
        abstract = True
        ('status', )

    def to_archive(self):
        """
        Перевести запись в статус В архиве
        """
        self.status = self.ARCHIVED
        self.save()

    def to_work(self):
        """
        Перевести запись в статус Работает
        """
        self.status = self.WORKS
        self.save()