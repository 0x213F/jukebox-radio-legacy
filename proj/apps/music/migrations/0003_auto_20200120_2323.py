# Generated by Django 3.0 on 2020-01-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_stream_vote_controlled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('joined', 'Joined'), ('waited', 'Waited'), ('left', 'Left'), ('activated', 'Activated'), ('idle', 'Idle'), ('low', ':('), ('mid_low', ':/'), ('neutral', ':|'), ('mid_high', ':)'), ('high', ':D'), ('spin', 'Spinning'), ('stop', 'Stopped'), ('start', 'Started'), ('play', 'Played'), ('pause', 'Paused'), ('neutral', 'Neutral'), ('next', 'Skipped'), ('prev', 'Backtracked'), ('queue', 'Queued')], max_length=12),
        ),
    ]
