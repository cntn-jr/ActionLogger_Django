# Generated by Django 3.1.6 on 2021-04-01 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actionLoggerApp', '0023_auto_20210312_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('informationText', models.TextField(max_length=200)),
                ('groupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actionLoggerApp.mgtgroup')),
            ],
        ),
    ]