# Generated by Django 2.1.1 on 2019-08-08 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='spotify_uri',
            field=models.CharField(default=1, max_length=36),
            preserve_default=False,
        ),
    ]
