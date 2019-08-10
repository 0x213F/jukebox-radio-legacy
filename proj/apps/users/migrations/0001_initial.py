# Generated by Django 2.1.1 on 2019-08-10 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_showing_uuid', models.UUIDField(blank=True, null=True)),
                ('default_display_name', models.CharField(blank=True, max_length=32, null=True)),
                ('spotify_access_token', models.CharField(blank=True, max_length=158, null=True)),
                ('spotify_refresh_token', models.CharField(blank=True, max_length=134, null=True)),
                ('spotify_scope', models.CharField(blank=True, max_length=108, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
