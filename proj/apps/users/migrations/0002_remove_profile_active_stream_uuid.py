# Generated by Django 3.0.3 on 2020-04-09 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="active_stream_uuid",),
    ]
