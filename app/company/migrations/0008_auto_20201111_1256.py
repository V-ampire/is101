# Generated by Django 3.1.3 on 2020-11-11 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20201110_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='city',
            field=models.CharField(default='Комсомольск-на-Амуре', max_length=264, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=264, unique=True, verbose_name='Название должности'),
        ),
    ]