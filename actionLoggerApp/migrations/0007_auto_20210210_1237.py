# Generated by Django 3.1.6 on 2021-02-10 12:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0006_auto_20210210_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='userId',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^[0-9]{4-10}$')]),
        ),
    ]
