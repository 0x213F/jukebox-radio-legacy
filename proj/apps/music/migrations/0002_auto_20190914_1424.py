# Generated by Django 2.2.5 on 2019-09-14 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commenter_ticket',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commenter_tickets', to='music.Ticket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('joined', 'Joined'), ('waited', 'Waited'), ('left', 'Left'), ('activated', 'Activated'), ('completed', 'Completed'), ('terminated', 'Terminated'), ('low', ':('), ('mid_low', ':/'), ('neutral', ':|'), ('mid_high', ':)'), ('high', ':D'), ('play', 'Played'), ('pause', 'Paused'), ('neutral', 'Neutral'), ('next', 'Skipped'), ('prev', 'Backtracked')], max_length=12),
        ),
    ]
