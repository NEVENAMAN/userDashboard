# Generated by Django 2.2.4 on 2023-01-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appDashboard', '0002_auto_20230105_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_level',
            field=models.CharField(default='', max_length=255),
        ),
    ]
