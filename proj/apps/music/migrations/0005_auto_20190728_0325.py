# Generated by Django 2.1.1 on 2019-07-28 03:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20190727_2025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='showing',
            old_name='showtime',
            new_name='scheduled_showtime',
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='showing',
            name='actual_showtime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='music.Track'),
        ),
    ]
