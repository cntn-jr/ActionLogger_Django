# Generated by Django 3.1.6 on 2021-04-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0024_groupinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupinformation',
            name='informationTitle',
            field=models.CharField(default='タイトル', max_length=30),
            preserve_default=False,
        ),
    ]