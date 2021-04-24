# Generated by Django 3.2 on 2021-04-17 07:22

import companies.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_companyprofile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='pasport_scan',
            field=models.FileField(max_length=264, upload_to=companies.models.get_employee_pasport_scan_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'pdf', 'zip'])], verbose_name='Скан паспорта'),
        ),
    ]