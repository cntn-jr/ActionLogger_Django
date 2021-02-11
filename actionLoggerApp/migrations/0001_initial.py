# Generated by Django 3.1.6 on 2021-02-10 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userId', models.IntegerField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=15, null=True)),
                ('lastName', models.CharField(max_length=15, null=True)),
                ('address', models.TextField(max_length=40)),
                ('tel', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(regex='^[0-9]{2,4}-[0-9]{2,4}-[0-9]{3,4}$')])),
                ('email', models.EmailField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
