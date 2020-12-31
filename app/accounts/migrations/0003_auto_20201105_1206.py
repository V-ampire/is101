# Generated by Django 3.1.3 on 2020-11-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201104_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('company', 'Юр. лицо'), ('employer', 'Работник')], default='employer', max_length=16, verbose_name='Тип учетки'),
        ),
    ]
