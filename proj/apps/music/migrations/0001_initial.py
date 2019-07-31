# Generated by Django 2.1.1 on 2019-07-31 06:55

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
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.URLField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('release_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
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
                ('status', models.CharField(choices=[('joined', 'Joined'), ('waited', 'Waited'), ('left', 'Left'), ('activated', 'Activated'), ('completed', 'Completed'), ('terminated', 'Terminated'), ('low', ':('), ('mid_low', ':/'), ('mid_high', ':)'), ('high', ':D')], max_length=7)),
                ('text', models.TextField(blank=True, null=True)),
                ('showing_timestamp', models.FloatField()),
                ('track_timestamp', models.FloatField()),
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
                ('status', models.CharField(default='scheduled', editable=False, max_length=128)),
                ('actual_showtime', models.DateTimeField(null=True)),
                ('scheduled_showtime', models.DateTimeField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='albums', to='music.Album')),
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
                ('runtime', models.FloatField()),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tracks', to='music.Album')),
            ],
            options={
                'abstract': False,
            },
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
        migrations.AlterUniqueTogether(
            name='track',
            unique_together={('number', 'album')},
        ),
    ]
