# Generated by Django 3.1.5 on 2021-02-21 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20210213_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='status',
            field=models.CharField(choices=[('works', 'Работает'), ('archived', 'В архиве')], default='works', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='status',
            field=models.CharField(choices=[('works', 'Работает'), ('archived', 'В архиве')], default='works', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='status',
            field=models.CharField(choices=[('works', 'Работает'), ('archived', 'В архиве')], default='works', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='position',
            name='status',
            field=models.CharField(choices=[('works', 'Работает'), ('archived', 'В архиве')], default='works', max_length=10, verbose_name='Статус'),
        ),
    ]