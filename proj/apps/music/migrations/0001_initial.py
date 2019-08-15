# Generated by Django 2.1.1 on 2019-08-15 06:24

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
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.URLField(max_length=256)),
                ('title', models.CharField(max_length=128)),
                ('release_date', models.DateField()),
                ('spotify_uri', models.CharField(max_length=36)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='artist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('joined', 'Joined'), ('waited', 'Waited'), ('left', 'Left'), ('activated', 'Activated'), ('completed', 'Completed'), ('terminated', 'Terminated'), ('low', ':('), ('mid_low', ':/'), ('mid_high', ':)'), ('high', ':D')], max_length=12)),
                ('text', models.TextField(blank=True, null=True)),
                ('showing_timestamp', models.DurationField()),
                ('track_timestamp', models.DurationField()),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showtime_actual', models.DateTimeField(null=True)),
                ('showtime_scheduled', models.DateTimeField()),
                ('status', models.CharField(default='scheduled', max_length=128)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='albums', to='music.Album')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Side',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_administrator', models.BooleanField(default=False)),
                ('timestamp_join', models.DateTimeField(auto_now_add=True)),
                ('timestamp_last_active', models.DateTimeField(auto_now_add=True)),
                ('display_name', models.CharField(editable=False, max_length=32)),
                ('display_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to='music.Showing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('number', models.PositiveIntegerField()),
                ('runtime', models.DurationField()),
                ('spotify_uri', models.CharField(max_length=36)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks', to='music.Album')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='side',
            name='track_0',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track0', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track1', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track2', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track3', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track4', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track5', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track6', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_7',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track7', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_8',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track8', to='music.Track'),
        ),
        migrations.AddField(
            model_name='side',
            name='track_9',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sides_with_track9', to='music.Track'),
        ),
        migrations.AddField(
            model_name='comment',
            name='showing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Showing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Track'),
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='albums', to='music.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='sides',
            field=models.ManyToManyField(blank=True, to='music.Side'),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together={('number', 'album')},
        ),
    ]
