# Generated by Django 3.0.3 on 2020-04-18 18:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('played_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128)),
                ('spotify_uri', models.CharField(max_length=128)),
                ('spotify_name', models.CharField(max_length=128)),
                ('spotify_duration_ms', models.PositiveIntegerField(blank=True, null=True)),
                ('spotify_img', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('unique_custom_id', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('status', models.CharField(default='idle', max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('tags', models.CharField(max_length=128)),
                ('owner_name', models.CharField(max_length=128)),
                ('is_private', models.BooleanField(default=False)),
                ('record_begun_at', models.DateTimeField(null=True)),
                ('record_terminates_at', models.DateTimeField(null=True)),
                ('played_at', models.DateTimeField(null=True)),
                ('paused_at', models.DateTimeField(null=True)),
                ('current_queue', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_stream', to='music.Queue')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('spotify_uri', models.CharField(max_length=64)),
                ('spotify_name', models.CharField(max_length=256)),
                ('spotify_duration_ms', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrackListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('number', models.PositiveIntegerField()),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks_through', to='music.Record')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='records_through', to='music.Track')),
            ],
            options={
                'abstract': False,
                'unique_together': {('track', 'record', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.CharField(editable=False, max_length=64)),
                ('name', models.CharField(editable=False, max_length=32)),
                ('status', models.CharField(choices=[('created_stream', 'Created stream'), ('added_as_host', 'Added as host')], max_length=32)),
                ('is_active', models.BooleanField(default=False)),
                ('is_administrator', models.BooleanField(default=False)),
                ('holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to='music.Stream')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='stream',
            name='current_tracklisting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='now_playing_tracklisting', to='music.TrackListing'),
        ),
        migrations.AddField(
            model_name='stream',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='owned_streams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='record',
            name='tracks',
            field=models.ManyToManyField(through='music.TrackListing', to='music.Track'),
        ),
        migrations.CreateModel(
            name='QueueListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('start_at_ms', models.PositiveIntegerField()),
                ('end_at_ms', models.PositiveIntegerField()),
                ('played_at', models.DateTimeField(blank=True, null=True)),
                ('paused_at', models.DateTimeField(blank=True, null=True)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queue_listings', to='music.Queue')),
                ('track_listing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queued_listing', to='music.TrackListing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='queue',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queued', to='music.Record'),
        ),
        migrations.AddField(
            model_name='queue',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queued', to='music.Stream'),
        ),
        migrations.AddField(
            model_name='queue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='queued', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('joined', 'Joined'), ('left', 'Left'), ('comment', 'Commented'), ('spinning', 'Spinning'), ('play', 'Played'), ('paused', 'Paused'), ('next', 'Next'), ('skip', 'Skipped')], max_length=12)),
                ('text', models.TextField(blank=True, null=True)),
                ('track_timestamp', models.DurationField(blank=True, null=True)),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('commenter_ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commenter_tickets', to='music.Ticket')),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spins', to='music.Record')),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Stream')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Track')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
