# Generated by Django 3.1.6 on 2021-02-16 02:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0018_actionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionlog',
            name='goHomeTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
