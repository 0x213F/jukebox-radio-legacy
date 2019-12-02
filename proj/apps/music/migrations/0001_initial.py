# Generated by Django 2.2.5 on 2019-12-02 06:32

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
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_playing', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=128)),
                ('showtime_actual', models.DateTimeField(null=True)),
                ('record_terminates_at', models.DateTimeField(null=True)),
                ('status', models.CharField(default='idle', max_length=128)),
                ('current_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='now_playing_at_showings', to='music.Record')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spotify_uri', models.CharField(max_length=36)),
                ('spotify_name', models.CharField(max_length=64)),
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
                ('number', models.PositiveIntegerField()),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks_through', to='music.Record')),
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
                ('is_administrator', models.BooleanField(default=False)),
                ('timestamp_join', models.DateTimeField(auto_now_add=True)),
                ('timestamp_last_active', models.DateTimeField(auto_now_add=True)),
                ('holder_name', models.CharField(editable=False, max_length=32)),
                ('holder_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to='music.Showing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='record',
            name='tracks',
            field=models.ManyToManyField(through='music.TrackListing', to='music.Track'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('joined', 'Joined'), ('waited', 'Waited'), ('left', 'Left'), ('activated', 'Activated'), ('idle', 'Idle'), ('terminated', 'Terminated'), ('low', ':('), ('mid_low', ':/'), ('neutral', ':|'), ('mid_high', ':)'), ('high', ':D'), ('spin', 'Spinning'), ('stop', 'Stopped'), ('start', 'Started'), ('play', 'Played'), ('pause', 'Paused'), ('neutral', 'Neutral'), ('next', 'Skipped'), ('prev', 'Backtracked')], max_length=12)),
                ('text', models.TextField(blank=True, null=True)),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('commenter_ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commenter_tickets', to='music.Ticket')),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='spins', to='music.Record')),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Showing')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Track')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
