# Generated by Django 3.1.6 on 2021-02-13 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0017_auto_20210212_0511'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('place', models.TextField(blank=True, max_length=200, null=True)),
                ('reason', models.TextField(blank=True, max_length=200, null=True)),
                ('remarks', models.TextField(blank=True, max_length=200, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
