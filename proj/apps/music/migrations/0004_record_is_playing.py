# Generated by Django 2.2.5 on 2019-11-29 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_remove_record_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='is_playing',
            field=models.BooleanField(default=False),
        ),
    ]
