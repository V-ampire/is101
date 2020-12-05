# Generated by Django 3.1.3 on 2020-11-04 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_employee_fio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='businessentity',
            options={'ordering': ('is_active', 'title', '-created'), 'verbose_name': 'Юридические лица', 'verbose_name_plural': 'Юридические лица'},
        ),
        migrations.AddField(
            model_name='branch',
            name='company',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='company.company'),
            preserve_default=False,
        ),
    ]