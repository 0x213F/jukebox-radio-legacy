# Generated by Django 3.0 on 2020-03-19 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_stream_unique_custom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='unique_custom_id',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
