# Generated by Django 3.2 on 2021-04-11 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210411_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='creator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_accounts', to='accounts.useraccount'),
        ),
    ]
