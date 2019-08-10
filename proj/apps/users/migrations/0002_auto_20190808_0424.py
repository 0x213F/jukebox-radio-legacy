# Generated by Django 2.1.1 on 2019-08-08 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='spotify_access_token',
            field=models.CharField(blank=True, max_length=158, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='spotify_refresh_token',
            field=models.CharField(blank=True, max_length=134, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='spotify_scope',
            field=models.CharField(blank=True, max_length=108, null=True),
        ),
    ]