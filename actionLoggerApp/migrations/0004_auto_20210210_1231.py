# Generated by Django 3.1.6 on 2021-02-10 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0003_auto_20210210_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='address',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='tel',
            field=models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{2,4}-[0-9]{2,4}-[0-9]{3,4}$')]),
        ),
    ]