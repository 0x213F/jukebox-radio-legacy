# Generated by Django 3.0 on 2020-03-21 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_auto_20200321_0556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='holder_name',
        ),
    ]