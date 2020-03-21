# Generated by Django 3.0 on 2020-03-21 05:33

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0015_auto_20200319_0647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='timestamp_join',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='timestamp_last_active',
        ),
        migrations.AddField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 3, 21, 5, 32, 14, 60910)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stream',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 3, 21, 5, 32, 20, 946003)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='is_listed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default=1, editable=False, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=1, editable=False, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='track',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 3, 21, 5, 32, 40, 330341)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracklisting',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 3, 21, 5, 32, 48, 306624)),
            preserve_default=False,
        ),
    ]