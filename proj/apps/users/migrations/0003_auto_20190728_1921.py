# Generated by Django 2.1.1 on 2019-07-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_showing_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='showing_uuid',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
